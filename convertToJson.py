import os
import glob
import json
import sys

path_list = glob.glob(os.path.join("BallJson/", "*.json"))

res = dict()

for index in range(len(path_list)):
    with open(path_list[index]) as json_file:
        data = json.load(json_file)
        name = data["image_id"] + ".jpg"
        res[name] = []
        data["bbox"][2] = data["bbox"][0] + data["bbox"][2]
        data["bbox"][3] = data["bbox"][1] + data["bbox"][3]
        res[name].append(data["bbox"])

with open("data.json", "w") as outfile:
    json.dump(res, outfile)
