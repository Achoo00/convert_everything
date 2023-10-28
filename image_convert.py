# Converts images to "png" format

from PIL import Image
import os
from tqdm import tqdm #Progress bar used in for loop

os.startfile('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\input')
path = os.chdir('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\input')


def img_type_input():
    img_type = input("Converting WEBP [1] or JPG [2] or JFIF [3]? or JPEG [4]" + "")
    if int(img_type) == 1:
        img_type = '.webp'
    elif int(img_type) == 2:
        img_type = '.jpg'
    elif int(img_type) == 3:
        img_type = '.jfif'
    elif int(img_type) == 4:
        img_type = '.jpeg'
    else:
        print("Enter # between 1 to 4")
        img_type_input()
    return img_type

def start_input():
    img_type = img_type_input()
    start = input("Convert All [1] or Manual [2]:" + "")
    if int(start) == 1: # Converts all images in input
        for item in tqdm(os.listdir(path)):
            os.chdir('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\input')
            if item.endswith(str(img_type)): # Converts every .webp to .png
                im = Image.open(item)
                renamed_item = item.replace(img_type,"")
                os.chdir('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\output')
                im.save(renamed_item + '.png')
    elif int(start) == 2: # Converts 1 manually typed image name
        image_name = input("Image name:")
        im = Image.open(image_name + str(img_type))
        os.chdir('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\output')
        im.save(image_name + '.png')
    else:
        print("Enter 1 or 2")
        start_input()


start_input()
os.startfile('C:\\Users\\amaha\\VS_Python_Projects\\convert_everything\\output')
