import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()
elastic_user = os.getenv('elastic_user')
password = os.getenv('password')

print(f"The elastic_user is: {elastic_user}")
print(f"The password is: {password}")

es = Elasticsearch(
    hosts=['https://localhost:9200'], 
    basic_auth=(elastic_user, password),
    verify_certs=False,
    ssl_show_warn=False
)

try:
    cluster_info = es.info()
    print(f"Cluster Info: {cluster_info}")
except Exception as e:
    print(f"Connection Failed: {e}")