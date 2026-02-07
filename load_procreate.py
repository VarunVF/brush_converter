import os
import sys

from procreate.brush import read_procreate_brush
from brush_json import write_brush_json


def usage():
    return ("Usage: python load_procreate.py BRUSH_FILE OUTPUT_DIR\n"
            "    BRUSH_FILE: Path to the .brush file\n"
            "    OUTPUT_DIR: Directory to extract the contents\n")


def check_args():
    if len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments.\n" + usage())
    if not os.path.isfile(sys.argv[1]):
        raise ValueError(f"Zip file does not exist: {sys.argv[1]}")
    # OUTPUT_DIR will be created if it does not exist

    
def main():
    if len(sys.argv) == 1:
        print(usage())
        return
    
    check_args()
    zip_file_path = sys.argv[1]
    extract_dir = sys.argv[2]

    os.makedirs(extract_dir, exist_ok=True)
    
    json_path = os.path.join(extract_dir, "brush.json")
    brush_info = read_procreate_brush(zip_file_path, extract_dir)
    write_brush_json(brush_info, json_path)


if __name__ == "__main__":
    main()
