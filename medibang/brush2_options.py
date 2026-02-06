# Translate options to their human-readable form
OPTIONS = {
    "name": "name",
    "type": "type",  # only "bitmap" is supported
    "width": "width",  # in pixels
    "min": "minimumBrushSize",  # range 0.0 to 1.0
    "opacity": "opacity",
    "psize": "pressureChangesSize",  # true or false
    "palpha": "pressureChangesOpacity",  # true or false
    "bitmapfile": "bitmapfile",
    "option": "brushSpacing",  # range 2 to 100
    "option2": "doRotateAlong",  # 0 or 1
    "option3": "rotateAngle",  # range 0 to 100 (displayed in UI as -50 to 50)
    "option4": "randomRotateAngle",  # range 0 to 100
    "option5": "applyForegroundColor",  # 0 or 1
    "option6": "colorJitter",  # range 0 to 100
    "option7": "hueJitter",  # range 0 to 100
}

REVERSE_OPTIONS = {v: k for k, v in OPTIONS.items()}

# Options that we remove during loading and add back during saving.
MEDIBANG_SPECIFIC = {
    # option: default_value
    "group": "-1",
    "cloudid": "-1",
    "clouduuid": "",
}
