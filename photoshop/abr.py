import os

from io import BufferedReader
from PIL import Image, ImageOps


def pack_uint(f: BufferedReader, byte_length: int):
    pattern = f.read(byte_length)
    if len(pattern) != byte_length:
        return None  # Reached EOF

    return int.from_bytes(pattern, "big", signed=False)


def pack_int(f: BufferedReader, byte_length: int):
    pattern = f.read(byte_length)
    if len(pattern) != byte_length:
        return None  # Reached EOF

    return int.from_bytes(pattern, "big", signed=True)


def read_int8(f: BufferedReader):
    return pack_int(f, 1)


def read_uint8(f: BufferedReader):
    return pack_uint(f, 1)


def read_uint16(f: BufferedReader):
    return pack_uint(f, 2)


def read_uint32(f: BufferedReader):
    return pack_uint(f, 4)


def align(position: int, boundary: int = 4):
    aligned_position = position
    if position % boundary != 0:
        aligned_position += boundary - (position % boundary)
    return aligned_position


class BinaryParser:
    POSSIBLE_DEPTH_VALUES: tuple[int] = (8, 32)
    MINOR_V1_METADATA_LENGTH: int = 47
    MINOR_V2_METADATA_LENGTH: int = 301

    def __init__(self, abr_file: str, output_dir: str):
        self.abr_file = abr_file
        self.output_dir = output_dir

        self.bitmaps: list[bytes] = []
        self.brush_info: list[dict] = []
    
    def parse(self) -> list[dict]:
        with open(self.abr_file, "rb") as f:
            # Header validation
            version_major = read_uint16(f)
            version_minor = read_uint16(f)
            if version_major != 10:
                raise RuntimeError(f"Unsupported ABR version: {version_major}")
            
            print(f"Photoshop .abr version {version_major}.{version_minor}")

            # Skip to the "container" for all brushes
            if not self._skip_to_samp_section(f):
                raise RuntimeError("Could not find '8BIMsamp' section")
            
            samp_section_size = read_uint32(f)
            samp_section_end = f.tell() + samp_section_size
            
            index = 1
            while f.tell() < samp_section_end:
                brush_size = read_uint32(f)
                if brush_size == 0 or brush_size is None:
                    break
                
                next_brush_pos = align(f.tell() + brush_size)
                brush_data = self._parse_single_brush(f, index, brush_size, version_minor)
                
                if brush_data:
                    self.bitmaps.append(brush_data["pixels"])
                    self.brush_info.append(self._make_brush_settings(index, brush_data))
                    index += 1

                # Always jump to the next brush start, even if extraction failed
                f.seek(next_brush_pos)
        
        return self.brush_info
    
    def save_brush_images(self):
        for i, bitmap in enumerate(self.bitmaps):
            settings = self.brush_info[i]
            width, height = settings["width"], settings["height"]
            depth = settings["depth"]

            try:
                if depth == 8:
                    img = Image.frombytes("L", (width, height), bitmap)
                    img = ImageOps.invert(img)
                elif depth == 32:
                    pixels = bytearray()
                    alpha = bytearray()
                    for i in range(0, len(bitmap), 4):
                        pixels += bitmap[i:i+3]
                        alpha.append(bitmap[i+3])
                    rgb_img = Image.frombytes('RGB', (width, height), pixels)
                    alpha_img = Image.frombytes('L', (width, height), alpha)
                    img = Image.merge('RGBA', (rgb_img.split()[0], rgb_img.split()[1], rgb_img.split()[2], alpha_img))
                else:
                    print(f"Unknown bit depth {depth} for bitmap")
                
                filename = settings["bitmapfile"]
                img.save(
                    os.path.join(self.output_dir, filename),
                    compress_level=1  # Faster compression
                )
                
            except Exception as e:
                print(f"Failed to save bitmap {i}: {e}")

    def _parse_single_brush(self, f: BufferedReader, index: int, brush_size: int, version_minor: int):
        """Internal helper to locate dimensions and extract pixel data."""
        start_pos = f.tell()
        
        if version_minor == 1:
            f.seek(BinaryParser.MINOR_V1_METADATA_LENGTH, os.SEEK_CUR)
        elif version_minor == 2:
            f.seek(BinaryParser.MINOR_V2_METADATA_LENGTH, os.SEEK_CUR)
        else:
            # Some other minor version, we need to scan for valid-looking dimensions
            found_offset = self._find_brush_offset(f, start_pos, brush_size)
            if found_offset is None:
                print(f"Could not locate brush data for brush {index}")
                return None
            f.seek(start_pos + found_offset)

        y_min, x_min = read_uint32(f), read_uint32(f)
        y_max, x_max = read_uint32(f), read_uint32(f)
        depth = read_uint16(f)
        are_pixels_compressed = read_uint8(f)
        
        width, height = x_max - x_min, y_max - y_min
        if width <= 0 or height <= 0:
            return None

        if not are_pixels_compressed:
            pixels = f.read(width * height * (depth // 8))
        else:
            pixels = self._decode_pixels(f, width, height)
            
        return {
            "width": width,
            "height": height,
            "depth": depth,
            "pixels": pixels
        }

    @staticmethod
    def _find_brush_offset(f: BufferedReader, start_pos: int, brush_size: int):
        """Internal helper for the 'guessing' logic for unknown minor versions."""

        start = 0
        stop = 512 if brush_size > 512 else brush_size
        step = 32 // 8
        for offset in range(start, stop, step):
            f.seek(start_pos + offset)
            y_min, x_min = read_uint32(f), read_uint32(f)
            y_max, x_max = read_uint32(f), read_uint32(f)
            depth = read_uint16(f)
            
            width, height = x_max - x_min, y_max - y_min
            if 0 < width < 10000 and 0 < height < 10000:
                if depth in BinaryParser.POSSIBLE_DEPTH_VALUES:
                    return offset
        return None

    @staticmethod
    def _skip_to_samp_section(f: BufferedReader) -> bool:
        """Seek `f` to the nearest 8BIM section of the 'samp' type."""

        while True:
            marker = f.read(4) 
            if len(marker) != 4:
                return False  # Reached EOF without finding 'samp'
            if marker != b"8BIM":
                return False  # Corrupted file / unexpected padding
            
            kind = f.read(4)
            if len(kind) < 4:
                return False  # Reached EOF
            
            if kind == b"samp":
                return True  # Found the target
            else:
                # Skip to the end of this unwanted section
                section_length = read_uint32(f)
                if section_length is None:
                    return False  # Reached EOF
                
                f.seek(section_length, os.SEEK_CUR)

    def _make_brush_settings(self, brush_index: int, brush_data: dict) -> dict:
        filename = os.path.basename(self.abr_file)
        filename_no_ext = os.path.splitext(filename)[0]
        brush_name = f"{filename_no_ext}_{brush_index}"

        return {
            # We cannot get brush settings from the file.
            # Try to provide somewhat reasonable defaults.
            "name": brush_name,
            "type": "bitmap",
            "width": brush_data["width"],
            "minimumBrushSize": 0.0,
            "opacity": 1,
            "pressureChangesSize": True,
            "pressureChangesOpacity": False,
            "bitmapfile": f"{brush_name}.png",
            "brushSpacing": 25,
            "doRotateAlong": 1,
            "rotateAngle": 50,
            "randomRotateAngle": 0,
            "applyForegroundColor": 1,
            "colorJitter": 0,
            "hueJitter": 0,

            # "Extra" settings to be used later on
            "height": brush_data["height"],
            "depth": brush_data["depth"],
        }

    @staticmethod
    def _decode_pixels(f: BufferedReader, width: int, height: int) -> bytes:
        # Read the Scanline Table (2 bytes per row)
        # This table tells us the compressed length of every single row.
        scanline_bytes = f.read(2 * height)
        scanline_lengths = []
        for i in range(0, 2 * height, 2):
            row_length = int.from_bytes(scanline_bytes[i : i + 2], "big")
            scanline_lengths.append(row_length)
        
        decoded = bytearray(width * height)
        curr_pos = 0

        # Read all the rows at once
        data = f.read(sum(scanline_lengths))
        data_ptr = 0
        for row_length in scanline_lengths:
            row_data = data[data_ptr : data_ptr + row_length]
            data_ptr += row_length
            row_ptr = 0
            
            while row_ptr < row_length:
                n_byte = row_data[row_ptr]
                row_ptr += 1
                
                # Convert unsigned byte to signed (-128 to 127)
                n = n_byte if n_byte <= 127 else n_byte - 256

                if 0 <= n <= 127:
                    # Copy next n+1 bytes literally
                    count = n + 1
                    decoded[curr_pos : curr_pos + count] = row_data[row_ptr : row_ptr + count]
                    curr_pos += count
                    row_ptr += count
                elif n != -128:
                    # Repeat next byte -n+1 times
                    count = -n + 1
                    byte_val = row_data[row_ptr : row_ptr + 1]
                    decoded[curr_pos : curr_pos + count] = byte_val * count
                    curr_pos += count
                    row_ptr += 1
                    
        return bytes(decoded)

def read_abr(abr_file: str, output_dir: str) -> list[dict]:
    os.makedirs(output_dir, exist_ok=True)

    with open(abr_file, "rb") as f:
        parser = BinaryParser(abr_file, output_dir)
        brush_info = parser.parse()
        parser.save_brush_images()
        return brush_info
