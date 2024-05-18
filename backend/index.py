import os

from elasticsearch_dsl import (
    DenseVector, Document, Keyword, Text,
    analyzer, tokenizer, token_filter, connections
)

# TODO: get out very secret default elasticsearch username from ENV
connections.create_connection(hosts=f"http://search:9200", basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD')))


code_hierarchy_analyzer = analyzer(
    'code_hierarchy_analyzer',
    tokenizer=tokenizer(
        'code_hierarchy_tokenizer', 
        type='path_hierarchy',
        delimiter='.',
        replacement='-',
    )
)

name_analyzer = analyzer(
    'name_analyzer',
    filter=[
        'lowercase',
        token_filter(
            'ru_stopword_filter',
            type='stop',
            stopwords='_russian_'
        )
    ],
    tokenizer='standard'
)

class KsrEntry(Document):
    code = Text(
        analyzer=code_hierarchy_analyzer
    )
    okpd2 = Keyword()
    full_code = Keyword()
    type = Keyword() 
    name = Text(
        analyzer=name_analyzer,
        fields={'raw': Keyword()}
    )
    embedding = DenseVector(dims=1024)

    class Index:
        name = 'ksr'

    def save(self, **kwargs): # type: ignore
        if self.okpd2:
            self.full_code = f"{self.okpd2}.{self.code}"
        else:
            self.full_code = self.code
        return super().save(**kwargs)


KsrEntry.init()
