import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

elastic_user = os.getenv('elastic_user')
password = os.getenv('password')

api_key_id = os.getenv('api_key_id')
api_key_secret = os.getenv('api_key_secret')
# Basic Elasticsearch connection
# es = Elasticsearch(
#     hosts=['https://localhost:9200'], 
#     basic_auth=(elastic_user, password),
#     verify_certs=False,
#     ssl_show_warn=False
# )

# try:
#     cluster_info = es.info()
#     print(f"Cluster Info: {cluster_info}")
# except Exception as e:
#     print(f"Connection Failed: {e}")

# # Get The API Key For Connection
# api_key_response = es.security.create_api_key(
#     body={
#         "name": "python-app-key",
#         "role_descriptors": {
#             "python-app-role": {
#                 "cluster": ["monitor"],
#                 "index": [
#                     {
#                         "names": ["logs-*", "metrics-*"],
#                         "privileges": ["read", "write", "create_index"]
#                     }
#                 ]
#             }
#         }
#     }
# )

# api_key_id = api_key_response['id']
# api_key_secret = api_key_response['api_key']

# print(f"The API Key Response: {api_key_response}")
# print(f"The API key ID: {api_key_id}")
# print(f"The API Key Secret: {api_key_secret}")

es = Elasticsearch(
    hosts=['https://localhost:9200'],
    api_key=(api_key_id, api_key_secret),
    verify_certs=False,
    ssl_show_warn=False
)

try:
    cluster_info = es.info()
    print(f"Cluster Info: {cluster_info}")
except Exception as e:
    print(f"Connection Failed: {e}")
