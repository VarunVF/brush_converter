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
            "    BITMAP_DIR: Path to the directory containing brush bitmaps\n")


def check_args():
    if len(sys.argv) != 4:
        raise ValueError("Invalid number of arguments.\n" + usage())
    if not os.path.isfile(sys.argv[1]):
        raise ValueError(f"Brush JSON file does not exist: {sys.argv[1]}")
    if not os.path.isfile(sys.argv[2]):
        raise ValueError(f"Brush2.ini file does not exist: {sys.argv[2]}")
    # Bitmap directory will be created if it does not exist

def main():
    if len(sys.argv) == 1:
        print(usage())
        return
    
    check_args()
    
    brush_info = read_brush_json(sys.argv[1])
    brush_info = add_options(MEDIBANG_SPECIFIC, brush_info)
    brush_info = encode_options(OPTIONS, brush_info)
    write_brush2(brush_info, sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
