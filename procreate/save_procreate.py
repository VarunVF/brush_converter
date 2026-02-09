import os
import sys

from procreate.brush import write_procreate_brush
from brush_json import read_brush_json


def usage():
    return ("Usage: python save_procreate.py BRUSH_JSON BITMAP_DIR OUTPUT_DIR\n"
            "    BRUSH_JSON: Path to the brush json file\n"
            "    BITMAP_DIR: Path to the directory containing the brush bitmaps\n"
            "    OUTPUT_DIR: Path to the output directory for procreate brushes\n")


def check_args(json_filepath: str, bitmap_dir: str):
    if not os.path.isfile(json_filepath):
        raise ValueError(f"Brush JSON file does not exist: {json_filepath}")
    if not os.path.isdir(bitmap_dir):
        raise ValueError(f"Bitmap directory does not exist: {bitmap_dir}")
    # OUTPUT_DIR will be created if it does not exist


def save_procreate(json_filepath: str, bitmap_dir: str, output_dir: str):
    brush_info = read_brush_json(json_filepath)
    write_procreate_brush(brush_info, bitmap_dir, output_dir)


def main():
    if len(sys.argv) == 1:
        print(usage())
        return
    elif len(sys.argv) != 4:
        raise ValueError("Invalid number of arguments.\n" + usage())
    
    json_filepath = sys.argv[1]
    bitmap_dir = sys.argv[2]
    output_dir = sys.argv[3]
    check_args(json_filepath, bitmap_dir)
    save_procreate(json_filepath, bitmap_dir, output_dir)


if __name__ == "__main__":
    main()
