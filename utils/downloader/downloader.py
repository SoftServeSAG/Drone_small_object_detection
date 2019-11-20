import csv
import json
import urllib.request
import cv2
import functools
import numpy as np


with open('SoftBall.csv') as csvfile:
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    readCSV = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in readCSV:
        data = row[3]
        if len(data) < 40:
            continue


        mask_name = row[9].split('.')[0]
        print(f"{index} - {mask_name}")

        data = json.loads(data)

        all_imgs = []
        for mask in data["objects"]:
            link = mask["instanceURI"]
            print(link)
            # req = urllib.request.urlopen(link)
            # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            # all_imgs.append(cv2.imdecode(arr, -1))

        if len(all_imgs) == 0:
            continue
        elif len(all_imgs) == 1:
            # cv2.imwrite(f"./Rosbag2_vol1/{mask_name}.png", all_imgs[0])
            pass
        else:
            # cv2.imwrite(f"./Rosbag2_vol1/{mask_name}.png", functools.reduce(lambda a, b: cv2.bitwise_or(a, b), all_imgs))
            print("reduced")

        index += 1
