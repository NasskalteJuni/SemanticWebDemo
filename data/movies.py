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


def _load_from_csv(csv_file):
    df = pd.read_csv(csv_file, index_col=None, na_values=['NA'], low_memory=False)
    df.reset_index(inplace=True)
    records = df.to_dict('records')
    for record in records:
        try:
            if 'belongs_to_collection' in record and isinstance(record['belongs_to_collection'], str):
                record['belongs_to_collection'] = eval(record['belongs_to_collection']) or None
                if record['belongs_to_collection']:
                    record['belongs_to_collection'] = record['belongs_to_collection']['name']
            else:
                record['belongs_to_collection'] = None

            if 'genres' in record and isinstance(record['production_companies'], str):
                record['genres'] = eval(record['genres'])
                record['genres'] = [genre['name'] for genre in record['genres']]

            if 'production_companies' in record and isinstance(record['production_companies'], str):
                record['production_companies'] = eval(record['production_companies']) or []
                record['production_companies'] = [company['name'] for company in record['production_companies']]

            if 'production_countries' in record and isinstance(record['production_countries'], str):
                record['production_countries'] = eval(record['production_countries']) or []
                record['production_countries'] = [country['name'] for country in record['production_countries']]

            if 'spoken_languages' in record and isinstance(record['spoken_languages'], str):
                record['spoken_languages'] = eval(record['spoken_languages']) or []
                record['spoken_languages'] = [language['iso_639_1'] for language in record['spoken_languages']]
        except TypeError:
            pass

    return records


def _map_object_id_to_id(obj):
    obj['uuid'] = str(obj['_id'])
    del obj['_id']
    return obj


def get_all(limit=-1):
    if limit >= 0:
        movies = list(collection.find().limit(limit))
    else:
        movies = list(collection.find())
    for movie in movies:
        _map_object_id_to_id(movie)
    return movies


def get_by_title(movie_title):
    return _map_object_id_to_id(collection.find_one({'title': movie_title}))


def get_by_id(movie_id):
    return _map_object_id_to_id(collection.find_one({'id': movie_id}))


def get_by_uuid(movie_uuid):
    return _map_object_id_to_id(collection.find_one({'_id': ObjectId(movie_uuid)}))


def add_data_by_title(movie_id, data):
    return collection.update_one({"title": movie_id}, {"$set": data})


data_dict = _load_from_csv(file)
collection.insert_many(data_dict)
