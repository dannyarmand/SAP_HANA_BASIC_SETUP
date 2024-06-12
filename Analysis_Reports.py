# Fetch the summary data for reporting
summary_query = "SELECT * FROM Sales_Summary"
summary_data = fetch_data(summary_query)
print(summary_data.head())

# Perform analysis (example: total sales per product)
total_sales_per_product = summary_data.groupby('Product_ID')['Total_Sales'].sum().reset_index()
print(total_sales_per_product)
