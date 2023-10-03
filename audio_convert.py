# Converts m4a to unsigned 8-bit PCM at 16000 Hz

from pydub import AudioSegment
import os
from tqdm import tqdm #Progress bar used in for loop

i=0 # Starting value

os.chdir("C:/ffmpeg/bin")

input_folder="C:/Users/amaha/PycharmProjects/converter/input"
output_folder="C:/Users/amaha/PycharmProjects/converter/output"

# Set the path to the ffmpeg executable
AudioSegment.converter = 'C:/ffmpeg/bin/ffmpeg'
AudioSegment.ffprobe = 'C:/ffmpeg/bin/ffprobe'

for item in tqdm(os.listdir(input_folder)):
    os.chdir(input_folder)
    if item.endswith('.m4a'):  # Finds only .m4a files to convert

        # Read the m4a file using pydub
        audio = AudioSegment.from_file(item, format='m4a')
        audio = audio.set_sample_width(1) # 1 byte = 8 bits
        audio = audio.set_channels(1) # mono channel

        # Export the audio data to a pcm file
        os.chdir(output_folder)
        #audio.export(str(i) + '.pcm', format='u8', parameters=['-ar', '16000']) # Sampling rate set to 16000 Hz
        audio.export(str(i) + '.mp3')
        # s8 means signed 8-bit PCM
        # u8 means unsigned 8-bit PCM
        i = i + 1 # Counter for filename
