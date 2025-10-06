import os
import subprocess
import json

from pathlib import Path

ffmpeg_cmd = 'ffmpeg -i $songName -i cover.jpg -map 0 -map 1 -c copy -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" -disposition:v attached_pic $songName'
PATH = "/mnt/MEDIA/MUSIC/"


### rename the new file, replacing the old one (no needed to have duplicates)
def cleanUp(oldPath,newPath):
    cmd = ["mv", newPath, oldPath]
    subprocess.run(cmd)


def insertImage(albumPath, songName):
    try:
        input_path = os.path.join(albumPath, songName)
        output_path = os.path.join(albumPath, "tmp"+ songName)

        # ffmpeg command as list (safer and no shell escaping needed)
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", input_path,
            "-i", albumPath+"/cover.jpg",
            "-map", "0",
            "-map", "1",
            "-c", "copy",
            "-metadata:s:v", "title=Album cover",
            "-metadata:s:v", "comment=Cover (front)",
            "-disposition:v", "attached_pic",
            output_path
        ]

        result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(f"ffmpeg error for {songName}:\n{result.stderr.decode()}")
        else:
            print(f"Added for: {songName}")
            cleanUp(input_path,output_path)
    except Exception as e:
        pass


def has_cover_art(file_path):
    if not Path(file_path).is_file():
        print(f"File does not exist: {file_path}")
        return False
    try:
        # Run ffprobe to get all streams in JSON format
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_streams",
                file_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"ffprobe failed: {result.stderr.strip()}", file_path)
            return False

        info = json.loads(result.stdout)
        streams = info.get("streams", [])

        for stream in streams:
            if stream.get("codec_type") == "video":
                disposition = stream.get("disposition", {})
                if disposition.get("attached_pic") == 1:
                    return True

        return False

    except Exception as e:
        print(f"Error: {e}")
        return False



def scanFolder(path):
    for root, directories, files in os.walk(path, topdown=True):
        for name in files:
            pathTmp=str(os.path.join(root, name))
            if(pathTmp.endswith(".m4a") and not has_cover_art(pathTmp)):
                insertImage(root,name)
                


scanFolder(PATH)