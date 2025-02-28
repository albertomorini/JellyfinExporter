import requests
# from pydub import AudioSegment

BASE_URL = "http://10.0.0.3:8096/"
HEADERS = {'Authorization': 'MediaBrowser Client="Jellyfin%20Web", Device="Firefox", DeviceId="TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTAuMTU7IHJ2OjEzNS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEzNS4wfDE3NDA1MTgwNTk1NjE1", Version="10.10.6", Token=""'}

FOLDER_DEST = "./downloaded/"

def downloadFile(fileID,destFolder,fileName):
    url = BASE_URL+"Items/"+fileID+"/Download"
    with requests.get(url, stream=True, headers=HEADERS) as res:
        if(res.status_code==200):
            #TODO: better parameters for folders and children folders
            with open(FOLDER_DEST+"/"+destFolder+"/"+fileName, 'wb') as f:
                for chunk in res.iter_content(chunk_size=8192): 
                    f.write(chunk)
                print("Downloaded "+fileName+" in folder: "+destFolder)
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


def main():
    #TODO: a for to cycle on the indicated playlists, for now download single

    songs_id = getSongsIDFromPlaylist("1d64b9eab05f552af44fdb8c3efe8353")
    for s in songs_id:
        downloadFile(s, "stuff", getSongMetadata(s))

main()

def getInfoSong(fileID):
    pass

# download_file("http://10.0.0.3:8096/Items/68a3a384293fe8359461c907a046ef27/Download")


