import json

search_fields = {"brand": 10, "name": 10, "categories": 5}

index_name = "electronics"
file_path = "ElectronicsData.csv"
mapping = """
            {
  "mappings": {
    "properties": { 
      "prices":  { "type": "float"  }, 
      "brand":   { "type": "text"  },
      "categories":  { "type": "text"  }, 
      "name":  { "type": "text"  }, 
      "dateAdded":  { "type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss'Z'"  }, 
      "imageURLs":  { "type": "text", "index": false  } 
    }
  }
}
"""


def getDocBody(row) -> str:
    body = {
        "prices": row["prices"],
        "brand": row["brand"],
        "categories": row["categories"],
        "dateAdded": row["dateAdded"],
        "imageURLs": row["imageURLs"],
        # "manufacturer": row["manufacturer"],
        "name": row["name"]
    }
    return json.dumps(body)


def getData(res: dict):
    data_dic_array = []
    data_dic = None
    if isinstance(res, dict):
        if "hits" in res:
            data_dic = res["hits"]
            if "hits" in data_dic:
                data_dic = data_dic["hits"]
                for item in data_dic:
                    data_dic_array.append(item["_source"])
                    # print(item["_source"])
    return data_dic_array


def getAllDataSearchQuery():
    query = {"match_all": {}}


def getSearchQuery(query_param: dict):
    query_template = """{
    "fuzzy": {
      "%s": {
        "value": "%s",
        "fuzziness": "AUTO",
        "max_expansions": 50,
        "prefix_length": 0,
        "transpositions": true,
        "boost": %d
      }
    }},"""
    query = ""
    for key, value in query_param.items():
        boost_value = search_fields[key]
        query = query + query_template % (key, value.lower(), boost_value)
    if not query:
        return getAllDataSearchQuery()
    else:
        query = query[:-1]

    search_query_template = """
                {
                    "bool": {
                      "should": [
                        %s
                      ]
                    }
                  }
                
    """ % query
    query_dict = json.loads(search_query_template)
    return query_dict


def getSortList(sort_order: str):
    sort_list = [{"prices": sort_order}, {"dateAdded": "desc"}, "_score"]
    return sort_list
