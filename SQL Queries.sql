create database Retail_Sales_Data;
use Retail_Sales_Data;

select * from retail_data_response;
select * from retail_data_transactions;

-- Check for missing values in transactions
SELECT 
    COUNT(*) AS missing_customer_id 
FROM Retail_Data_Transactions 
WHERE customer_id IS NULL;

SELECT 
    COUNT(*) AS missing_trans_date 
FROM Retail_Data_Transactions 
WHERE trans_date IS NULL;

SELECT 
    COUNT(*) AS missing_tran_amount 
FROM Retail_Data_Transactions 
WHERE tran_amount IS NULL;



-- Total transactions and revenue.

SELECT COUNT(*) AS total_transactions, 
       SUM(tran_amount) AS total_revenue 
FROM Retail_Data_Transactions;


-- Customer-level spending behavior.
SELECT customer_id, 
       COUNT(*) AS total_transactions, 
       SUM(tran_amount) AS total_spent, 
       AVG(tran_amount) AS avg_transaction_amount 
FROM Retail_Data_Transactions 
GROUP BY customer_id 
ORDER BY total_spent DESC 
LIMIT 10;


-- Response rate analysis.
SELECT r.response, 
       COUNT(t.customer_id) AS total_customers, 
       SUM(t.tran_amount) AS total_spent 
FROM Retail_Data_Response r
LEFT JOIN Retail_Data_Transactions t ON r.customer_id = t.customer_id 
GROUP BY r.response;
 
 
-- Create Total Sales per Customer
SELECT customer_id, 
       SUM(tran_amount) AS total_sales 
FROM Retail_Data_Transactions 
GROUP BY customer_id;


-- Top 5 Customers with the Most Frequent Purchases
SELECT customer_id, 
       COUNT(*) AS total_transactions, 
       SUM(tran_amount) AS total_spent 
FROM Retail_Data_Transactions 
GROUP BY customer_id 
ORDER BY total_transactions DESC 
LIMIT 5;

-- Categorizes customers based on total spending.
SELECT customer_id, 
       SUM(tran_amount) AS total_spent,
       CASE 
           WHEN SUM(tran_amount) < 1000 THEN 'Low Spender'
           WHEN SUM(tran_amount) BETWEEN 1000 AND 5000 THEN 'Medium Spender'
           ELSE 'High Spender'
       END AS spending_category
FROM Retail_Data_Transactions
GROUP BY customer_id
ORDER BY total_spent DESC;


-- Response Rate vs Total Spending
SELECT r.response, 
       COUNT(DISTINCT t.customer_id) AS total_customers, 
       SUM(t.tran_amount) AS total_spent, 
       AVG(t.tran_amount) AS avg_spending_per_customer
FROM Retail_Data_Response r
LEFT JOIN Retail_Data_Transactions t ON r.customer_id = t.customer_id 
GROUP BY r.response;


-- the top 10 highest-spending customers.
SELECT customer_id, 
       SUM(tran_amount) AS total_spent 
FROM Retail_Data_Transactions 
GROUP BY customer_id 
ORDER BY total_spent DESC 
LIMIT 10;


-- Identify customers who purchased only once vs. repeat buyers.
SELECT customer_id, 
       COUNT(*) AS transaction_count, 
       SUM(tran_amount) AS total_spent, 
       CASE 
           WHEN COUNT(*) = 1 THEN 'One-Time Customer'
           ELSE 'Returning Customer'
       END AS customer_type
FROM Retail_Data_Transactions
GROUP BY customer_id
ORDER BY transaction_count DESC;









 
 
