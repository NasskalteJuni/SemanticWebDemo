import sys
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from IPython.display import display, Markdown

endpoint_url = "https://query.wikidata.org/sparql"


def query(q):
    user_agent = "jupyter-notebook-/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def table(result):
    vars = result['head']['vars']
    thead = "| "
    for th in vars:
        thead += th+" |"
    thead += "\n|"
    for th in vars:
        thead += " --- |"
    thead += "\n"
    tbody = ""
    for tr in result['results']['bindings']:
        tbody += "| "
        for td in vars:
            tbody += tr[td]['value'] + " |"
        tbody += "\n"
    display(Markdown(thead+tbody))
    return "showing "+str(len(result['results']['bindings']))+" results"


def entity_to_json(entity_tag):
    url = 'https://www.wikidata.org/wiki/Special:EntityData/'+entity_tag+'.json'
    return requests.get(url).json()


def data(result):
    entities = result['results']['bindings']
    mapped_to_flat_object = []
    for entity in entities:
        flat_object = {}
        for attr in entity:
            flat_object[attr] = entity[attr]['value']
        mapped_to_flat_object.append(flat_object)

    return mapped_to_flat_object
