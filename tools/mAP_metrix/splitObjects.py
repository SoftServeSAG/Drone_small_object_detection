import os
import json
import sys
import math
import cv2
from argparse import ArgumentParser, SUPPRESS


def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group("Options")
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument('-s', '--small', action='Small object rate.', default=1.5, type=float)
    args.add_argument('-l', '--large', action='Large object rate.', default=20, type=float)
    args.add_argument("-a", "--annotation", help="Required. Path to data annotation file.",
                      required=True, type=str)
    args.add_argument("-f", "--folder", help="Required. Path to model output data file.",
                      required=True, type=str)
    args.add_argument("-i", "--images", help="Required. Path to images.",
                      required=True, type=str)

    return parser


def data_split(min_threshold, max_threshold, path_to_file, path_to_images):
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
                img = cv2.imread(path_to_images + key)
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
    args = build_argparser().parse_args()
    small_data, middle_data, large_data = data_split(float(args.small), float(args.large), args.annotation,
                                                     args.images)
    small_data_result = split_result_data(small_data, args.folder)
    middle_data_result = split_result_data(middle_data, args.folder)
    large_data_result = split_result_data(large_data, args.folder)

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
    main()
