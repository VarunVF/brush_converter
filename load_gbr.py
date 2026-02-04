import os
import sys

from gimp.gbr import read_gbr
from brush_json import write_brush_json


def usage():
    print("Usage: python load_gbr.py GBR_FILE OUTPUT_JSON")
    print("    GBR_FILE  : Path to the gbr file")
    print("    OUTPUT_DIR: Directory to write the output json and png files")


def main():
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]):
        usage()
        return
    
    os.makedirs(sys.argv[2], exist_ok=True)
    
    brush_info, img, bitmap_filename = read_gbr(sys.argv[1])
    json_path = os.path.join(sys.argv[2], "brush.json")
    image_path = os.path.join(sys.argv[2], bitmap_filename)

    # Translation not applicable for this format.
    write_brush_json(brush_info, json_path)
    img.save(image_path, "PNG")

if __name__ == "__main__":
    main()
