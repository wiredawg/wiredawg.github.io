#!/usr/bin/env python
import argparse, os, sys
from fractions import Fraction

import PIL
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_gps_info(filename):
    try:
        exif = Image.open(filename)._getexif()
    except (IsADirectoryError, PIL.UnidentifiedImageError): return {}

    if exif is None: return {}

    for key, value in exif.items():
        name = TAGS.get(key, key)
        exif[name] = exif.pop(key)

    if 'GPSInfo' not in exif: return {}

    for key in exif['GPSInfo'].keys():
        name = GPSTAGS.get(key,key)
        exif['GPSInfo'][name] = exif['GPSInfo'].pop(key)

    return exif.get("GPSInfo", {})


def strip_exif(filename, overwrite=False):
    image = Image.open(filename)
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    if overwrite:
        new_filename = filename
        print("Overwritting: " + filename)
    else:
        oldfname,ext = os.path.splitext(filename)
        new_filename = oldfname + ".stripped" + ext
    image_without_exif.save(new_filename)

def main():
    parser = argparse.ArgumentParser(description='Strip EXIF from any image with GPS information in it.')
    parser.add_argument('dir', metavar='DIRECTORY', help='The directory to process.')
    parser.add_argument('--overwrite', default=False, action="store_true", help='Overwrite the original image files.')

    args = parser.parse_args()
    files = os.listdir(args.dir)

    for iname in files:
        filename = args.dir+iname
        gps_info = get_gps_info(filename)
        if not gps_info:
            print("No GPS info: " + iname)
            continue
        print(iname, gps_info)
        strip_exif(filename, overwrite=args.overwrite)

    return 0

# =============================================================================
if __name__ == "__main__" : sys.exit(main())
