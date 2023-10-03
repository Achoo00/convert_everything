from PIL import Image
import os
from tqdm import tqdm #Progress bar used in for loop

os.startfile('C:\\Users\\amaha\\PycharmProjects\\converter\\input')
path = os.chdir('C:\\Users\\amaha\\PycharmProjects\\converter\\input\\')

def img_type_input():
    img_type = input("Converting WEBP [1] or JPG [2] or JFIF [3]?" + "")
    if int(img_type) == 1:
        img_type = '.webp'
        fixed_filename=-9
    elif int(img_type) == 2:
        img_type = '.jpg'
        fixed_filename=-8
    elif int(img_type) == 3:
        img_type = '.jfif'
        fixed_filename=-9
    else:
        print("Enter 1 or 2")
        img_type_input()
    return img_type, fixed_filename

def start_input():
    img_type, fix_filename = img_type_input()
    start = input("Convert All [1] or Manual [2]:" + "")
    if int(start) == 1: # Converts all images in input
        for item in tqdm(os.listdir(path)):
            os.chdir('C:\\Users\\amaha\\PycharmProjects\\converter\\input')
            if item.endswith(str(img_type)): # Converts every .webp to .png
                im = Image.open(item)
                os.chdir('C:\\Users\\amaha\\PycharmProjects\\converter\\output')
                im.save(item + '.png')
        for filename in os.listdir(): # Removes .webp in image name
            if filename.endswith('png'):
                os.rename(filename, filename[:fix_filename] + filename[-4:])
    elif int(start) == 2: # Converts 1 manually typed image name
        image_name = input("Image name:")
        im = Image.open(image_name + str(img_type))
        os.chdir('C:\\Users\\amaha\\PycharmProjects\\converter\\output')
        im.save(image_name + '.png')
    else:
        print("Enter 1 or 2")
        start_input()


start_input()
os.startfile('C:\\Users\\amaha\\PycharmProjects\\converter\\output')
