import csv
import es_helper
import os 

from elasticsearch import Elasticsearch


class EsManagement:
    # ES_HOST = "localhost:9200"
    # USER_NAME = "elastic"
    # PASSWORD = "elsy1995"

    def __init__(self):
        self.es_client = Elasticsearch(['http://localhost:9200'], http_auth=('elastic', 'elsy1995'))
        # self.es_client = Elasticsearch()

    def create_index(self) -> None:
        self.es_client.indices.create(index=es_helper.index_name, ignore=400, body=es_helper.mapping)


    def populate_index(self) -> None:
        with open(es_helper.file_path, newline='') as dataFile:
            reader = csv.DictReader(dataFile)

            doc_counter = 0
            for row in reader:
                body = es_helper.getDocBody(row)
                # print(body)
                self.es_client.index(index=es_helper.index_name, document=body)
                doc_counter = doc_counter + 1


    def getALlData(self):
        res = self.es_client.search(index=es_helper.index_name, query=es_helper.getAllDataSearchQuery(), size=25)
        return es_helper.getData(res)

    def search(self, form_data: dict):
        query = es_helper.getSearchQuery(form_data)
        # print(query)
        res = self.es_client.search(index=es_helper.index_name, query=query, size=25)
        return es_helper.getData(res)

    def searchWithSorting(self, form_data: dict, sort_order: str):
        query = es_helper.getSearchQuery(form_data)
        # print(query)
        res = self.es_client.search(index=es_helper.index_name, query=query, sort=es_helper.getSortList(sort_order),
                                    size=25)
        return es_helper.getData(res)
