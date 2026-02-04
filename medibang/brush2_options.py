# Translate options to their human-readable form
FORWARD_TRANSLATION = {
    "min": "minimumBrushSize",  # range 0.0 to 1.0
    "psize": "pressureChangesSize",  # true or false
    "palpha": "pressureChangesOpacity",  # true or false
    "option": "brushSpacing",  # range 2 to 100
    "option2": "doRotateAlong",  # 0 or 1
    "option3": "rotateAngle",  # range 0 to 100 (displayed in UI as -50 to 50)
    "option4": "randomRotateAngle",  # range 0 to 100
    "option5": "applyForegroundColor",  # 0 or 1
    "option6": "colorJitter",  # range 0 to 100
    "option7": "hueJitter",  # range 0 to 100
}

# Reverse the mapping of keys to values
BACKWARD_TRANSLATION = {val: key for key, val in FORWARD_TRANSLATION.items()}


def translate(key: str):
    # Translate if we can, otherwise leave it alone
    return FORWARD_TRANSLATION.get(key, key)


def encode(key: str):
    return BACKWARD_TRANSLATION.get(key, key)


def translate_options(brush_info: dict):
    return {
        section: {translate(key): val for key, val in options.items()}
        for section, options in brush_info.items()
    }


def encode_options(brush_info: dict):
    return {
        section: {encode(key): val for key, val in options.items()}
        for section, options in brush_info.items()
    }
