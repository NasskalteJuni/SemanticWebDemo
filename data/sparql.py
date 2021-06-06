import sys
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from IPython.display import display, HTML

endpoint_url = "https://query.wikidata.org/sparql"


def query(q):
    user_agent = "jupyter-notebook-/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def table(result):
    return display(HTML(_table(result)))


def _table(result):
    if 'head' in result and 'vars' in result['head']:
        rendered = _sparql_result_to_table(result)
    elif isinstance(result, dict):
        rendered = _json_dict_to_table(result)
    elif isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
        rendered = _list_of_json_dict_to_table(result)
    else:
        rendered = str(result)
    return rendered


def _list_of_json_dict_to_table(json_list):
    columns = set()
    for result in json_list:
        for key in result:
            columns.add(key)

    thead = "<thead><tr>"
    for column in columns:
        thead += "<th>" + column + "</th>"
    thead += "</tr></thead>"

    tbody = "<tbody>"
    for result in json_list:
        tbody += "<tr>"
        for column in columns:
            value = result[column] if column in result else ""
            value = value if value is not None else ""
            if isinstance(value, list) or isinstance(value, dict):
                value = _table(value)
            else:
                value = value if value is not None else ""
            tbody += "<td>" + str(value) + "</td>"
        tbody += "</tr>"
    tbody += "</tbody>"

    return "<table>"+thead+tbody+"</tbody>"


def _json_dict_to_table(json):
    thead = "<thead><tr><th> Key </th><th> Value </th></tr></thead>"

    tbody = "<tbody>"
    for key, value in json.items():
        if isinstance(value, list) or isinstance(value, dict):
            value = _table(value)
        else:
            value = value if value is not None else ""
        tbody += "<tr><td>" + str(key) + "</td><td>" + str(value) + "</td></tr>"
    tbody += "</tbody>"

    return "<table>" + thead + tbody + "</table>"


def _sparql_result_to_table(result):
    vars = result['head']['vars']

    thead = "<thead><tr>"
    for th in vars:
        thead += "<th>" + th + "</th>"
    thead += "</tr></thead>"

    tbody = "<tbody>"
    for tr in result['results']['bindings']:
        tbody += "<tr>"
        for td in vars:
            value = tr[td]['value'] if tr[td]['value'] is not None else ""
            tbody += "<td>" + str(value) + "</td>"
        tbody += "</tr>"
    tbody += "</tbody>"

    return "<table>"+thead+tbody+"</table>"


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
