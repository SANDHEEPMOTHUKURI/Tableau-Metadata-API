# Login to the server
# Query Metadata
# Convert the json to CSV file

import tableauserverclient as TSC
import pandas as pd

csv_path = "<file path>"

Server_URL = "<Server URL>"
site_id = "<Site id>"
PAT_Name = "<PAT Name>"
PAT_Token = "<Token Value>"

Tableau_auth = TSC.PersonalAccessTokenAuth(PAT_Name, PAT_Token, site_id)
server = TSC.Server(Server_URL, use_server_version=True)

# Authentication to Tableau Server
def server_auth(Tableau_auth, server):
    return server.auth.sign_in(Tableau_auth)

# Graphql Query for finding list of all workbooks
query_workbooks = """
query workbook {
    workbooks {
        id
        name
        projectName
        owner {
            id
            name
        }
    }
}
"""

# Running query & coneverting the query data to CSV 
def Metadata_query(query_workbooks):
    try:
        query_wb = server.metadata.query(query_workbooks)
        workbooks = query_wb['data']['workbooks']
        data = pd.json_normalize(query_wb['data']['workbooks'])
        data.to_csv(csv_path, index = False)
    except Exception as e:
        print(f"Error: {e}")

# Calling functions
with server_auth(Tableau_auth, server):
    Metadata_query(query_workbooks)