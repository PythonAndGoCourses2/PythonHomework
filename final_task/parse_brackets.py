import calculate_expression


def parse_brackets(value):
    result = []
    temp = ""
    is_calculate_expression = False
    counter_value = 1
    for item in value:
        if item == '(' or item == ')':
            if item == ')':
                temp += item
            if len(temp) > 0:
                if temp.find('(') != -1 and temp.find(')') != -1:
                    temp = temp.replace('(', '').replace(')', '')
                    if len(result) > 0:
                        if result[-1].find('(') != -1:
                            temp = result[-1] + str(calculate_expression.calculate(temp))
                            del result[-1]
                        else:
                            temp = str(calculate_expression.calculate(temp))
                            result.append(temp)
                            temp = ""
                        is_calculate_expression = True
                    else:
                        temp = str(calculate_expression.calculate(temp))
                        result.append(temp)
                else:
                    result.append(temp)
                    temp = ""
        else:
            if len(value) == counter_value:
                temp += item
                result.append(temp)
        temp += item
        if item == ')' and not is_calculate_expression:
            temp = ""
        elif is_calculate_expression:
            temp = temp[:-1]
            is_calculate_expression = False
        counter_value += 1
    result = ''.join(result)
    return result
