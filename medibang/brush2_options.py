# Translate options to their human-readable form
OPTIONS = {
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

# Options that we remove during loading and add back during saving.
MEDIBANG_SPECIFIC = {
    # option: default_value
    "group": "-1",
    "cloudid": "-1",
    "clouduuid": "",
}
