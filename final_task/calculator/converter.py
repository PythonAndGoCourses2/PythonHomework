from regexp import has_non_zero_fraction_part

def convert_answer(expr: str, has_compare: bool) -> str:
    """
    Converts the resulting string to the desired type.

    Args:
        expr (str): String representation of a number.
    """
    num = float(expr)
    match = has_non_zero_fraction_part(expr)
    num = num if match else int(num)

    answer = bool(num) if has_compare else num

    return str(answer)
