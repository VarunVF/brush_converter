import os
import sys

from medibang.brush2 import write_brush2, read_brush_json
from medibang.brush2_options import encode_options


def usage():
    print("Usage: python save_mdp.py BRUSH_JSON OUTPUT_INI")
    print("    BRUSH_JSON: Path to the brush json file")
    print("    OUTPUT_INI: Path to write the output ini file")


def main():
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]):
        usage()
        return
    
    brush_info = read_brush_json(sys.argv[1])
    brush_info = encode_options(brush_info)
    write_brush2(brush_info, sys.argv[2])

if __name__ == "__main__":
    main()
