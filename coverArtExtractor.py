import os
import subprocess


ffmpeg_cmd = "ffmpeg -i t.m4a -an cover.jpg"
PATH = "/Users/alby/Downloads/t.m4a"


# subprocess.call(['useradd', '-m', '-g', _primarygroup, '-G', _secondarygroup, '-u', _userid, _username])


#process each song by searching and saving the lyrics
def scanFolder(path):
    for root, directories, files in os.walk(path, topdown=True):
        for name in files:
            pathTmp=str(os.path.join(root, name))
            if(pathTmp.endswith(".m4a")):

                dummy = "cd "+ root+ " ;" + "ffmpeg -i "+name.replace(" ",r'\ ')+" -an cover.jpg"
                print([dummy]) 
                subprocess.run(dummy) 
                # print(["cd ", root, " ;", "ffmpeg -i ",name," -an cover.jpg"]) 
                continue
               




scanFolder("/Volumes/MEDIA/MUSIC/")