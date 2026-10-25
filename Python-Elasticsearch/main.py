import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from dotenv import load_dotenv

load_dotenv()

elastic_user = os.getenv('elastic_user')
password = os.getenv('password')

api_key_id = os.getenv('api_key_id')
api_key_secret = os.getenv('api_key_secret')
# Basic Elasticsearch connection
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

# es = Elasticsearch(
#     hosts=['https://localhost:9200'],
#     api_key=(api_key_id, api_key_secret),
#     verify_certs=False,
#     ssl_show_warn=False
# )

# try:
#     cluster_info = es.info()
#     health = es.cluster.health()
#     print(f"Cluster info: {cluster_info}")
#     print(f"The health is: {health}")
# except Exception as e:
#     print(f"Connection Failed: {e}")

# es.indices.create(index='articles', body=index_settings)

# Update index settings
# update_settings = {
#     'index': {
#         'refresh_interval': '60s',
#         'number_of_replicas': 2
#     }
# }

# es.indices.put_settings(index='articles', body=update_settings)

# settings = {
#     "number_of_shards": 3,
#     "number_of_replicas": 1,
#     "refresh_interval": "30s",
#     "analysis": {
#         "analyzer": {
#             "custom_analyzer": {
#                 "type": "custom",
#                 "tokenizer": "standard",
#                 "filter": ["lowercase", "stop"]
#             }
#         }
#     }
# }

# mappings = {
#     "properties": {
#         "title": {
#             "type": "text",
#             "analyzer": "standard",
#             "fields": {
#                 "keyword": {"type": "keyword"}
#             }
#         },
#         "content": {
#             "type": "text",
#             "analyzer": "custom_analyzer"
#         },
#         "publish_date": {
#             "type": "date",
#             "format": "yyyy-MM-dd||epoch_millis"
#         },
#         "author": {
#             "type": "object",
#             "properties": {
#                 "name": {"type": "text"},
#                 "email": {"type": "keyword"},
#                 "bio": {"type": "text"}
#             }
#         },
#         "tags": {"type": "keyword"},
#         "view_count": {"type": "integer"},
#         "rating": {"type": "float"},
#         "metadata": {
#             "type": "object",
#             "enabled": False
#         }
#     }
# }

# es.indices.create(
#     index="articles",
#     body={
#         "settings": settings,
#         "mappings": mappings
#     }
# )

document = {
    'title': 'Getting Started with Elasticsearch and Python',
    'content': 'This guide covers how to index documents, run searches, and optimize performance.',
    'publish_date': '2024-01-15',
    'author': {
        'name': 'John Developer',
        'email': 'john@example.com',
        'bio': 'Senior Python developer with expertise in search technologies'
    },
    'tags': ['elasticsearch', 'python', 'tutorial', 'search'],
    'view_count': 1250,
    'rating': 4.7,
    'metadata': {
        'source': 'blog',
        'category': 'technical'
    }
}

# response = es.index(index='articles', id=1, body=document)
# print(f"Document indexed: {response['result']}")

# Check index status
# index_stats = es.indices.stats(index='articles')
# print(f"The index stats is: {index_stats}")
# print(f"Document count: {index_stats['indices']['articles']['total']['docs']['count']}")
# print(f"Index size: {index_stats['indices']['articles']['total']['store']['size_in_bytes']} bytes")

# Generate and prepare documents
# documents = []
# for i in range(1000):
#     documents.append({
#         '_index': 'articles',
#         '_id': i,
#         '_source': {
#             'title': f'Article {i}',
#             'content': f'Content for article number {i}',
#             'publish_date': '2026-10-24',
#             'tags': ['bulk', 'indexing', 'test'],
#             'view_count': i * 10,
#             'rating': 4.0 + (i % 10) * 0.1
#         }
#     })

# Bulk indexing
# You can tune chunk_size based on memory and performance. 
# For high-throughput pipelines, this is the preferred method.
# bulk(es, documents, chunk_size=100)
# print(f"Indexed {len(documents)} documents")

search_query = {
    'query': {
        'match': {
            'content': 'Content Article 11'
        }
    },
    'size': 10
}

response = es.search(index='articles', body=search_query)

print(f"Found {response['hits']['total']['value']} documents")
for hit in response['hits']['hits']:
    print(f"Score: {hit['_score']}, Title: {hit['_source']['title']}, Content: {hit['_source']['content']}")

# Use complex query to search the data
complex_query = {
    'query': {
        'bool': {
            'must': [
                {'match': {'content': 'Article'}}
            ],
            'filter': [
                {'term': {'tags': 'indexing'}},
                {'range': {'rating': {'gte': 4.0}}}
            ],
            'should': [
                {'match': {'title': '11'}}
            ]
        }
    },
    'sort': [
        {'publish_date': {'order': 'desc'}},
        {'rating': {'order': 'desc'}}
    ],
    'highlight': {
        'fields': {
            'content': {},
            'title': {}
        }
    }
}

response = es.search(index='articles', body=complex_query)
print(f"Complex Query - Found {response['hits']['total']['value']} documents")
for hit in response['hits']['hits']:
    print(f"The hit is: {hit}")
    print(f"Score: {hit['_score']}, Title: {hit['_source']['title']}, Content: {hit['_source']['content']}")
    print("\t\t\t", "=" * 20)

# Use aggregations to analyze the data.
agg_query = {
    'size': 0,
    'aggs': {
        'popular_tags': {
            'terms': {
                'field': 'tags',
                'size': 10
            }
        },
        'avg_rating': {
            'avg': {
                'field': 'rating'
            }
        },
        'monthly_posts': {
            'date_histogram': {
                'field': 'publish_date',
                'calendar_interval': 'month'
            }
        }
    }
}

response = es.search(index='articles', body=agg_query)
print(f"Average rating: {response['aggregations']['avg_rating']['value']}")
print("\t\t\t", "="*20)

for bucket in response['aggregations']['popular_tags']['buckets']:
    print(f"Tag: {bucket['key']}, Count: {bucket['doc_count']}")
print("\t\t\t", "="*20)

for bucket in response['aggregations']['monthly_posts']['buckets']:
    print(f"Monthly Posts: {bucket['key']}, Count: {bucket['doc_count']}")
print("\t\t\t", "="*20)

es.close()