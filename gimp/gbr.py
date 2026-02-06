import os
import struct

from PIL import Image


def calculate_spacing(brush_spacing_pct: int, brush_width: int):
    return brush_spacing_pct / 100.0 * brush_width


def calculate_spacing_pct(spacing: float, brush_width: int):
    return int(spacing / brush_width * 100.0)


def read_gbr(filepath: str) -> tuple[list[dict], Image.Image, str]:
    f = open(filepath, "rb")

    header_size = struct.unpack(">I", f.read(4))[0]
    version = struct.unpack(">I", f.read(4))[0]
    brush_width = struct.unpack(">I", f.read(4))[0]
    brush_height = struct.unpack(">I", f.read(4))[0]
    color_depth = struct.unpack(">I", f.read(4))[0]
    magic_number = f.read(4)
    if (magic_number.decode() != "GIMP"):
        raise RuntimeError(f"File {filepath} is not a GIMP brush")
    brush_spacing_pct = struct.unpack(">I", f.read(4))[0]
    brush_name_size = header_size - f.tell()
    brush_name: bytes = struct.unpack(f">{brush_name_size}s", f.read(brush_name_size))[0]
    brush_name_str: str = brush_name[:-1].decode()  # remove null terminator

    print(f"GIMP version: {version}")
    print(f"Brush name: {brush_name_str}")
    print(f"Brush size: {brush_width, brush_height}")
    print(f"Color depth: {color_depth}")

    body_size = brush_width * brush_height * color_depth
    body = struct.unpack(f">{body_size}s", f.read(body_size))[0]  # unsigned char[]

    f.close()

    # Save the pixels as a PNG file
    if color_depth == 1:
        img = Image.frombytes("L", (brush_width, brush_height), body)
    elif color_depth == 4:
        img = Image.frombytes("RGBA", (brush_width, brush_height), body)
    else:
        raise RuntimeError(f"Unsupported color depth: {color_depth}")
    bitmap_filename_str = f"{brush_name_str}.png"

    # A gbr file contains info for a single brush => JSON is an array of one brush object
    brush_info = [
        {
            "name": brush_name_str,
            "type": "bitmap",
            "width": brush_width,
            "minimumBrushSize": 0.0,
            "opacity": 1,
            "pressureChangesSize": True,
            "pressureChangesOpacity": False,
            "bitmapfile": bitmap_filename_str,
            "brushSpacing": calculate_spacing(brush_spacing_pct, brush_width),
            "doRotateAlong": 1,
            "rotateAngle": 50,
            "randomRotateAngle": 0,
            "applyForegroundColor": 1,
            "colorJitter": 0,
            "hueJitter": 0,
        }
    ]

    return brush_info, img, bitmap_filename_str


def write_gbr(brush_info: list[dict], bitmap_dir: str, output_dir: str):
    # TODO update for new json structure

    for brush in brush_info:
        # Header contains: seven uint32_t (4-byte unsigned) integers + brush name (incl. null terminator)
        brush_name = brush["name"]
        brush_name_size = len(brush_name) + 1
        header_size = 7*4 + brush_name_size
        magic_number = (ord('G') << 24) + (ord('I') << 16) + (ord('M') << 8) + ord('P')
        brush_spacing_pct = calculate_spacing_pct(float(brush["brushSpacing"]), float(brush["width"]))

        # Load the PNG file as raw pixels
        # Expect the bitmap file to be in the bitmap_dir
        bitmap_filepath = os.path.join(bitmap_dir, brush["bitmapfile"])
        img = Image.open(bitmap_filepath)
        brush_width, brush_height = img.size

        # Find the bit depth
        if img.mode == "L":
            color_depth = 1
        elif img.mode == "RGBA":
            color_depth = 4
        else:
            raise RuntimeError(f"Unsupported color mode: {img.mode}")
        
        body_size = brush_width * brush_height * color_depth
        file_bytes = struct.pack(f">IIIIIII{brush_name_size}s{body_size}s",
            header_size,
            2,  # version number
            brush_width,
            brush_height,
            color_depth,
            magic_number,
            brush_spacing_pct,
            bytes(brush_name, encoding="utf-8"),
            img.tobytes()
        )

        os.makedirs(output_dir, exist_ok=True)
        output_filepath = os.path.join(output_dir, f"{brush_name}.gbr")
        with open(output_filepath, "wb") as f:
            f.write(file_bytes)

        img.close()
