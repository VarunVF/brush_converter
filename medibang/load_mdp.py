import os
import sys

from medibang.brush2 import read_brush2
from medibang.brush2_options import OPTIONS, MEDIBANG_SPECIFIC
from translate import translate_options, remove_options
from brush_json import write_brush_json


def usage():
    return ("Usage: python load_mdp.py BRUSH2_FILE OUTPUT_JSON\n"
            "    BRUSH2_FILE: Path to the Brush2.ini file\n"
            "    OUTPUT_JSON: Path to write the output json file\n")


def check_args(brush2_file: str):
    if not os.path.isfile(brush2_file):
        raise ValueError(f"File does not exist: {brush2_file}")


def load_mdp(brush2_file: str, output_json: str):
    brush_info = read_brush2(brush2_file)
    brush_info = remove_options(MEDIBANG_SPECIFIC, brush_info)
    brush_info = translate_options(OPTIONS, brush_info)
    write_brush_json(brush_info, output_json)


def main():
    if len(sys.argv) == 1:
        print(usage())
        return
    elif len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments.\n" + usage())
    
    brush2_file = sys.argv[1]
    output_json = sys.argv[2]
    check_args(brush2_file)
    load_mdp(brush2_file, output_json)


if __name__ == "__main__":
    main()
