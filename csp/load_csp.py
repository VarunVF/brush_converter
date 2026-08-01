import glob
import os
import sys

from csp.sut import read_sut
from brush_json import write_brush_json


def usage():
    return ("Usage: python load_csp.py SUT_FILE OUTPUT_DIR\n"
            "    SUT_FILE  : Path to the sut file\n"
            "    OUTPUT_DIR: Directory to write the output json and png files\n")


def check_args(file_or_dir):
    if not os.path.isfile(file_or_dir):
        raise ValueError(f"No such file: {file_or_dir}")
    # OUTPUT_DIR will be created if it does not exist


def load_csp(db_file_pattern: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(output_dir, "brush.json")
    brush_info: list[dict] = []

    for db_file in glob.glob(db_file_pattern):
        check_args(db_file)
        brush_info += read_sut(db_file, output_dir)

    write_brush_json(brush_info, json_path)


def main():
    if len(sys.argv) == 1:
        print(usage())
        return
    elif len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments\n" + usage())
    
    sut_file_pattern = sys.argv[1]
    output_dir = sys.argv[2]
    load_csp(sut_file_pattern, output_dir)


if __name__ == "__main__":
    main()
