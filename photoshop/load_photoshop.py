import os
import sys

from photoshop.abr import read_abr
from brush_json import write_brush_json


def usage():
    return ("Usage: python load_photoshop.py ABR_FILE OUTPUT_DIR\n"
            "    ABR_FILE  : Path to the abr file\n"
            "    OUTPUT_DIR: Directory to write the output json and png files\n")


def check_args(file_or_dir):
    if not os.path.isfile(file_or_dir):
        raise ValueError(f"No such file: {file_or_dir}")
    # OUTPUT_DIR will be created if it does not exist


def load_photoshop(abr_file: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    brush_info = read_abr(abr_file, output_dir)
    write_brush_json(brush_info, os.path.join(output_dir, "brush.json"))


def main():
    if len(sys.argv) == 1:
        print(usage())
        return
    elif len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments\n" + usage())
    
    abr_file = sys.argv[1]
    output_dir = sys.argv[2]
    check_args(abr_file)
    load_photoshop(abr_file, output_dir)


if __name__ == "__main__":
    main()
