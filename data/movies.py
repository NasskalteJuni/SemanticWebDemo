from pymongo import MongoClient
from bson.objectid import ObjectId
from pathlib import Path
import pandas as pd


file = str(Path(__file__).parent.resolve())+'/movies_metadata.csv'
db_name = 'moviedb'
db_connection_string = 'mongodb://root:sparql_and_rdf@db:27017/'
movie_collection = 'movie'

client = MongoClient(db_connection_string)
db = client[db_name]
collection = db[movie_collection]
df = pd.read_csv(file, index_col=None, na_values=['NA'], low_memory=False)
df.reset_index(inplace=True)
data_dict = df.to_dict('records')
collection.insert_many(data_dict)


def _map_object_id_to_id(obj):
    obj['uuid'] = str(obj['_id'])
    del obj['_id']
    return obj


def get_all(limit=-1):
    selection = {}
    if limit >= 0:
        selection['limit'] = limit
    movies = list(collection.find(selection))
    for movie in movies:
        _map_object_id_to_id(movie)
    return movies


def get_by_title(movie_title):
    return _map_object_id_to_id(collection.find_one({'title': movie_title}))


def get_by_id(movie_id):
    return _map_object_id_to_id(collection.find_one({'id': movie_id}))


def get_by_uuid(movie_uuid):
    return _map_object_id_to_id(collection.find_one({'_id': ObjectId(movie_uuid)}))
