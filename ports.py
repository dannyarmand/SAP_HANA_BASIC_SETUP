#2. Connect to SAP HANA
#Create a connection to your SAP HANA database using the hdbcli library.

from hdbcli import dbapi

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
