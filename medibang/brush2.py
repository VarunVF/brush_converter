import configparser


def clamp_brush_spacing(spacing: int):
    return max(2, min(spacing, 100))


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
    for brush, options in brush_info.items():
        options["brushSpacing"] = clamp_brush_spacing(options["brushSpacing"])

    config = configparser.ConfigParser()
    config.read_dict(brush_info)
    with open(filepath, "w") as f:
        config.write(f, space_around_delimiters=False)
