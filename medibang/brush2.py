import configparser
import json


def read_brush2(filepath: str) -> dict:
    config = configparser.ConfigParser()
    config.read(filepath)

    output = dict()
    for section in config.sections():
        output[section] = dict()
        for key in config[section].keys():
            output[section][key] = config[section][key]
    
    return output


def write_brush2(brush_info: dict, filepath: str):
    config = configparser.ConfigParser()
    config.read_dict(brush_info)
    with open(filepath, "w") as f:
        config.write(f, space_around_delimiters=False)


def read_brush_json(filepath: str) -> dict:
    with open(filepath, "r") as f:
        brush_info = json.load(f)
    return brush_info

def write_brush_json(brush_info: dict, filepath: str):
    with open(filepath, "w") as f:
        json.dump(brush_info, f, indent=4)
