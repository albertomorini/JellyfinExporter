
# Jellyfin Exporter

Export music playlists to local folder

**PARAMETERS**
```sh
python3 PlaylistMusicDownloader.py $PlaylistFolder $JustNewMusic

------
$PlaylistFolder  --> if 1 create a folder for each playlist | 0 just store all song in single folder
$JustNewMusic --> if 1 delete old songs not contained in register and download new | 0 leave the old songs and download new 

```


#TODO:

[ ] Configure the download destination folder
[ ] Interactive playlist picking