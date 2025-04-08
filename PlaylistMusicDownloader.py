import requests
import os

BASE_URL = "http://10.0.0.3:8096/"
HEADERS = {'Authorization': 'MediaBrowser Client="Jellyfin%20Web", Device="Firefox", DeviceId="TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTAuMTU7IHJ2OjEzNS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEzNS4wfDE3NDA1MTgwNTk1NjE1", Version="10.10.6", Token="cd00993a7bfe4b2caccc288aedf170aa"'}

FOLDER_DEST = "/home/alby/MusicExported/"

def downloadFile(fileID,playlistName,fileName, createPlaylistFolder=False):
    url = BASE_URL+"Items/"+fileID+"/Download"
    with requests.get(url, stream=True, headers=HEADERS) as res:
        if(res.status_code==200):
            if(not os.path.isdir(FOLDER_DEST)):
                os.mkdir(FOLDER_DEST)
            
            if(createPlaylistFolder):
                finalPath = FOLDER_DEST + "/" +playlistName
            else:
                finalPath = FOLDER_DEST + "downloaded"
                playlistFile = FOLDER_DEST+"/"+playlistName+".m3u"
                ## create a m3u playlist file
                if(not os.path.exists(playlistFile)):
                    with open(playlistFile,"w") as f:
                        f.write("#test"+"\n")
                with open(playlistFile,"a") as f:
                    f.write("./downloaded/"+fileName+"\n")


            if(not os.path.isdir(finalPath)):
                os.mkdir(finalPath)

            if(not os.path.exists(os.path.join(os.getcwd(), (finalPath), fileName))): #only if not exists
                with open(finalPath+"/"+fileName, 'wb') as f:
                    for chunk in res.iter_content(chunk_size=8192): 
                        f.write(chunk)
                    print("Downloaded "+fileName+" in folder: "+finalPath)
                
        else:
            print("ERROR ON DOWNLOADING THE SONG - fileid: "+fileID)




def getSongsIDFromPlaylist(PlaylistID):
    url = BASE_URL+"Playlists/"+PlaylistID
    res = requests.get(url, headers=HEADERS)
    if(res.status_code==200):
        res = res.json()
        return res["ItemIds"]
    else:
        return []

def getSongMetadata(songID):
    url = BASE_URL+"Items/"+songID
    res = requests.get(url,headers=HEADERS)
    if(res.status_code==200):
        res = res.json()
        fileName= res["MediaSources"][0]["Name"] + "." + res["MediaSources"][0]["Container"]

        return fileName
    else:
        return null

#### 

## for each playlist will be created a folder with the same name containing the songs
def main():
    # cycle thru the playlist, done manually because the API to retrieve automatically is a hell 
    ##  --> http://10.0.0.3:8096/Users/acbf0cef0357403a9a3abb314b67b2a3/Items?SortBy=SortName&SortOrder=Ascending&IncludeItemTypes=Playlist&Recursive=true&Fields=PrimaryImageAspectRatio%2CSortName%2CCanDelete&StartIndex=0

    # key: name of playlist, value: id of playlist
    playlists = dict()
    playlists["chillin"] = "4638cefbb8c256e05192e51aed0f48ec"
    playlists["deep night"] = "959668ac405340c31c34046129b35ac1"
    playlists["energy"] = "3c87f65b5fe53cf74c36219e8425af59"
    playlists["gym"] = "ff8fe24fbc3bd811a9bfccbd3113c7eb"
    playlists["runnin"] = "301709956ac5e8a3d051797c2605fb1d"
    playlists["stuff"] = "1d64b9eab05f552af44fdb8c3efe8353"

    for p in playlists:
        print(p)
        songs_id = getSongsIDFromPlaylist(playlists[p])
        for s in songs_id:
            downloadFile(s, p, getSongMetadata(s))

    


main()