from elasticsearch import Elasticsearch
from os import environ

# es = Elasticsearch(
#         environ.get('ELASTIC_URL'),
#         basic_auth=(environ.get('ELASTIC_USER'), environ.get('ELASTIC_PASSWORD'))
#     )
es = Elasticsearch(environ.get('ELASTIC_URL'))
