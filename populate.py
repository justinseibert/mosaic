from PIL import Image, ImageStat
from os import listdir, getcwd
from statistics import mean
from os.path import join
from pymongo import MongoClient

database =  MongoClient()
db = database['rgba']
folders = [
    'tree',
    'aqua',
    'sand'
]
colors = {f:([None]*255) for f in folders}
location = getcwd() + '/img/'

def populate():
    if 'tree' in db.collection_names():
        db.drop_collection('tree')
        db.drop_collection('aqua')
        db.drop_collection('sand')

    collections = {f:db[f] for f in folders}
    for folder in folders:
        directory = join(location,folder+'/')
        for file in listdir(directory):
            if file.lower().endswith('png'):
                the_file = join(directory, file)

                the_image = Image.open(the_file)
                bands = ImageStat.Stat(the_image).mean

                the_bands = {
                    'a' : int(mean(bands)),
                    'r' : int(bands[0]),
                    'g' : int(bands[1]),
                    'b' : int(bands[2])
                }

                for the_band in the_bands:
                    index = the_bands[the_band]
                    collections[folder].update_one(
                        {
                            'band' : the_band,
                            'index': index,
                        },
                        {
                            '$push' : { 'images' : file },
                        },
                        True
                    )
populate()
