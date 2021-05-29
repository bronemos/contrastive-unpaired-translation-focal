import cv2
import numpy as np
import sys
from shutil import copy, copyfile
import os


def contains_water(img):
    hsv_l = np.array([254, 208, 177])
    hsv_h = np.array([255, 209, 178])

    return 255 in cv2.inRange(img, hsv_l, hsv_h)


def copy_water(directory: str):
    count = 0
    for file in os.listdir(directory):
        src_B = directory + file
        src_A = directory.replace("B", "A") + file.replace("_B", "_A")
        src = directory.replace("B", "") + file.replace("_B", "")
        dest_B = directory.replace("maps", "maps-filtered") + file
        dest_A = directory.replace("B", "A").replace(
            "maps", "maps-filtered"
        ) + file.replace("_B", "_A")
        dest = directory.replace("B", "").replace(
            "maps", "maps-filtered"
        ) + file.replace("_B", "")
        img = cv2.imread(src)
        if contains_water(img):
            copyfile(src, dest)
            copyfile(src_A, dest_A)
            copyfile(src_B, dest_B)
            count += 1
    return count


def copy_no_water(directory: str, max_count: int):
    curr_count = 0
    for file in os.listdir(directory):
        src_B = directory + file
        src_A = directory.replace("B", "A") + file.replace("_B", "_A")
        src = directory.replace("B", "") + file.replace("_B", "")
        dest_B = directory.replace("maps", "maps-filtered") + file
        dest_A = directory.replace("B", "A").replace(
            "maps", "maps-filtered"
        ) + file.replace("_B", "_A")
        dest = directory.replace("B", "").replace(
            "maps", "maps-filtered"
        ) + file.replace("_B", "")
        img = cv2.imread(src)
        if not contains_water(img) and curr_count < max_count:
            copyfile(src, dest)
            copyfile(src_A, dest_A)
            copyfile(src_B, dest_B)
            curr_count += 1


def main():
    directory = sys.argv[1]
    max_count = copy_water(directory)
    print(max_count)
    copy_no_water(directory, max_count)


if __name__ == "__main__":
    main()
