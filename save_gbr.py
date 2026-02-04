import os
import sys

from gimp.gbr import write_gbr
from brush_json import read_brush_json


def usage():
    print("Usage: python save_gbr.py BRUSH_JSON OUTPUT_GBR")
    print("    BRUSH_JSON: Path to the brush json file")
    print("    OUTPUT_GBR: Path to write the output gbr file")


def main():
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]):
        usage()
        return

    # Translation not applicable for this format.
    brush_info = read_brush_json(sys.argv[1])
    write_gbr(brush_info, sys.argv[2])

if __name__ == "__main__":
    main()
