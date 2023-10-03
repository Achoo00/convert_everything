# Converts mp4 to gif
# Not working

import moviepy.editor as mp
from tqdm import tqdm #Progress bar used in for loop
import os

os.startfile('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\input')
path = os.chdir('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\input')

def vid_type_input():
    vid_type = input("Converting MP4 [1]" + "")
    if int(vid_type) == 1:
        vid_type = '.mp4'
        fixed_filename=-8
    else:
        print("Enter 1 or 2")
        vid_type_input()
    return vid_type, fixed_filename

def start_input():
    vid_type, fix_filename = vid_type_input()
    for item in tqdm(os.listdir(path)):
        os.chdir('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\input')
        if item.endswith("mp4"): # Converts every .mp4 to .gif
            clip = mp.VideoFileClip(item)
            #os.chdir('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\output')
            clip.write_videofile("videoconv.gif")
        for filename in os.listdir(): # Removes .webp in image name
            if filename.endswith('mp4'):
                os.rename(filename, filename[:fix_filename] + filename[-4:])

start_input()
os.startfile('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\output')
