#!/usr/bin/env python
# coding: utf-8

# In[87]:


get_ipython().system('pip install pandas')


# In[7]:


import pandas as pd


# # load the datasets

# In[8]:


response= pd.read_csv('Retail_Data_Response.csv')


# In[11]:


response


# In[13]:


transactions= pd.read_csv('Retail_Data_Transactions.csv')


# In[14]:


transactions


# In[27]:


# Convert 'trans_date' to datetime format
transactions['trans_date'] = pd.to_datetime(transactions['trans_date'], format='%d-%b-%y')


# # Get basic info about both datasets

# In[28]:


response_info = {
    "shape": response.shape,
    "columns": response.columns.tolist(),
    "missing_values": response.isnull().sum().to_dict()
}

transactions_info = {
    "shape": transactions.shape,
    "columns": transactions.columns.tolist(),
    "missing_values": transactions.isnull().sum().to_dict()
}

# Display first few rows of each dataset
response_head = response.head()
transactions_head = transactions.head()

response_info, response_head, transactions_info, transactions_head


# In[37]:


#Top 10 Customers by Spending
customer_spending = transactions.groupby('customer_id').agg(
    total_transactions=('tran_amount', 'count'),
    total_spent=('tran_amount', 'sum'),
    avg_transaction_amount=('tran_amount', 'mean')
).sort_values(by='total_spent', ascending=False).head(10)


# In[43]:


customer_spending


# In[40]:


#Response Rate Analysis
df_merged = response.merge(transactions, on='customer_id', how='left')
response_analysis = df_merged.groupby('response').agg(
    total_customers=('customer_id', 'count'),
    total_spent=('tran_amount', 'sum')
)


# In[42]:


df_merged


# In[41]:


#Monthly Revenue Trends
transactions['month'] = transactions['trans_date'].dt.to_period('M')
monthly_revenue = transactions.groupby('month')['tran_amount'].sum()


# In[44]:


monthly_revenue


# In[81]:


# creating new columns

df_merged['month']= df_merged['trans_date'].dt.month


# In[82]:


df_merged


# # Analysis

# In[48]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[45]:


# Set style
sns.set_style("whitegrid")

# Plot Monthly Revenue Trend
plt.figure(figsize=(12, 6))
monthly_revenue.sort_index().plot(kind='line', marker='o', color='b')
plt.title("Monthly Revenue Trend", fontsize=14)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total Revenue (₹)", fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


# In[46]:


# Plot Response Rate Spending Behavior
plt.figure(figsize=(6, 6))
sns.barplot(x=response_analysis.index, y=response_analysis["total_spent"], palette=["red", "green"])
plt.title("Spending Behavior: Responders vs Non-Responders", fontsize=14)
plt.xlabel("Response", fontsize=12)
plt.ylabel("Total Spent (₹)", fontsize=12)
plt.xticks([0, 1], ["Non-Responders", "Responders"])
plt.show()


# In[47]:


# Plot Top 10 Customers by Spending
plt.figure(figsize=(12, 6))
sns.barplot(
    x=customer_spending.index, 
    y=customer_spending["total_spent"], 
    palette="Blues_r"
)
plt.title("Top 10 Customers by Total Spending", fontsize=14)
plt.xlabel("Customer ID", fontsize=12)
plt.ylabel("Total Spending (₹)", fontsize=12)
plt.xticks(rotation=45)
plt.show()


# In[66]:


sns.barplot(x='customer_id',y='tran_amount',data=top_5_sal)


# In[63]:


# Customers having highest value of orders

customer_sales= df_merged.groupby('customer_id')['tran_amount'].sum().reset_index()
customer_sales

# sort

top_5_sal= customer_sales.sort_values(by='tran_amount', ascending=False).head(5)
top_5_sal


# In[74]:


# Recency will be the maximum of trans_date
recency = df_merged.groupby('customer_id')['trans_date'].max()

# Frequency will be the count of transactions
frequency = df_merged.groupby('customer_id')['trans_date'].count()

# Monetary will be the sum of tran_amount
monetary = df_merged.groupby('customer_id')['tran_amount'].sum()

# Combine all three into a DataFrame
rfm = pd.DataFrame({'recency': recency, 'frequency': frequency, 'monetary': monetary})


# In[76]:


def segment_customer(row):
    if row['recency'].year >= 2012 and row['frequency'] >= 15 and row['monetary'] > 1000:
        return 'P0'
    elif (2011 <= row['recency'].year < 2012) and (10 < row['frequency'] <= 15) and (500 < row['monetary'] <= 1000):
        return 'P1'
    else:
        return 'P2'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)


# In[77]:


rfm


# In[86]:


df_merged.to_csv('MainData.csv')


# In[85]:


rfm.to_csv('AddAnalysis')

