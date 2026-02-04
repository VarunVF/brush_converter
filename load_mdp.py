import os
import sys

from medibang.brush2 import read_brush2, write_brush_json
from medibang.brush2_options import translate_options


def usage():
    print("Usage: python load_mdp.py BRUSH2_FILE OUTPUT_JSON")
    print("    BRUSH2_FILE: Path to the Brush2.ini file")
    print("    OUTPUT_JSON: Path to write the output json file")


def main():
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]):
        usage()
        return
    
    brush_info = read_brush2(sys.argv[1])
    brush_info = translate_options(brush_info)
    write_brush_json(brush_info, sys.argv[2])

if __name__ == "__main__":
    main()
