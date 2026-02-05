import configparser
import os

from PIL import Image

from medibang.brush2_options import REVERSE_OPTIONS


def clamp_brush_spacing(spacing: int):
    return max(2, min(spacing, 100))


def mask_to_inverted(input_path, output_path):
    img = Image.open(input_path).convert("L")  # L = 8-bit grayscale

    # Create RGBA image
    rgba = Image.new("L", img.size)
    rgba_pixels = rgba.load()
    mask_pixels = img.load()

    width, height = img.size

    for y in range(height):
        for x in range(width):
            alpha = mask_pixels[x, y]
            rgba_pixels[x, y] = (255 - alpha)  # invert bytes

    # Save RGBA image
    rgba.save(output_path, "PNG")


def read_brush2(filepath: str) -> dict:
    config = configparser.ConfigParser()
    config.read(filepath)

    output = dict()
    for section in config.sections():
        # We can only handle bitmap brushes for now
        if section != "General" and config[section]["type"] == "bitmap":
            output[section] = dict()
            for key in config[section].keys():
                output[section][key] = config[section][key]
    
    return output


def write_brush2(brush_info: dict, brush_json_filepath: str, brush2_filepath: str, bitmap_dir: str):
    for brush, options in brush_info.items():
        brush_spacing_key = REVERSE_OPTIONS["brushSpacing"]
        options[brush_spacing_key] = clamp_brush_spacing(float(options[brush_spacing_key]))

    # Parse the existing ini to find the next section index
    new_config = configparser.ConfigParser()
    with open(brush2_filepath, "r") as f:
        old_config = configparser.ConfigParser()
        old_config.read_file(f)
        next_section_index = len(old_config.sections()) - 1
        new_section_name = str(next_section_index)

    # Add the new brushes to the dict with the correct section name
    for brush, options in brush_info.items():
        new_section_name = str(next_section_index)
        next_section_index += 1
        new_config.add_section(new_section_name)
        new_config[new_section_name] = options

    # Write the new brushes to the ini file
    with open(brush2_filepath, "a") as f:
        new_config.write(f, space_around_delimiters=False)
    
    # Need to write a new image with inverted pixels for use in MediBang Paint
    print(f"New images will be created in: {bitmap_dir}")
    os.makedirs(bitmap_dir, exist_ok=True)
    for brush, options in brush_info.items():
        # Expecting bitmap file to be relative to the brush json file
        input_image_path = os.path.join(os.path.dirname(brush_json_filepath), options["bitmapfile"])
        output_image_path = os.path.join(bitmap_dir, os.path.basename(input_image_path))
        mask_to_inverted(input_image_path, output_image_path)
        print(f"Saved brush image: {output_image_path}")
