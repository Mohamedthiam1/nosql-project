from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.entertainment
films_collection = db.films

def get_movies():
    return list(films_collection.find()) 