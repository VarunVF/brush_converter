import json


def read_brush_json(filepath: str) -> list[dict]:
    with open(filepath, "r") as f:
        brush_info = json.load(f)
    return brush_info


def write_brush_json(brush_info: list[dict], filepath: str):
    with open(filepath, "w") as f:
        json.dump(brush_info, f, indent=4)
