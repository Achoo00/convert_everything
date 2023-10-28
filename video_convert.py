# Converts mp4 to gif

import moviepy.editor as mp
from tqdm import tqdm #Progress bar used in for loop
import os

os.startfile('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\input')
path = os.chdir('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\input')

def vid_type_input():
    vid_type = input("Converting MP4 [1]" + "")
    if int(vid_type) == 1:
        vid_type = '.mp4'
    else:
        print("Enter 1 or 2")
        vid_type_input()
    return vid_type

def start_input():
    vid_type = vid_type_input()
    for item in tqdm(os.listdir(path)):
        os.chdir('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\input')
        if item.endswith("mp4"): # Converts every .mp4 to .gif
            clip = mp.VideoFileClip(item)
            renamed_item = item.replace(".mp4","")
            os.chdir('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\output')
            clip.write_gif(renamed_item + ".gif", fps=15)

start_input()
os.startfile('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\output')
