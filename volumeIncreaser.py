import os
import subprocess

def increase_volume_in_folder(directory, volume_factor=3):
    # Get all files in the directory
    for filename in os.listdir(directory):
        # Skip directories, only process files
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            continue

        # Get file extension and check if it's a valid audio file
        ext = filename.split('.')[-1].lower()
        if ext not in ['mp3', 'wav', 'm4a', 'flac']:
            continue
        
        print(f"Processing {filename}...")

        # Prepare input and temporary output file paths
        input_file = file_path
        temp_output = os.path.join(directory, 'output.m4a')
        
        # FFmpeg command to increase volume
        command = [
            'ffmpeg', 
            '-i', input_file, 
            '-filter:a', f'volume={volume_factor}', 
            temp_output
        ]
        
        # Run the FFmpeg command
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Rename the temp file to the original filename
        final_output = os.path.join(directory, filename)
        os.rename(temp_output, final_output)
        
        print(f"Volume increased for {filename}.")

if __name__ == "__main__":
    # Directory where your audio files are located
    folder_path = "/mnt/MEDIA/MUSIC/Kanye West/Donda 2"  # <-- Change this path!
    
    # Volume factor (e.g., 2 means double the volume)
    volume_factor = 2

    increase_volume_in_folder(folder_path, volume_factor)
