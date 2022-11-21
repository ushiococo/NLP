try:
    from elasticsearch import Elasticsearch, helpers
    import pandas as pd
    import json
    from ast import literal_eval
    from tqdm import tqdm
    from datetime import datetime
    import os
    import sys
    import numpy as np
    import csv
    from py2neo import Node, Graph,Relationship, NodeMatcher
    import ast
    print("imports loaded....")
except Exception as e:
    print("some modules are missing{}".format(e))

now = datetime.now()
es_username= "elastic"
es_password = "sV6Z4M-ExtFR7MiP8UM61"
es = Elasticsearch([{"host": "127.0.0.1", "port": 9200,"scheme": "http"}],basic_auth=(str(es_username), str(es_password)))

# Multiple nodes via dictionary
#es = Elasticsearch([
 #   {"scheme": "http", "host": "localhost", "port": 9200},
  #  {"scheme": "http", "host": "localhost", "port": 9201},
#])


if es.ping():
    print("Successful connection to the server")
    Elasticsearch.info(es)
    print(Elasticsearch.info(es).values())
else:
    print("failed to connect to the server")

print("choose option 1-2 \n 1: Push data into Elasticsearch \n 2: Plotting Knowledge Graph")
user_input = int(input("Enter 1 or 2 "))

if user_input == 1:
    df = pd.read_csv("best2.csv")
    #Defining the settings for this ingestion process: set field limits
    params = {
        "settings": {
            "index.mapping.total_fields.limit": 50000000000000,  # currently set to overlimit
        },
        "mappings": {
            "properties": {
                "_ID": {
                    "type": "integer"
                },
            }
        }
    }

    # importing data to elasticsearch
    # print(df["ID"])
    es.indices.create(index='master-index', ignore=4000, **params)
    for index, row in df.iterrows():
        # print(row)
        d = {}
        # d["ID"] = row["ID"]
        # d["client"] = row["client"]
        # d["hostname"] = row["hostname"]
        # d["Record"] = row["Record"]
        # d["alias_list"] = row["alias_list"]
        # d["address_list"] = row["address_list"]
        # print(d["address_list"])
        # d["content-length"] = row["content-length"]
        # d["url"] = row["url"]
        # d["User-Agent"] = row["User-Agent"]
        # d["datetime"] = row["datetime"]
        # d["HTTPMethods"] = row["HTTPMethods"]
        # d["HTTPVersion"] = row["HTTPVersion"]

        # address_list	content-length	url	User-Agent	datetime	HTTPMethods	HTTPVersion
        # print((df.iloc[index,row[c]])

        for c in df:
            if not pd.isnull(row[c]):
                d[c] =row[c]

        ingest_content = {
            "_id": str(row['ID']),
            "_source": d
        }
        print(d)
        ingest_content = [ingest_content]

        helpers.bulk(es, ingest_content, index='master-index')
    # print(df)
if user_input == 2:
    now = datetime.now()
    es_username = "elastic"
    #sV6Z4M-ExtFR7MiP8UM6#
    #CtS-1ITidsWKdU7rzCMt#
    es_password = "sV6Z4M-ExtFR7MiP8UM6"
    es = Elasticsearch([{"host": "127.0.0.1", "port": 9200, "scheme": "http"}],
                       basic_auth=(str(es_username), str(es_password)))

    if es.ping():
        print("Successful connection to the server")
        Elasticsearch.info(es)
        print(Elasticsearch.info(es).values())
    else:
        print("failed to connect to the server")
    port = input("Enter Neo4j DB Port: ")
    user = input("Enter Neo4j DB Username: ")
    #password: chairwoman-tumbles-coordinators
    # neSzjRHBf4LtF_gwQhKQBmms8fToMhqlQwbn4LzAAuw
    pwsd = input("Enter Neo4j DB Password ")
    # 54.152.13.23
    # 174.129.148.41
    try:
        neo4j_instance = Graph('bolt://localhost:' + port, auth=(user, pwsd))
        print("Success! Connected to Neo4j Database")
    except Exception as e:
        print('Error: Could not connect to the Neo4j Database')
        raise SystemExit(e)
    nodes_matcher = NodeMatcher(neo4j_instance)
    tx = neo4j_instance.begin()
    entity1 = nodes_matcher.match('ISP', name='ISP').first()
    if not entity1:
        entity1 = Node('ISP', name='ISP')
        tx.create(entity1)
        neo4j_instance.commit(tx)
    tx = neo4j_instance.begin()
    entity2 = nodes_matcher.match('Server', name='Server').first()
    if not entity2:
        entity2 = Node('Server', name='Server')
        tx.create(entity2)
        neo4j_instance.commit(tx)
    qtx = neo4j_instance.begin()
    edge = Relationship(entity2, "connect to", entity1)
    qtx.create(edge)
    neo4j_instance.commit(qtx)
    tx = neo4j_instance.begin()
    entity3 = nodes_matcher.match('Network Logs', name='Network Logs').first()
    if not entity3:
        entity3 = Node('Network Logs', name='Network Logs')
        tx.create(entity3)
        neo4j_instance.commit(tx)
    qtx = neo4j_instance.begin()
    edge = Relationship(entity2, "contains info", entity3)
    qtx.create(edge)
    neo4j_instance.commit(qtx)
    tx = neo4j_instance.begin()
    entity4 = nodes_matcher.match('Connection Details', name='Connection Details').first()
    if not entity4:
        entity4 = Node('Connection Details', name='Connection Details')
        tx.create(entity4)
        neo4j_instance.commit(tx)
    qtx = neo4j_instance.begin()
    edge = Relationship(entity2, "contains info", entity4)
    qtx.create(edge)
    neo4j_instance.commit(qtx)
    tx = neo4j_instance.begin()
    entity5 = nodes_matcher.match('Browser', name='Browser').first()
    if not entity5:
        entity5 = Node('Browser', name='Browser')
        tx.create(entity5)
        neo4j_instance.commit(tx)
    qtx = neo4j_instance.begin()
    edge = Relationship(entity3, "has the info", entity5)
    qtx.create(edge)
    neo4j_instance.commit(qtx)
    tx = neo4j_instance.begin()
    entity6 = nodes_matcher.match('Computer', name='Computer').first()
    if not entity6:
        entity6 = Node('Computer', name='Computer')
        tx.create(entity6)
        neo4j_instance.commit(tx)
    qtx = neo4j_instance.begin()
    edge = Relationship(entity4, "has the info of connection", entity6)
    qtx.create(edge)
    neo4j_instance.commit(qtx)

    query = {
        "track_total_hits": True,
        "query": {
            "match_all": {}
        }
    }

    resp = es.search(index="master-index", body=query, size=10000)
    print("Got %d Hits from Elasticsearch:" % resp['hits']['total']['value'])
    data = []
    for hit in resp['hits']['hits']:
        data.append(hit["_source"])

    print("# pulling data from elasticsearch")
    print(len(data))
    list = []
    for i in range(1,1000):
        list.append(i * 100)
        print(list)
    count =0
    for row in data:
            # print(index)
            count+=1
            print(count)
            if i in list:
                neo4j_instance = Graph('bolt://localhost:' + port, auth=(user, pwsd))
            tx = neo4j_instance.begin()
            h = nodes_matcher.match('Hostname', name=row['hostname']).first()

            if not h:
                h = Node('Hostname', name=row['hostname'])
                tx.create(h)
                neo4j_instance.commit(tx)
            qtx = neo4j_instance.begin()
            edge = Relationship(entity6, "hostname", h)
            qtx.create(edge)
            neo4j_instance.commit(qtx)
            tx = neo4j_instance.begin()
            i = nodes_matcher.match('IP_Address', name=row['ipAddress']).first()
            if not i:
                i = Node('IP_Address', name=row['ipAddress'])
                tx.create(i)
                neo4j_instance.commit(tx)
            qtx = neo4j_instance.begin()
            edge = Relationship(entity5, "has the info of", i)
            qtx.create(edge)
            neo4j_instance.commit(qtx)
            qtx = neo4j_instance.begin()
            edge = Relationship(entity6, "has the info of", i)
            qtx.create(edge)
            neo4j_instance.commit(qtx)
            qtx = neo4j_instance.begin()
            edge = Relationship(h, "uses", i)
            qtx.create(edge)
            neo4j_instance.commit(qtx)
            tx = neo4j_instance.begin()
            b = nodes_matcher.match('Browser_Agent', name=row['User-Agent']).first()
            if not b:
                b = Node('Browser_Agent', name=row['User-Agent'])
                tx.create(b)
                neo4j_instance.commit(tx)
            qtx = neo4j_instance.begin()
            edge = Relationship(entity5, "user agent", b)
            qtx.create(edge)
            neo4j_instance.commit(qtx)
            tx = neo4j_instance.begin()
            v = nodes_matcher.match('HTTP_Version', name=row['HTTPVersion']).first()
            if not v:
                v = Node('HTTP_Version', name=row['HTTPVersion'])
                tx.create(v)
                neo4j_instance.commit(tx)
            qtx = neo4j_instance.begin()
            edge = Relationship(b, "uses", v)
            qtx.create(edge)
            neo4j_instance.commit(qtx)
            tx = neo4j_instance.begin()
            s = nodes_matcher.match('HTTP_Status', name=row['HTTPMethods']).first()
            if not s:
                s = Node('HTTP_Status', name=row['HTTPMethods'])
                tx.create(s)
                neo4j_instance.commit(tx)
            qtx = neo4j_instance.begin()
            edge = Relationship(b, "has status", s)
            qtx.create(edge)
            neo4j_instance.commit(qtx)
            tx = neo4j_instance.begin()
            u = nodes_matcher.match('URL', name=row['url']).first()
            if not u:
                u = Node('URL', name=row['url'])
                tx.create(u)
                neo4j_instance.commit(tx)
            qtx = neo4j_instance.begin()
            edge = Relationship(b, "access", u)
            qtx.create(edge)
            neo4j_instance.commit(qtx)


