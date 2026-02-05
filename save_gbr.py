import os
import sys

from gimp.gbr import write_gbr
from brush_json import read_brush_json


def usage():
    return ("Usage: python save_gbr.py BRUSH_JSON OUTPUT_GBR BITMAP_DIR\n"
            "    BRUSH_JSON: Path to the brush json file\n"
            "    BITMAP_DIR: Path to the directory containing brush bitmaps\n"
            "    OUTPUT_DIR: Path to the directory to write output gbr files\n")


def check_args():
    if len(sys.argv) != 4:
        raise ValueError("Invalid number of arguments.\n" + usage())
    if not os.path.isfile(sys.argv[1]):
        raise ValueError(f"Brush JSON file does not exist: {sys.argv[1]}")
    if not os.path.isdir(sys.argv[3]):
        raise ValueError(f"Bitmap directory does not exist: {sys.argv[3]}")
    # OUTPUT_DIR will be created if it does not exist.


def main():
    if len(sys.argv) == 1:
        print(usage())
        return

    check_args()

    # Translation not applicable for this format.
    brush_info = read_brush_json(sys.argv[1])
    write_gbr(brush_info, sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
