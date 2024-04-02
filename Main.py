import pymongo
import requests
import json
from flask import Flask, redirect, render_template, request, url_for
from BDmongo import insert_artist_info_into_db, check_artist_in_db, check_tag_in_db, insert_tag_info_into_db, check_album_in_db, insert_album_info_into_db
#API key
XI_API_KEY = "43fd3e0df818d835e6b144ad21a7765a"
#Url pour mongo

import requests

def get_info_charttags(api_key, chart_type, page=1, limit=10):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': f'chart.gettop{chart_type}',
        'api_key': api_key,
        'format': 'json',
        'page': page,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    tags = data.get('tags', {}).get('tag', [])
    tag_info_list = []
    for index, tag in enumerate(tags, start=1):
        name = tag.get('name')
        reach = tag.get('reach')
        wiki = tag.get('wiki', {})
        summary = wiki.get('summary') if 'summary' in wiki else None
        tag_info = {
            'index': index,
            'name': name,
            'reach': reach,
            'summary': summary
        }
        tag_info_list.append(tag_info)
    return tag_info_list


def get_info_chartartist(api_key, chart_type, page=1, limit=10):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': f'chart.gettop{chart_type}',
        'api_key': api_key,
        'format': 'json',
        'page': page,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    artists = data.get('artists', {}).get('artist', [])
    artist_info_list = []
    for index, artist in enumerate(artists, start=1):
        name = artist.get('name')
        playcount = artist.get('playcount')
        listeners = artist.get('listeners')
        artist_info = {
            'index': index,
            'name': name,
            'playcount': playcount,
            'listeners': listeners
        }
        artist_info_list.append(artist_info)
    return artist_info_list


def get_info_chart(api_key, chart_type, page=1, limit=10):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': f'chart.gettop{chart_type}',
        'api_key': api_key,
        'format': 'json',
        'page': page,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    tracks = data.get('tracks', {}).get('track', [])
    track_info_list = []
    for track in tracks:
        track_info = {
            'name': track.get('name'),
            'playcount': track.get('playcount'),
            'listeners': track.get('listeners'),
            'artist': track.get('artist', {}).get('name')
        }
        track_info_list.append(track_info)
    return track_info_list
    

def get_tag_info(api_key, tag):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'tag.getinfo',
        'tag': tag,
        'api_key': api_key,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    tag_info = data.get('tag', {})
    tag_result = {
        'name': tag_info.get('name'),
        'total': tag_info.get('total'),
        'reach': tag_info.get('reach'),
        'tagging': tag_info.get('tagging'),
        'streamable': tag_info.get('streamable'),
        'wiki': {
            'summary': tag_info.get('wiki', {}).get('summary'),
            'content': tag_info.get('wiki', {}).get('content')
        }
    }
    
    return tag_result




def get_artist_info(api_key, artist):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'artist.getinfo',
        'artist': artist,
        'api_key': api_key,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    data = response.json()

    artist_info = {
        'name': data['artist']['name'],
        'similar_artists': []
    }

    similar_artists = data['artist'].get('similar', {}).get('artist', [])
    for similar_artist in similar_artists:
        similar_artist_info = {
            'name': similar_artist['name']
        }
        artist_info['similar_artists'].append(similar_artist_info)

    return artist_info



def get_album_info(api_key, artist, album):
    params = {
        'method': 'album.getinfo',
        'api_key': api_key,
        'artist': artist,
        'album': album,
        'format': 'json'
    }
    response = requests.get('http://ws.audioscrobbler.com/2.0/', params=params)
    data = response.json()
    album_data = data.get('album', {})
    album_info = {
        'name' : album_data.get('name'),
        'artist' : album_data.get('artist'),
        'listeners': album_data.get('listeners'),
        'release_date': album_data.get('releasedate'),
        'playcount': album_data.get('playcount'),
        'tracks': []
    }
    tracks = album_data.get('tracks', {}).get('track', [])
    for track in tracks:
        track_info = {
            'name': track.get('name'),
            'duration': track.get('duration'),
            'streamable': track.get('streamable'),
            'artist': track.get('artist', {}).get('name')  
        }
        album_info['tracks'].append(track_info)
        
    return album_info






app = Flask(__name__, static_folder='templates/', static_url_path='')


@app.route('/') 
def home():
    message = request.args.get('message')  
    return render_template('Lastfm.html', message=message)
@app.route('/t')
def t():
    return render_template('Tag.html')
@app.route('/a') 
def a():
    return render_template('Artiste.html')

@app.route('/c',methods=['GET'])
def c():
    track_info_list = get_info_chart(XI_API_KEY, 'tracks')
    
    tracks_with_index = [(index + 1, track_info) for index, track_info in enumerate(track_info_list)]

    return render_template('chart_tracks.html',tracks_with_index=tracks_with_index)

@app.route('/c2',methods=['GET'])
def c2():
    track_info_list = get_info_chartartist(XI_API_KEY, 'artists')
    print(track_info_list)
    tracks_with_index = [(index + 1, track_info) for index, track_info in enumerate(track_info_list)]

    return render_template('chart_artist.html',tracks_with_index=tracks_with_index)

@app.route('/c3',methods=['GET'])
def c3():
    track_info_list = get_info_charttags(XI_API_KEY, 'tags')
    print(track_info_list)
    tracks_with_index = [(index + 1, track_info) for index, track_info in enumerate(track_info_list)]

    return render_template('chart_tags.html',tracks_with_index=tracks_with_index)

@app.route('/Artiste', methods=['GET'])
def Artiste():
    artist_name = request.args.get('artist') 
    info = check_artist_in_db(artist_name)
    if info : 
        print("dans la base")
        return render_template('Artiste.html', artist_info=info)
    else:
        artist_info = get_artist_info(XI_API_KEY, artist_name)
        insert_artist_info_into_db(artist_info)
        print("pas dans la base")
        return render_template('Artiste.html', artist_info=artist_info)

@app.route('/tag', methods=['GET'])
def tag_info():
    tag = request.args.get('tag')
    info = check_tag_in_db(tag)
    if info: 
        print("dans la base")
        return render_template('Tag.html', tag_info=info)
    else:
        print("pas dans la base")
        tag_info = get_tag_info(XI_API_KEY, tag)
        insert_tag_info_into_db(tag_info)
        return render_template('Tag.html', tag_info=tag_info)



@app.route('/result', methods=['GET'])
def result():
    artist = request.args.get('artist')
    album = request.args.get('album')
    info = check_album_in_db(artist,album)
    if info: 
        print("dans la base")
        return render_template('Lastfm.html',message=info)
    else: 
        print("pas dans la base")
        response = get_album_info(XI_API_KEY, artist, album)
        insert_album_info_into_db(response)
        return render_template('Lastfm.html',message=response)




if __name__ == '__main__':
      app.run(host='0.0.0.0')
      app.run(debug=True)