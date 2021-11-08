# spotify-tools
Spotify tools to import and export playlists from one user to another user

```
usage: spotify-tools.py [-h] {export,import,user} ...

Import and export of Spotify playlists

positional arguments:
  {export,import,user}  Spotify tool
    export              Export playlists
    import              Import playlists
    user                User info
    merge               Merge two playlists
    get_following_artist_ids
                        Get followed artist ids
    add_following_artist_ids
                        Add followed artist ids
optional arguments:
  -h, --help            show this help message and exit
```
## Get tokens
https://developer.spotify.com/console

## Export to playlists.json
```
  --token token  API token https://developer.spotify.com/console/get-current-user-playlists/
  --file file    File name
```

```
$ spotify-tools.py import --token "mytoken" --file playlists.json
```


## Import from playlists.json
```
  --token token  API token. Import --> https://developer.spotify.com/console/post-playlist-tracks/
  --file file    File name
```

```
$ spotify-tools.py import --token "mytoken" --file playlists.json
```

## Merge to playlists in a new playlist
```
usage: spotify-tools.py merge [-h] --token token --playlist_id_1 playlist id 1
                              --playlist_id_2 playlist id 2 --name playlist
                              name

optional arguments:
  -h, --help            show this help message and exit
  --token token         API token. Import -->
                        https://developer.spotify.com/console/post-playlist-
                        tracks/
  --playlist_id_1 playlist id 1
                        Id of the first Playlist to merge
  --playlist_id_2 playlist id 2
                        Id of the second Playlist to merge
  --name playlist name  Name of the playlist
 ```
## Get following artist ids
```
usage: spotify-tools.py get_following_artist_ids [-h] --token token

optional arguments:
  -h, --help     show this help message and exit
  --token token  API token --> https://developer.spotify.com/console/get-
                 following/
```

## Add following artist ids
```
usage: spotify-tools.py add_following_artist_ids [-h] --token token --ids ids

optional arguments:
  -h, --help     show this help message and exit
  --token token  API token --> https://developer.spotify.com/console/put-
                 following/
  --ids ids      Comma separated ids of artists
```

