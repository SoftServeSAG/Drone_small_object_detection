import os
import glob
import cv2
import csv
import json
import numpy as np
from pycocotools import mask
from skimage import measure
import urllib.request

def new_mask_annotation(path_to_mask):
    path_to_masks = glob.glob(os.path.join(path_to_mask, '*.png'))
    for index in range(len(path_to_masks)):
        print(index)
        image_name = path_to_masks[index].split('/')[1].split('.')[0]
        img_mask = cv2.imread(path_to_masks[index], cv2.IMREAD_GRAYSCALE)
        ground_truth_binary_mask = np.array(img_mask)
        fortran_ground_truth_binary_mask = np.asfortranarray(ground_truth_binary_mask)
        encoded_ground_truth = mask.encode(fortran_ground_truth_binary_mask)
        ground_truth_area = mask.area(encoded_ground_truth)
        ground_truth_bounding_box = mask.toBbox(encoded_ground_truth)
        contours = measure.find_contours(ground_truth_binary_mask, 0.5)

        annotation = {
            "segmentation": [],
            "area": ground_truth_area.tolist(),
            "iscrowd": 0,
            "image_id": image_name,
            "bbox": ground_truth_bounding_box.tolist(),
            "category_id": 1,
            "id": index
        }

        if os.path.isfile('Json2/{}.json'.format(image_name)):
            with open('Json2/{}.json'.format(image_name), 'r+') as my_file:
                data = json.load(my_file)
                for contour in contours:
                    contour = np.flip(contour, axis=1)
                    segmentation = contour.ravel().tolist()
                    data['segmentation'].append(segmentation)
                my_file.seek(0)
                json.dump(data, my_file)
                my_file.truncate()
        else:
            for contour in contours:
                contour = np.flip(contour, axis=1)
                segmentation = contour.ravel().tolist()
                annotation['segmentation'].append(segmentation)

            with open('Json2/{}.json'.format(image_name), 'w') as my_file:
                json.dump(annotation, my_file)

if __name__ == "__main__":
    with open('SoftBall.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        index = 0
        for row in readCSV:
            index += 1
            if index < 0:
                continue
            data = row[3]
            if len(data) < 40:
                continue
            data = json.loads(data)
            link = data["objects"][0]["instanceURI"]
            print(link)
            mask_name = row[9].split('.')[0]
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(link, "BallReadSoftserveMask/{}.png".format(mask_name))
            print(index)

    new_mask_annotation("BallReadSoftserveMask/")
