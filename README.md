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

optional arguments:
  -h, --help            show this help message and exit
```
## Get tokens
https://developer.spotify.com/console

## Export to playlists.json
```
spotify-tools.py import --token "mytoken" --file playlists.json
```


## Import from playlists.json
```
spotify-tools.py import --token "mytoken" --file playlists.json
```
