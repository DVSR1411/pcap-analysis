from elasticsearch import Elasticsearch

es = Elasticsearch("https://localhost:9200", 
                   api_key='RS1BMEZKMEJVWHBLdDhsU21KbjU6cG9Cb2kxel9STmVrS1M4NjM3dlhIdw==',
                   verify_certs=False)

print(es.cluster.health())