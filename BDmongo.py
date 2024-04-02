import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["SD2024_projet"]


######################
#fonctions pour artiste
def check_artist_in_db(artist):
    collection = db["GAMMA_artists"]
    artist_info_from_db = collection.find_one({"name": artist})
    return artist_info_from_db

def insert_artist_info_into_db(artist_info):

    collection = db["GAMMA_artists"]

    
    existing_document = collection.find_one({"name": artist_info["name"]})

    if existing_document:
        print("Le document existe déjà dans la collection GAMMA_artists. Pas besoin d'insérer à nouveau.")
    else:
        
        collection.insert_one(artist_info)
        print("Données de l'artiste insérées avec succès dans la collection GAMMA_artists.")
#####################
#fonctions pour tag
def check_tag_in_db(tag_name):
    collection = db["GAMMA_tags"]
    tag_info_from_db = collection.find_one({"name": tag_name})
    return tag_info_from_db

def insert_tag_info_into_db(tag_info):
    collection = db["GAMMA_tags"]

    existing_document = collection.find_one({"name": tag_info["name"]})

    if existing_document:
        print("Le document existe déjà dans la collection GAMMA_tags. Pas besoin d'insérer à nouveau.")
    else:
        collection.insert_one(tag_info)
        print("Données du tag insérées avec succès dans la collection GAMMA_tags.")

######################
#fonctions pour albums 
def check_album_in_db(artist_name, album_name):
    collection = db["GAMMA_albumes"]
    album_info_from_db = collection.find_one({"artist": artist_name, "album": album_name})
    return album_info_from_db


def insert_album_info_into_db(album_info):
    collection = db["GAMMA_albums"]

    existing_document = collection.find_one({"name": album_info["name"],"artist": album_info["artist"]})
    if existing_document:
        print("Le document existe déjà dans la collection GAMMA_albums. Pas besoin d'insérer à nouveau.")
    else:
        collection.insert_one(album_info)
        print("Données de l'album insérées avec succès dans la collection GAMMA_albums.")
