def reverse_translation(translation: dict):
    return {val: key for key, val in translation.items()}


def translate(translation: dict, key: str):
    # Translate if we can, otherwise leave it alone
    return translation.get(key, key)


def translate_options(translation: dict, brush_info: list[dict]):
    return [
        {translate(translation, key): val for key, val in options.items()}
        for options in brush_info
    ]


def encode_options(translation: dict, brush_info: list[dict]):
    encoding = reverse_translation(translation)
    return [
        {translate(encoding, key): val for key, val in options.items()}
        for options in brush_info
    ]


def add_options(app_specific: dict, brush_info: list[dict]):
    return [
        {**options, **app_specific}
        for options in brush_info
    ]


def remove_options(app_specific: dict, brush_info: list[dict]):
    return [
        {key: val for key, val in options.items() if key not in app_specific}
        for options in brush_info
    ]
