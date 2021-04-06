#!/usr/bin/env python3
from urllib import request, parse, error
import json
import sys
import os.path

def save_json(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

def get_user(token):
    headers = {"Content-Type": "application/json", "Authorization" : "Bearer " + token}
    req = request.Request(url='https://api.spotify.com/v1/me', headers= headers)
    with request.urlopen(req) as f:
        user = f.read().decode('utf-8')
        juser = json.loads(user)
        return juser

def get_users_playlists(token):
    headers = {"Content-Type": "application/json", "Authorization" : "Bearer " + token}
    req = request.Request(url='https://api.spotify.com/v1/me/playlists', headers= headers)
    r = { 'playlists' : [] }
    with request.urlopen(req) as f:
        pls = f.read().decode('utf-8')
        jpls = json.loads(pls)
        for item in jpls['items']:
            r['playlists'].append({ 'id' : item['id'],
                'name' : item['name'],
                'description' : item['description'],
                'items_href' : item['tracks']['href'],
                'items' : get_playlist_items(item['id'], token)
            })
    return r

def get_playlist_items(playlist_id, token):
    headers = {"Content-Type": "application/json", "Authorization" : "Bearer " + token}
    req = request.Request(url='https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks?fields=items(track.id)', headers = headers)
    with request.urlopen(req) as f:
        pl = f.read().decode('utf-8')
        jpl = json.loads(pl)
        r = []
        for item in jpl['items']:
            r.append(item['track']['id'])
        return r

def create_playlist(name, description, public, user_id, token):
    headers = {"Content-Type": "application/json", "Authorization" : "Bearer " + token}

    data = { "name": name, "description": description, "public": public }
    data = json.dumps(data)
    data = data.encode()

    req = request.Request(url='https://api.spotify.com/v1/users/' + user_id + '/playlists', method="POST", headers = headers)
    with request.urlopen(req, data=data) as f:
        pl = f.read().decode('utf-8')
        jpl = json.loads(pl)
        id = jpl['id']
        return id
    
def add_items_to_playlist(playlist_id, items, token):
    headers = {"Content-Type": "application/json", "Authorization" : "Bearer " + token}
    
    if len(items) == 0:
        return
    
    uris = "spotify:track:" + ",spotify:track:".join(items)
    req = request.Request(url='https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks?uris=' + uris, method="POST", headers = headers)
    r = request.urlopen(req).read()
    return r

def import_playlists(file_name, token):
    if not os.path.isfile(file_name):
        raise Exception('El fichero no existe')

    user_id = get_user(token)['id']

    with open(file_name, 'r') as readfile:
        playlists = readfile.read()
        jplaylists = json.loads(playlists)

    for pl in jplaylists['playlists']:
        new_pl_id = create_playlist(pl['name'], pl['description'], True, user_id, token)
        add_items_to_playlist(new_pl_id, pl['items'], token)


import argparse
parser = argparse.ArgumentParser(description='Import and export of Spotify playlists')

subparsers = parser.add_subparsers(dest='tool', help="Spotify tool")
subparsers.required = True

ex = subparsers.add_parser('export', help='Export playlists')
ex.add_argument('--token', metavar='token', type=str, dest='token', required=True, help='API token https://developer.spotify.com/console/get-current-user-playlists/')
ex.add_argument('--file', metavar='file', type=str, dest='file_name', required=True, help='File name')

imp = subparsers.add_parser('import', help='Import playlists')
imp.add_argument('--token', metavar='token', type=str, dest='token', required=True, help='API token. Import --> https://developer.spotify.com/console/post-playlist-tracks/')
imp.add_argument('--file', metavar='file', type=str, dest='file_name', required=True, help='File name')

imp = subparsers.add_parser('user', help='User info')
imp.add_argument('--token', metavar='token', type=str, dest='token', required=True, help='API token. Import --> https://developer.spotify.com/console/')

args = parser.parse_args()
if args.tool == "export":
    try:
        pls =  get_users_playlists(args.token)
        # Guarda las playlists
        save_json(args.file_name, pls)
    except error.HTTPError as err:
        print(err.code, err.reason);
        print(err.read())

elif args.tool == "import":
    try:
        import_playlists(args.file_name, args.token)
    except error.HTTPError as err:
        print(err.code, err.reason);
        print(err.read())
elif args.tool == "user":
    try:
        print(get_user(args.token))
    except error.HTTPError as err:
        print(err.code, err.reason);
        print(err.read())
else:
    print("Parameters error")



