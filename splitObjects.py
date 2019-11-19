import os
import json
import sys
import math
import cv2


def data_split(min_threshold, max_threshold, path_to_file):
    min_data_objects = dict()
    middle_data_objects = dict()
    max_data_objects = dict()
    with open(path_to_file) as json_file:
        data = json.load(json_file)
        for key in data:
            bboxes = data[key]
            for bbox in bboxes:
                height = math.sqrt(((bbox[0] - bbox[0]) ** 2) + ((bbox[1] - bbox[3]) ** 2))
                width = math.sqrt(((bbox[0] - bbox[2]) ** 2) + ((bbox[1] - bbox[1]) ** 2))
                area = height * width
                img = cv2.imread(sys.argv[5] + key)
                img_area = img.shape[0] * img.shape[1]
                rate = (area * 100) / img_area
                if rate <= min_threshold:
                    if key in min_data_objects:
                        min_data_objects[key].append(bbox)
                    else:
                        min_data_objects[key] = []
                        min_data_objects[key].append(bbox)
                elif rate >= max_threshold:
                    if key in max_data_objects:
                        max_data_objects[key].append(bbox)
                    else:
                        max_data_objects[key] = []
                        max_data_objects[key].append(bbox)
                else:
                    if key in middle_data_objects:
                        middle_data_objects[key].append(bbox)
                    else:
                        middle_data_objects[key] = []
                        middle_data_objects[key].append(bbox)
    return min_data_objects, middle_data_objects, max_data_objects


def split_result_data(data, path_to_file):
    result = dict()
    with open(path_to_file) as json_file:
        data_from_model = json.load(json_file)
        for key in data:
            result[key] = data_from_model[key]
    return result


def main():
    small_data, middle_data, large_data = data_split(float(sys.argv[1]), float(sys.argv[2]), sys.argv[3])
    small_data_result = split_result_data(small_data, sys.argv[4])
    middle_data_result = split_result_data(middle_data, sys.argv[4])
    large_data_result = split_result_data(large_data, sys.argv[4])

    with open("small_data.json", "w") as outfile:
        json.dump(small_data, outfile)
    with open("middle_data.json", "w") as outfile:
        json.dump(middle_data, outfile)
    with open("large_data.json", "w") as outfile:
        json.dump(large_data, outfile)
    with open("small_data_result.json", "w") as outfile:
        json.dump(small_data_result, outfile)
    with open("middle_data_result.json", "w") as outfile:
        json.dump(middle_data_result, outfile)
    with open("large_data_result.json", "w") as outfile:
        json.dump(large_data_result, outfile)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Enter small rate, large rate, path to data file, path to model output file, path to images")
        exit(1)
    main()
