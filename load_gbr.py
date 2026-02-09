import os
import sys

from gimp.gbr import read_gbr
from brush_json import write_brush_json


def usage():
    return ("Usage: python load_gbr.py GBR_FILE OUTPUT_JSON"
            "    GBR_FILE  : Path to the gbr file"
            "    OUTPUT_DIR: Directory to write the output json and png files")


def check_args():
    if len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments.\n" + usage())
    if not os.path.isfile(sys.argv[1]):
        raise ValueError(f"GBR file does not exist: {sys.argv[1]}")
    # OUTPUT_DIR will be created if it does not exist


def load_gbr(gbr_file_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    brush_info, img, bitmap_filename = read_gbr(gbr_file_path)
    json_path = os.path.join(output_dir, "brush.json")
    image_path = os.path.join(output_dir, bitmap_filename)

    # Translation not applicable for this format.
    write_brush_json(brush_info, json_path)
    img.save(image_path, "PNG")    


def main():
    if len(sys.argv) == 1:
        print(usage())
        return
    
    check_args()
    gbr_file_path = sys.argv[1]
    output_dir = sys.argv[2]
    load_gbr(gbr_file_path, output_dir)


if __name__ == "__main__":
    main()
