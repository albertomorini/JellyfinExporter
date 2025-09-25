import requests
import os
import json
import sys
########################################################################################
########################################################################################

BASE_URL = "http://10.0.0.3:8096/"
HEADERS = {'Authorization': 'MediaBrowser Client="Jellyfin Web", Device="Firefox", DeviceId="TW96aWxsYS81LjAgKFgxMTsgTGludXggeDg2XzY0OyBydjoxNDIuMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC8xNDIuMHwxNzU2NTQ3NzI3MTQ2", Version="10.10.7", Token="9b2c5c1a83d5448981ab9cfcf89eadf5"'}

FOLDER_DEST = "/home/alby/MusicExported/"

########################################################################################


def downloadFile(register,fileID,playlistName,fileName, createPlaylistFolder=False,deleteOld=False):
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
                with open(playlistFile,"a") as f: ## append file name to create the playlist
                    f.write("./downloaded/"+fileName+"\n")


            if(not os.path.isdir(finalPath)): ## make final dir to store songs
                os.mkdir(finalPath)

            # if(not os.path.exists(os.path.join(os.getcwd(), (finalPath), fileName))): #only if not exists
            if(fileID not in register["known_songs"]): # if not exists store the song
                with open(finalPath+"/"+fileName, 'wb') as f:
                    for chunk in res.iter_content(chunk_size=8192): 
                        f.write(chunk)
                    print("Downloaded "+fileName+" in folder: "+finalPath)
            
            elif(deleteOld): #if song already stored and justNewMusic is enabled, delete the old ones
                try:
                    print("Deleting "+fileName)
                    os.remove(finalPath+"/"+fileName)
                except OSError as e:
                    pass # print(e)

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

########################################################################################


## LOAD THE REGISTER OF SONGS ALREADY DOWNLOADED
def LoadRegister():
    try:
        config_file = open("./register.json",'r')
        return json.loads(config_file.read())
    except Exception as e:
        initRegister = dict()
        initRegister["known_songs"] = []
        StoreRegister(initRegister)
        return initRegister

## STORE THE JSON 
def StoreRegister(register):
    config_file = open("./register.json","w")
    config_file.write(json.dumps(register))
    config_file.close()
    


## for each playlist will be created a folder with the same name containing the songs
def main():

    pref_CretePlaylistFolder = False
    pref_JustNewMusic = False
    
    if(len(sys.argv)>1):
        print(sys.argv)
        pref_CretePlaylistFolder = True if int(sys.argv[1]) == 1 else False
        pref_JustNewMusic = True if int(sys.argv[2]) == 1 else False ## delete the previous download and store the new one

    register = LoadRegister()

    # cycle thru the playlist, done manually because the API to retrieve automatically is a hell 
    ##  --> http://10.0.0.3:8096/Users/acbf0cef0357403a9a3abb314b67b2a3/Items?SortBy=SortName&SortOrder=Ascending&IncludeItemTypes=Playlist&Recursive=true&Fields=PrimaryImageAspectRatio%2CSortName%2CCanDelete&StartIndex=0

    # key: name of playlist, value: id of playlist
    playlists = dict()
    playlists["chillin"] = "4638cefbb8c256e05192e51aed0f48ec"
    playlists["deep night"] = "959668ac405340c31c34046129b35ac1"
    playlists["energy"] = "3c87f65b5fe53cf74c36219e8425af59"
    playlists["stuff"] = "1d64b9eab05f552af44fdb8c3efe8353"
    

    for p in playlists:
        print("Downloading ", p)
        songs_id = getSongsIDFromPlaylist(playlists[p])
        #check if the playlist file exists, if so, delete (to update all the list) -- the media already existing won't be downloaded again
        playlistFile = FOLDER_DEST+"/"+p+".m3u" 

        if(pref_JustNewMusic):
            with open(playlistFile,"w") as a: ## in just new music we can go to append the new music to the queque of playlist
                f.write("#"+p+"\n")

            ## and in new music we can avoid fetching all song to the playlist, so remove the stored songs_ids
            songs_id = set(songs_id)-set(register["known_songs"])
        else:
            #everything, so recreate the playlist file in itself, in writing mode thus do manage also delation, update (eg. change position of a song)
            with open(playlistFile,"w") as f:
                f.write("#"+p+"\n")

        for s in songs_id:
            downloadFile(register,s, p, getSongMetadata(s),pref_CretePlaylistFolder,pref_JustNewMusic)
            if(s not in register["known_songs"]):
                register["known_songs"].append(s)
        
        StoreRegister(register)


main()

