import json
import os
import plistlib
import sys
import zipfile


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


def build_brush_info(plist_data: dict, bitmap_filename: str) -> dict:
    # TODO verify this mapping
    options_array = plist_data["$objects"][1]
    
    return {
        "name": plist_data["$objects"][4],
        "type": "bitmap",
        "width": options_array["paintSize"],
        "minimumBrushSize": options_array["taperSize"],  # this is a guess
        "opacity": options_array["paintOpacity"],
        "pressureChangesSize": options_array["dynamicsPressureSize"],
        "pressureChangesOpacity": options_array["dynamicsPressureOpacity"],
        "bitmapfile": bitmap_filename,
        "brushSpacing": options_array["plotSpacing"],
        "doRotateAlong": 0,
        "rotateAngle": 50,
        "randomRotateAngle": 0,
        "applyForegroundColor": 1,
        "colorJitter": 0,
        "hueJitter": 0,
    }

    
def main():
    if len(sys.argv) == 1:
        print(usage())
        return
    
    check_args()

    zip_file_path = sys.argv[1]
    extract_dir = sys.argv[2]

    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extract('Shape.png', extract_dir)
        zip_ref.extract('Brush.archive', extract_dir)

    brush_archive_path = os.path.join(extract_dir, 'Brush.archive')
    with open(brush_archive_path, 'rb') as f:
        plist_data: dict = plistlib.load(f)

    brush_info = []
    brush_info.append(build_brush_info(plist_data, 'Shape.png'))
    json_path = os.path.join(extract_dir, 'brush.json')
    with open(json_path, 'w') as json_file:
        json.dump(brush_info, json_file, indent=4)


if __name__ == "__main__":
    main()
