import black


def python_prettify(code: str, options: dict):
    line_length = options["line_length"]
    string_normalization = options["string_normalization"]
    magic_trailing_comma = options["magic_trailing_comma"]
    try:
        return (
            black.format_str(
                code,
                mode=black.Mode(
                    line_length=line_length,
                    string_normalization=string_normalization,
                    magic_trailing_comma=magic_trailing_comma,
                ),
            ),
            True,
        )
    except black.parsing.InvalidInput:
        return code, False


def default_prettify(code: str, options: dict):
    return code, True


prettify_by_name = {"python": python_prettify}


def get_prettifier_by_name(name):
    return prettify_by_name.get(name.lower(), default_prettify)
