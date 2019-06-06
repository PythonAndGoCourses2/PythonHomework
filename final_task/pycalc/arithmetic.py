def subtraction(first_parameter, second_parameter):
    return float(first_parameter) - float(second_parameter)


def add(first_parameter, second_parameter):
    return float(first_parameter) + float(second_parameter)


def multiply(first_parameter, second_parameter):
    return float(first_parameter) * float(second_parameter)


def division(first_parameter, second_parameter):
    if float(second_parameter) == 0:
        return "Error: division by zero"
    return float(first_parameter) / float(second_parameter)


def power(first_parameter, second_parameter):
    return float(first_parameter) ** float(second_parameter)


def integer_division(first_parameter, second_parameter):
    return float(first_parameter) // float(second_parameter)


def modulo_division(first_parameter, second_parameter):
    return float(first_parameter) % float(second_parameter)
