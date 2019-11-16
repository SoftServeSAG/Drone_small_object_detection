import os
import random
import re
import json
import pandas
from PIL import Image

DATA_PATH = '/data_path'
FRAME_PATH = DATA_PATH + 'FRAME'
MASK_PATH = DATA_PATH + 'MASK'
JSON_PATH = DATA_PATH + 'Json'

# Create folders to hold images and masks

folders = ['train_frames', 'train_masks', 'train_json', 'val_frames', 'val_masks', 'val_json']

for folder in folders:
    os.makedirs(DATA_PATH + folder)

# Get all frames and masks, sort them, shuffle them to generate data sets.

all_frames = os.listdir(FRAME_PATH)
all_masks = os.listdir(MASK_PATH)
all_json = os.listdir(JSON_PATH)

all_frames.sort(key=lambda var: [int(x) if x.isdigit() else x
                                 for x in re.findall(r'[^0-9]|[0-9]+', var)])
all_masks.sort(key=lambda var: [int(x) if x.isdigit() else x
                                for x in re.findall(r'[^0-9]|[0-9]+', var)])
all_json.sort(key=lambda var: [int(x) if x.isdigit() else x
                               for x in re.findall(r'[^0-9]|[0-9]+', var)])

random.seed(123)
random.shuffle(all_frames)

# Generate train, val, and test sets for frames

train_split = int(0.8 * len(all_frames))
val_split = int(len(all_frames) - train_split)

train_frames = all_frames[:train_split]
val_frames = all_frames[train_split:]

# Generate corresponding mask lists for masks

train_masks = [f for f in all_masks if f in [f.replace("jpg", "png") for f in train_frames]]
val_masks = [f for f in all_masks if f in [f.replace("jpg", "png") for f in val_frames]]

# Generate corresponding mask lists for JSONs
train_json = [f for f in all_json if f in [f.replace("jpg", "json") for f in train_frames]]
val_json = [f for f in all_json if f in [f.replace("jpg", "json") for f in val_frames]]


# Add train, val, test frames,JSONs and masks to relevant folders


def add_frames(dir_name, image):
    img = Image.open(FRAME_PATH + image)
    img.save(DATA_PATH + '/{}'.format(dir_name) + '/' + image)


def add_masks(dir_name, image):
    img = Image.open(MASK_PATH + image)
    img.save(DATA_PATH + '/{}'.format(dir_name) + '/' + image)


def add_json(dir_name, json_file):

    with open(JSON_PATH + json_file) as json_data:
        data = json.load(json_data)
        with open(DATA_PATH + '/{}'.format(dir_name) + '/' + json_file, 'w') as f:
            json.dump(data, f)

    data = pandas.read_json(JSON_PATH + json)
    data.save(DATA_PATH + '/{}'.format(dir_name) + '/' + json)


frame_folders = [(train_frames, 'train_frames'), (val_frames, 'val_frames')]

mask_folders = [(train_masks, 'train_masks'), (val_masks, 'val_masks')]

json_folders = [(train_json, 'train_json'), (val_json, 'val_json')]

# Add frames

for folder in frame_folders:
    array = folder[0]
    name = [folder[1]] * len(array)

    list(map(add_frames, name, array))

# Add masks

for folder in mask_folders:
    array = folder[0]
    name = [folder[1]] * len(array)

    list(map(add_masks, name, array))

# Add JSON

for folder in json_folders:
    array = folder[0]
    name = [folder[1]] * len(array)

    list(map(add_json, name, array))






