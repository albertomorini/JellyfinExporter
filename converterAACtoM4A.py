## Python script to convert ALAC (not supported on Android to AAC loseless in M4A, 256k bitrate that's good) ~> this improve storage (*ie 100MB song down to 20MB with same quality) and Android can play with every player (Phocid, RetroMusic, etc.)

import os
import subprocess
from mutagen.mp4 import MP4
from mutagen.mp4 import MP4StreamInfoError
########################


ffmpeg_cmd = "ffmpeg -i $songName -c:a aac -b:a 256k -vn $songName"


########################
# if ALAC coded return true
def is_alac(file_path):
    try:
        audio = MP4(file_path)
        codec = audio.info.codec_description
        # print(codec)
        return 'ALAC' in codec
    except MP4StreamInfoError:
        return False
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

### rename the new file, replacing the old one (no needed to have duplicates)
def cleanUp(oldPath,newPath):
    cmd = ["mv", newPath, oldPath]
    subprocess.run(cmd)

# execute ffmpeg format
def convertCodec(albumPath, songName):
    input_path = os.path.join(albumPath, songName)
    output_path = os.path.join(albumPath, "N" + songName)

    # ffmpeg command as list (safer and no shell escaping needed)
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_path,
        "-c:a", "aac",
        "-b:a", "256k",
        "-vn",
        output_path
    ]

    print("Running command:", " ".join(ffmpeg_cmd))
    result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(f"ffmpeg error for {songName}:\n{result.stderr.decode()}")
    else:
        print(f"Converted: {songName}")
        cleanUp(input_path,output_path)


# scan root folder searching for ALAC
def scanFolder(path):
    alac_files = []
    for root, directories, files in os.walk(path, topdown=True):
        for name in files:
            pathTmp=str(os.path.join(root, name))
            if(pathTmp.endswith(".m4a") and is_alac(pathTmp)):
                    alac_files.append(pathTmp)
                    ## CONVERT TO AAC
                    convertCodec(root,name)

    return alac_files
					

    

alac_songs = scanFolder("/mnt/MEDIA/MUSIC/")

for song in alac_songs:
    print(song)

print(len(alac_songs))
