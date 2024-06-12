from hdbcli import dbapi
import pandas as pd

# Connection details
host = 'your_hana_host'
port = 30015
user = 'your_username'
password = 'your_password'

# Establish connection
connection = dbapi.connect(
    address=host,
    port=port,
    user=user,
    password=password
)

# Function to fetch data from a table
def fetch_data(query):
    cursor = connection.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=columns)

# Extract data from Sales_Data table
query = "SELECT Product_ID, Sales_Date, Sales_Amount FROM Sales_Data"
sales_data = fetch_data(query)

# Transform data: aggregate sales by month and product
sales_data['Sales_Date'] = pd.to_datetime(sales_data['Sales_Date'])
sales_data['Sales_Month'] = sales_data['Sales_Date'].dt.to_period('M')
sales_summary = sales_data.groupby(['Product_ID', 'Sales_Month']).agg({'Sales_Amount': 'sum'}).reset_index()
sales_summary['Sales_Month'] = sales_summary['Sales_Month'].dt.to_timestamp()

# Create a new table in SAP HANA for the transformed data
create_table_query = """
CREATE TABLE Sales_Summary (
    Product_ID INTEGER,
    Sales_Month DATE,
    Total_Sales DECIMAL(10, 2)
)
"""
cursor = connection.cursor()
cursor.execute(create_table_query)
connection.commit()

# Load the transformed data into the new table
for index, row in sales_summary.iterrows():
    insert_query = "INSERT INTO Sales_Summary (Product_ID, Sales_Month, Total_Sales) VALUES (?, ?, ?)"
    cursor.execute(insert_query, (row['Product_ID'], row['Sales_Month'], row['Sales_Amount']))
connection.commit()

# Fetch the summary data for reporting
summary_query = "SELECT * FROM Sales_Summary"
summary_data = fetch_data(summary_query)
print(summary_data.head())

# Perform analysis (example: total sales per product)
total_sales_per_product = summary_data.groupby('Product_ID')['Total_Sales'].sum().reset_index()
print(total_sales_per_product)

# Close the connection
connection.close()
