import os
import plistlib
import zipfile


def build_brush_info(plist_data: dict, bitmap_filename: str) -> dict:
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


def read_procreate_brush(zip_file_path: str, extract_dir: str) -> list[dict]:
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        # Brush.png doesn't always exist; this means the brush derives from Procreate's built-in shapes.
        # We cannot convert such brushes without the bitmap.
        if "Shape.png" not in zip_ref.namelist():
            raise ValueError("Brush file cannot be converted because it does not contain a Shape.png bitmap")
        
        zip_ref.extract("Shape.png", extract_dir)
        zip_ref.extract("Brush.archive", extract_dir)

    brush_archive_path = os.path.join(extract_dir, "Brush.archive")
    with open(brush_archive_path, "rb") as f:
        plist_data: dict = plistlib.load(f)

    for key, value in plist_data.items():
        print(f"{key}: {value}")
    
    os.remove(brush_archive_path)
    new_shape_filename = f"{plist_data['$objects'][4]}.png"
    if os.path.exists(os.path.join(extract_dir, new_shape_filename)):
        raise ValueError(f"Cannot rename Shape.png to {new_shape_filename} because the file already exists")
    os.rename(os.path.join(extract_dir, "Shape.png"),
              os.path.join(extract_dir, new_shape_filename))

    return [
        build_brush_info(plist_data, new_shape_filename)
    ]


def create_plist_data(brush: dict) -> dict:
    return {
        "$version": 100000,
        "$objects": [
            None,
            {
                # TODO fill in actual values from brush, after normalizing/scaling as needed.
                # possible mappings:
                # "paintSize": brush["width"],
                # "taperSize": brush["minimumBrushSize"],
                # "paintOpacity": brush["opacity"],
                # "dynamicsPressureSize": brush["pressureChangesSize"],
                # "dynamicsPressureOpacity": brush["pressureChangesOpacity"],
                # "plotSpacing": brush["brushSpacing"],

                'shapeOrientation': 1,
                'paintSize': 0.2,
                'shapeRotation': 0.0,
                'textureRotation': 1.0,
                'smudgeOpacity': 0.7,
                'textureInverted': False,
                'plotJitter': 0.2,
                'stamp': False,
                'dynamicsFalloff': 0.0,
                'maxSize': 2.7,
                'eraseOpacity': 0.7,
                'paintOpacity': 1.0,
                'taperSize': 0.0,
                'dynamicsPressureSize': 0.0,
                'bundledShapePath': plistlib.UID(0),
                'taperOpacity': 0.0,
                'plotSpacing': 0.1,
                'textureOrientation': 1,
                'dynamicsJitterOpacity': 0.7,
                'oriented': False,
                'textureMovement': 1.0,
                'shapeRandomise': True,
                'taperEndLength': 0.0,
                'dynamicsSpeedSize': 0.0,
                'textureFilter': True,
                'bundledGrainPath': plistlib.UID(2),
                'shapeAzimuth': False,
                'dynamicsTiltAngle': 0.0,
                'dynamicsTiltSize': 0.0,
                'dynamicsTiltOpacity': 0.0,
                'dynamicsJitterSize': 1.0,
                'maxOpacity': 1.0,
                'minSize': 0.4,
                'name': plistlib.UID(4),
                '$class': plistlib.UID(5),
                'color': plistlib.UID(3),
                'shapeInverted': False,
                'dynamicsPressureSpeed': 0.0,
                'dynamicsPressureOpacity': 0.0,
                'minOpacity': 0.0,
                'dynamicsGlazeType': 0,
                'dynamicsLoad': 0.0,
                'taperStartLength': 0.0,
                'smudgeSize': 0.7,
                'shapeScatter': 0.0,
                'plotSmoothing': 0.6,
                'dynamicsMix': 0.0,
                'dynamicsGlazeFlow': 1.0,
                'eraseSize': 0.7,
                'textureZoom': 0.0,
                'textureScale': 2.6,
                'dynamicsSpeedOpacity': 0.0,
            },
            None,  # "bundledGrainPath"
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',  # "color"
            brush["name"],  # "name"
            {
                "$classname": "SilicaBrush",
                "$classes": ["SilicaBrush", "NSObject"],
            },  # "$class"
        ],
        "$archiver": "NSKeyedArchiver",
        "$top": {
            "root": plistlib.UID(1),
        },
    }


def write_procreate_brush(brush_info: list[dict], bitmap_dir: str, output_dir: str):
    # - Create output_dir if it doesn't exist
    # - For each brush in brush_info:
    #   - Open a zip file with .brush extension in output_dir containing:
    #    - "Brush.archive": brush_info converted to bplist
    #    - "Shape.png": Bitmap file copied from from bitmap_dir
    #    - "QuickLook/Thumbnail.png": placeholder for now (might be optional?)

    os.makedirs(output_dir, exist_ok=True)

    for brush in brush_info:
        brush_name = brush["name"]
        brush_filename = f"{brush_name}.brush"
        brush_path = os.path.join(output_dir, brush_filename)

        with zipfile.ZipFile(brush_path, "w") as zip_ref:
            plist_data = create_plist_data(brush)

            brush_archive_data = plistlib.dumps(plist_data, fmt=plistlib.FMT_BINARY)
            zip_ref.writestr("Brush.archive", brush_archive_data)

            bitmap_file_path = os.path.join(bitmap_dir, brush["bitmapfile"])
            zip_ref.write(bitmap_file_path, arcname="Shape.png")

            # Add placeholder for QuickLook/Thumbnail.png
            # TODO: generate actual thumbnail
            zip_ref.writestr("QuickLook/Thumbnail.png", b"")
