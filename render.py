from PIL import Image, ImageOps
from pymongo import MongoClient
from pprint import pprint
from os import listdir, getcwd()
from os.path import join
from sys import argv
from re import compile, search
from random import choice
from datetime import datetime

database = MongoClient()
db = database['rgba']
folders = [
    'tree',
    'aqua',
    'sand'
]
location = getcwd() + '/img/'
the_folder = argv[4]
collections = {f:db[f] for f in folders}
scale = int(argv[2])

def populate():
    total = len(data)
    w = resized_source.width
    h = resized_source.height
    count = {
        'x' : -1,
        'y' : 0
    }
    for pixel in range(total):
        print(pixel,'/',total)
        if count['x'] < w-1:
            count['x'] += 1
        else:
            count['x'] = 0
            count['y'] += 1

        x = count['x']*scale
        y = count['y']*scale

        image = determine_file(data[pixel])
        the_file = location + the_folder + '/' + image
        the_image = Image.open(the_file)
        the_resized_image = ImageOps.fit(the_image, (scale,scale))

        new_image.paste(the_resized_image,(x,y))

    export(new_image)

def export(image):
    test_path = join(location,'render/')
    greatestNumber = 0
    testID = argv[3]+argv[2]+'_'

    for f in listdir(test_path):
        pattern = compile(testID+'\d+')
        found = search(pattern, f)
        if found:
            currentNumber = int(found.group()[len(testID):])
            if(currentNumber >= greatestNumber):
                greatestNumber = currentNumber+1

    testFileName = test_path+testID+str(greatestNumber)+'.png'

    image.save(testFileName)

def scale_new():
    return (resized_source.width*scale, resized_source.height*scale)

def shrink_source():
    return (int(source_image.width/scale), int(source_image.height/scale))

remap_pixels = {}
def determine_file(pixel):
    original = pixel
    increment = 1

    try:
        image = remap_pixels[pixel]
    except KeyError:
        image = False
        tmp_map = { pixel : None }
        cursor = collections[the_folder].find_one({'band':'a','index':pixel})
        while cursor == None:
            tmp_map[pixel] = None
            if increment == 1 and pixel < 255:
                increment = 1
            elif increment == 1 and pixel == 255:
                increment = -1
                pixel = original
            elif increment == -1 and pixel > 0:
                increment = -1
            elif increment == -1 and pixel == 0:
                increment = 1
                pixel = original
            else:
                increment = 1

            pixel += increment
            try:
               image = remap_pixels[pixel]
               break
            except KeyError:
                cursor = collections[the_folder].find_one({'band':'a','index':pixel})

        if not image:
            image = cursor['images']
        for key in tmp_map:
            remap_pixels[key] = image

    return choice(image)

source_image = Image.open(join(location,argv[1]))
resized_source_size = shrink_source()
resized_source = ImageOps.fit(source_image,resized_source_size)
new_image = Image.new('RGB', scale_new(), (255,255,255))

data = list(resized_source.convert('L').getdata())

start = datetime.now()
populate()
pprint(remap_pixels)
print(datetime.now() - start)
