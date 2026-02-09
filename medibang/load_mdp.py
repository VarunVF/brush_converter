import os
import sys
import shutil

from medibang.brush2 import read_brush2
from medibang.brush2_options import OPTIONS, MEDIBANG_SPECIFIC
from translate import translate_options, remove_options
from brush_json import write_brush_json


def usage():
    return ("Usage: python load_mdp.py MEDIBANG_DIR OUTPUT_JSON\n"
            "    MEDIBANG_DIR: Path to the MediBang app data directory\n"
            "    OUTPUT_DIR: Path to the directory to write the output json and png files\n")


def check_args(medibang_dir: str, brush2_file: str):
    if not os.path.isdir(medibang_dir):
        raise ValueError(f"Folder does not exist: {medibang_dir}")
    if not os.path.isfile(brush2_file):
        raise ValueError(f"File does not exist: {brush2_file}")
    # OUTPUT_DIR will be created if it does not exist


def copy_all_files(source_dir, destination_dir):
    os.makedirs(destination_dir, exist_ok=True)
    
    files = os.listdir(source_dir)    
    for file_name in files:
        source_path = os.path.join(source_dir, file_name)
        destination_path = os.path.join(destination_dir, file_name)
        
        if os.path.isfile(source_path):
            try:
                # Copy data and metadata
                shutil.copy2(source_path, destination_path)
                print(f"Copied: {file_name}")
            except shutil.SameFileError:
                print(f"Skipped (same file): {file_name}")
            except PermissionError:
                print(f"Skipped (permission denied): {file_name}")
            except Exception as e:
                print(f"An error occurred while copying {file_name}: {e}")


def load_mdp(medibang_dir: str, brush2_file: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    brush_info = read_brush2(brush2_file)
    brush_info = remove_options(MEDIBANG_SPECIFIC, brush_info)
    brush_info = translate_options(OPTIONS, brush_info)
    output_file_path = os.path.join(output_dir, "brush.json")
    write_brush_json(brush_info, output_file_path)
    medibang_bitmap_dir = os.path.join(medibang_dir, "brush_bitmap")
    copy_all_files(medibang_bitmap_dir, output_dir)


def main():
    if len(sys.argv) == 1:
        print(usage())
        return
    elif len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments.\n" + usage())
    
    medibang_dir = sys.argv[1]
    output_dir = sys.argv[2]
    brush2_file = os.path.join(medibang_dir, "Brush2.ini")
    check_args(medibang_dir, brush2_file)
    load_mdp(medibang_dir, brush2_file, output_dir)


if __name__ == "__main__":
    main()
