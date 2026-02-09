import configparser
import os

from PIL import Image

from medibang.brush2_options import REVERSE_OPTIONS


def clamp_brush_spacing(spacing: int):
    return max(2, min(spacing, 100))


def mask_to_inverted(input_path, output_path):
    img = Image.open(input_path).convert("L")  # L = 8-bit grayscale

    # Create new bitmap image (for inversion)
    rgba = Image.new("L", img.size)
    rgba_pixels = rgba.load()
    mask_pixels = img.load()

    width, height = img.size

    for y in range(height):
        for x in range(width):
            alpha = mask_pixels[x, y]
            rgba_pixels[x, y] = (255 - alpha)  # invert bytes

    # Save inverted bitmap image
    rgba.save(output_path, "PNG")


def load_brush_keys(config: configparser.ConfigParser, section: str) -> dict:
    return {
        "name": config.get(section, REVERSE_OPTIONS["name"]),
        "type": config.get(section, REVERSE_OPTIONS["type"]),
        "bitmapfile": config.get(section, REVERSE_OPTIONS["bitmapfile"]),
        "width": config.getint(section, REVERSE_OPTIONS["width"]),
        "minimumBrushSize": config.getfloat(section, REVERSE_OPTIONS["minimumBrushSize"]),
        "opacity": config.getfloat(section, REVERSE_OPTIONS["opacity"]),
        "pressureChangesSize": config.getboolean(section, REVERSE_OPTIONS["pressureChangesSize"]),
        "pressureChangesOpacity": config.getboolean(section, REVERSE_OPTIONS["pressureChangesOpacity"]),
        "brushSpacing": config.getfloat(section, REVERSE_OPTIONS["brushSpacing"]),
        "doRotateAlong": config.getint(section, REVERSE_OPTIONS["doRotateAlong"]),
        "rotateAngle": config.getint(section, REVERSE_OPTIONS["rotateAngle"]),
        "randomRotateAngle": config.getint(section, REVERSE_OPTIONS["randomRotateAngle"]),
        "applyForegroundColor": config.getint(section, REVERSE_OPTIONS["applyForegroundColor"]),
        "colorJitter": config.getint(section, REVERSE_OPTIONS["colorJitter"]),
        "hueJitter": config.getint(section, REVERSE_OPTIONS["hueJitter"])
    }


def read_brush2(filepath: str) -> list[dict]:
    config = configparser.ConfigParser()
    config.read(filepath)

    output: list[dict] = []
    for section in config.sections():
        # We can only handle bitmap brushes for now
        if section != "General" and config[section]["type"] == "bitmap":
            brush_dict = load_brush_keys(config, section)
            output.append(brush_dict)
    
    return output


def write_brush2(brush_info: list[dict], brush_json_filepath: str, brush2_filepath: str, bitmap_dir: str):
    for brush in brush_info:
        brush_spacing_key = REVERSE_OPTIONS["brushSpacing"]
        brush[brush_spacing_key] = clamp_brush_spacing(brush[brush_spacing_key])

    # Parse the existing ini to find the next section index
    new_config = configparser.ConfigParser()
    with open(brush2_filepath, "r") as f:
        old_config = configparser.ConfigParser()
        old_config.read_file(f)
        next_section_index = len(old_config.sections()) - 1
        new_section_name = str(next_section_index)

    # Add the new brushes to the dict with the correct section name
    for brush in brush_info:
        new_section_name = str(next_section_index)
        next_section_index += 1
        new_config.add_section(new_section_name)
        for key, value in brush.items():
            new_config.set(new_section_name, key, str(value))

    # Write the new brushes to the ini file
    with open(brush2_filepath, "a") as f:
        new_config.write(f, space_around_delimiters=False)
    
    # Need to write a new image with inverted pixels for use in MediBang Paint
    print(f"New images will be created in: {bitmap_dir}")
    os.makedirs(bitmap_dir, exist_ok=True)
    for brush in brush_info:
        input_image_path = os.path.join(os.path.dirname(brush_json_filepath), brush["bitmapfile"])
        output_image_path = os.path.join(bitmap_dir, os.path.basename(input_image_path))
        mask_to_inverted(input_image_path, output_image_path)
        print(f"Saved brush image: {output_image_path}")
