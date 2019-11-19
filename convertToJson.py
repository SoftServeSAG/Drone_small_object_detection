import os
import glob
import json
import sys


def main():
    path_list = glob.glob(os.path.join(sys.argv[1], "*.json"))

    res = dict()

    for index in range(len(path_list)):
        with open(path_list[index]) as json_file:
            data = json.load(json_file)
            name = data["image_id"] + ".jpg"
            res[name] = []
            if type(data["bbox"][0]) == list:
                for it in range(len(data["bbox"])):
                    data["bbox"][it][2] = data["bbox"][it][0] + data["bbox"][it][2]
                    data["bbox"][it][3] = data["bbox"][it][1] + data["bbox"][it][3]
                    res[name].append(data["bbox"][it])
            else:
                data["bbox"][2] = data["bbox"][0] + data["bbox"][2]
                data["bbox"][3] = data["bbox"][1] + data["bbox"][3]
                res[name].append(data["bbox"])

    with open("data.json", "w") as outfile:
        json.dump(res, outfile)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please enter path to file")
        exit(1)
    else:
        main()