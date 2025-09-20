
# Jellyfin Exporter

Export music playlists to local folder

**PARAMETERS**
```sh
python3 PlaylistMusicDownloader.py $PlaylistFolder $JustNewMusic

------
$PlaylistFolder  --> if 1 create a folder for each playlist | 0 just store all song in single folder
$JustNewMusic --> if 1 delete old songs not contained in register and download new | 0 leave the old songs and download new 

```

*use case of JustNewMusic*: I personally download the song into a folder on my PC, then I move them (via LocalSend app, WiFi) to my phone where I already got the previous downloaded songs and then I just need the updated playlist


#TODO:

[ ] Configure the download destination folder
[ ] Interactive playlist picking