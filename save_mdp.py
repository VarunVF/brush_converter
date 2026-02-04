import os
import sys

from medibang.brush2 import write_brush2
from medibang.brush2_options import OPTIONS, MEDIBANG_SPECIFIC
from translate import add_options, encode_options
from brush_json import read_brush_json


def usage():
    print("Usage: python save_mdp.py BRUSH_JSON OUTPUT_INI")
    print("    BRUSH_JSON: Path to the brush json file")
    print("    OUTPUT_INI: Path to write the output ini file")


def main():
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]):
        usage()
        return
    
    brush_info = read_brush_json(sys.argv[1])
    brush_info = add_options(MEDIBANG_SPECIFIC, brush_info)
    brush_info = encode_options(OPTIONS, brush_info)
    write_brush2(brush_info, sys.argv[2])

if __name__ == "__main__":
    main()
