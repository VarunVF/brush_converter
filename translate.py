def reverse_translation(translation: dict):
    return {val: key for key, val in translation.items()}


def translate(translation: dict, key: str):
    # Translate if we can, otherwise leave it alone
    return translation.get(key, key)


def translate_options(translation: dict, brush_info: dict):
    return {
        section: {translate(translation, key): val for key, val in options.items()}
        for section, options in brush_info.items()
    }


def encode_options(translation: dict, brush_info: dict):
    encoding = reverse_translation(translation)
    return {
        section: {translate(encoding, key): val for key, val in options.items()}
        for section, options in brush_info.items()
    }


def add_options(app_specific: dict, brush_info: dict):
    return {
        section: {**options, **app_specific}
        for section, options in brush_info.items()
    }


def remove_options(app_specific: dict, brush_info: dict):
    return {
        section: {key: val for key, val in options.items() if key not in app_specific}
        for section, options in brush_info.items()
    }
