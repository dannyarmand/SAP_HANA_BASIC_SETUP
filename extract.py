import pandas as pd

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
print(sales_data.head())
