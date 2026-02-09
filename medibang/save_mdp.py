import os
import sys

from medibang.brush2 import write_brush2
from medibang.brush2_options import OPTIONS, MEDIBANG_SPECIFIC
from translate import add_options, encode_options
from brush_json import read_brush_json


def usage():
    return ("Usage: python save_mdp.py BRUSH_JSON BRUSH2_INI BITMAP_DIR\n"
            "    BRUSH_JSON: Path to the brush json file\n"
            "    BRUSH2_INI: Path to the Brush2.ini file\n"
            "    BITMAP_DIR: Path to the directory to write brush bitmaps\n")


def check_args(brush_json_file: str, brush2_ini_file: str):
    if not os.path.isfile(brush_json_file):
        raise ValueError(f"Brush JSON file does not exist: {brush_json_file}")
    if not os.path.isfile(brush2_ini_file):
        raise ValueError(f"Brush2.ini file does not exist: {brush2_ini_file}")
    # BITMAP_DIR will be created if it does not exist


def save_mdp(brush_json_file: str, brush2_ini_file: str, bitmap_dir: str):
    brush_info = read_brush_json(brush_json_file)
    brush_info = add_options(MEDIBANG_SPECIFIC, brush_info)
    brush_info = encode_options(OPTIONS, brush_info)
    write_brush2(brush_info, brush_json_file, brush2_ini_file, bitmap_dir)


def main():
    if len(sys.argv) == 1:
        print(usage())
        return
    elif len(sys.argv) != 4:
        raise ValueError("Invalid number of arguments.\n" + usage())    
    
    brush_json_file = sys.argv[1]
    brush2_ini_file = sys.argv[2]
    bitmap_dir = sys.argv[3]
    check_args(brush_json_file, brush2_ini_file)
    save_mdp(brush_json_file, brush2_ini_file, bitmap_dir)


if __name__ == "__main__":
    main()
