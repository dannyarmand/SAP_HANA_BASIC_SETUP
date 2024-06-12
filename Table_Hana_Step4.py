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
