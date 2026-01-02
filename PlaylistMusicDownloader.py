import requests
import os
import json
import sys
########################################################################################
########################################################################################

BASE_URL = "http://10.0.0.3:8096/"
HEADERS = {'Authorization': 'MediaBrowser Client="Jellyfin%20Web", Device="Firefox", DeviceId="TW96aWxsYS81LjAgKFgxMTsgTGludXggeDg2XzY0OyBydjoxNDYuMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC8xNDYuMHwxNzY2NTczMzI4MTgw", Version="10.11.4", Token="e333b841f09d4d129918e51d9915f4d8"'}

FOLDER_DEST = "/home/alby/MusicExported/"


PREF_CretePlaylistFolder = False
PREF_VirginExport = False

# load preferences if indicated
if(len(sys.argv)>1):
    print(sys.argv)
    PREF_CretePlaylistFolder = True if int(sys.argv[1]) == 1 else False
    PREF_VirginExport = True if int(sys.argv[2]) == 1 else False ## delete the previous download and store the new one

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
########################################################################################
    
def downloadFile(register,fileID,playlistName,fileName, createPlaylistFolder=False):
    url = BASE_URL+"Items/"+fileID+"/Download"
    with requests.get(url, stream=True, headers=HEADERS) as res:
        if(res.status_code==200):
            if(not os.path.isdir(FOLDER_DEST)):
                os.mkdir(FOLDER_DEST)
            
            print(fileName)
            if(createPlaylistFolder):
                finalPath = FOLDER_DEST + "/" +playlistName
            else:
                finalPath = FOLDER_DEST + "downloaded"
                playlistFile = FOLDER_DEST+"/"+playlistName+".m3u"
                with open(playlistFile,"a") as f: ## append file name to create the playlist
                    f.write("./downloaded/"+fileName+"\n")
                    f.close()


            if(not os.path.isdir(finalPath)): ## make final dir to store songs
                os.mkdir(finalPath)

            if(playlistName not in register):
                register[playlistName] = []

            # if(not os.path.exists(os.path.join(os.getcwd(), (finalPath), fileName))): #only if not exists
            if(fileID not in register[playlistName]): # if not exists store the song
                with open(finalPath+"/"+fileName, 'wb') as f:
                    for chunk in res.iter_content(chunk_size=8192): 
                        f.write(chunk)
                    print("Downloaded "+fileName+" in folder: "+finalPath)
            
            # elif(deleteOld): #if song already stored and justNewMusic is enabled, delete the old ones
            #     try:
            #         print("Deleting "+fileName)
            #         os.remove(finalPath+"/"+fileName)
            #     except OSError as e:
            #         pass # print(e)

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


## for each playlist will be created a folder with the same name containing the songs
def main():

    register = LoadRegister()
    # cycle thru the playlist, done manually because the API to retrieve automatically is a hell 
    ##  --> http://10.0.0.3:8096/Users/acbf0cef0357403a9a3abb314b67b2a3/Items?SortBy=SortName&SortOrder=Ascending&IncludeItemTypes=Playlist&Recursive=true&Fields=PrimaryImageAspectRatio%2CSortName%2CCanDelete&StartIndex=0

    # key: name of playlist, value: id of playlist
    playlists = dict()
    playlists["chillin"] = "4638cefbb8c256e05192e51aed0f48ec"
    playlists["deep night"] = "959668ac405340c31c34046129b35ac1"
    playlists["productivity"] = "5249d82dfb0a8530040b0485a86ab1ee"
    playlists["godmode"]= "b3590f563320eb6ad8952305ab31e1c5"
    
    if(PREF_VirginExport): ## remove previously downloaded songs
        storageDir = FOLDER_DEST+"downloaded"
        for filename in os.listdir(storageDir):
            file_path = os.path.join(storageDir, filename)
            if(not os.path.isdir(file_path)):
                os.remove(file_path)
        
    for playlistName in playlists:
        playlistFile = FOLDER_DEST+"/"+playlistName+".m3u"
        if(PREF_VirginExport):
            #everything, so recreate the playlist file in itself, in writing mode thus do manage also delation, update (eg. change position of a song)
            register[playlistName] = []
            with open(playlistFile,"w") as f:
                f.write("#"+playlistFile+"\n")

        print("Downloading ", playlistName)
        songs_id = getSongsIDFromPlaylist(playlists[playlistName]) #get the IDs of the songs
        with open(playlistFile,"a") as f: ## in just new music we can go to append the new music to the queque of playlist
            f.write("#"+playlistName+"\n")

        try:
            songs_id = set(songs_id)-set(register[playlistName])
        except Exception as e:
            song_id = set(songs_id)

        for s in songs_id:
            if(playlistName in register):
                if(s not in register[playlistName]):
                    downloadFile(register,s, playlistName, getSongMetadata(s),PREF_CretePlaylistFolder)
                    register[playlistName].append(s)
            else:
                    downloadFile(register,s, playlistName, getSongMetadata(s),PREF_CretePlaylistFolder)
                    register[playlistName].append(s)

        StoreRegister(register)

main()
