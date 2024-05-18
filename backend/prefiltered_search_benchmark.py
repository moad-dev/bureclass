from elasticsearch_dsl import Search, connections
import os

connections.create_connection(hosts=f"http://search:9200", basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD')))

def prefiltered_search(haystack: list[str], needle: str):
    search = (
        Search(using=connections.get_connection(), index='ksr')
            .filter("term", type='ресурс')
            .filter("terms", name=haystack)
            .query('match', title=needle)
    )
    
    response = search.execute()

    return response['hits']['hits']['_source'], response['hits']['max_score']
