from elasticsearch_dsl import Search, connections
import os

connections.create_connection(hosts=f"http://search:9200", basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD')))

def prefiltered_search(haystack: list[str], needle: str):
    print(haystack)
    print(type(haystack))


    # search = Search(using=connections.get_connection(), index='ksr')
    # search = search.filter("term", type='ресурс')
    # search = search.filter("terms", name=haystack)

    search = (
        Search(using=connections.get_connection(), index='ksr')
            #.filter("term", type='ресурс')
            .filter("term", name_raw='Листы хризотилцементные волнистые, профиль 40/150, 8-волновые, толщина 5,2 мм')
            # .query('match', name=needle)
    )
    
    response = search.execute()
    
    print(response)
    print(len(response))
    for resp in response:
        print(resp['name'])
    return response['hits']['hits'][0]['_source'], response['hits']['max_score']
