import math as m

func_dictionary = {'sin': m.sin, 
                   'cos': m.cos, 
                   'tan': m.tan, 
                   'atan': m.atan, 
                   'asin': m.asin, 
                   'acos': m.acos, 
                   'degrees': m.degrees, 
                   'radians': m.radians, 
                   'exp': m.exp, 
                   'sqrt': m.sqrt, 
                   'log': m.log, 
                   'log10': m.log10, 
                   'fabs': m.fabs, 
                   'round': round, 
                   'fsum': m.fsum, 
                   'frexp': m.frexp,
                   'ceil': m.ceil,
                   'copysigh': m.copysign,
                   'floor': m.floor,
                   'fmod': m.fmod,
                   'gcd': m.gcd,
                   'isclose': m.isclose,
                   'isfinite': m.isfinite,
                   'isinf': m.isinf,
                   'isnan': m.isnan,
                   'ldexp': m.ldexp,
                   'remainder': m.remainder,
                   'trunc': m.trunc,
                   'pow': m.pow,
                   'abs': abs
                   }


def skip_space(eval_string, index): 
    while index < len(eval_string) and eval_string[index] == ' ':
        index += 1
    if index > len(eval_string):
        raise ValueError("ERROR: invalid argument")
    return index


def wrapper(Func, Args):
    try:
        return Func(*Args)
    except Exception as err:
        print("ERROR: {}".format(err))


def get_arguments(eval_string, index):
    params = []
    while index < len(eval_string) and eval_string[index] != ')':
        temp = solve_equality(eval_string, index) 
        index = temp[1] 
        index = skip_space(eval_string, index)
        if index < len(eval_string) and eval_string[index] not in (',', ')'): 
            raise ValueError("ERROR: no zapyataya")
        elif index < len(eval_string) and eval_string[index] == ',': 
            index += 1
        params.append(temp[0]) 
    if index < len(eval_string) and eval_string[index] == ')':
        return params, index
    else:
        raise ValueError('ERROR: no closing bracket')


def error(args): 
    raise Exception("ERROR: invalid argument") 


def search_float(eval_string, index): 
    num = ""  
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == '-':  
        num = '-'  
        index += 1
    index = skip_space(eval_string, index)
    while index < len(eval_string): 
        if eval_string[index].isdigit():  
            num += eval_string[index]  
            index += 1
        elif (eval_string[index].isalpha()):  
            raise ValueError("""ERROR: РѕР±РЅР°СЂСѓР¶РµРЅ РЅРµРёР·РІРµСЃС‚РЅС‹Р№ СЃРёРјРІРѕР» {} РЅР° РїРѕР·РёС†РёРё {}""".format(
                                                                                                       eval_string[index], index))
        else:
            break 
    if (index < len(eval_string) and eval_string[index] == '.'): 
        num += eval_string[index] 
        index += 1 
        while index < len(eval_string):
            if eval_string[index].isdigit():
                num += eval_string[index] 
                index += 1
            else:
                break
        return (float(num), index) 
    else:
        return (int(num), index) 


def get_bracket(eval_string, index): 
    result, num1 = 0, 0
    index += 1
    result, index = solve_equality(eval_string, index) 
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == ')': 
        index += 1 
        return result, index
    else: 
        raise ValueError("ERROR: РІС‹ Р·Р°Р±С‹Р»Рё РґРѕР±Р°РІРёС‚СЊ Р·Р°РєСЂС‹РІР°СЋС‰СѓСЋ СЃРєРѕР±РєСѓ РЅР° РїРѕР·РёС†РёРё {}".format(index))


def znak(eval_string, index):
    if eval_string[index] == '+': 
        index += 1 
        if index >= len(eval_string): 
            raise ValueError("ERROR: РѕР¶РёРґР°Р»СЃСЏ РѕРїРµСЂР°РЅРґ")
        
        result, index = get_variable(eval_string, index) 
    elif eval_string[index] == '-': 
        index += 1
        if index >= len(eval_string):
            raise ValueError("ERROR: РѕР¶РёРґР°Р»СЃСЏ РѕРїРµСЂР°РЅРґ")
        result, index = get_variable(eval_string, index)
        result *= -1
    return result, index
       
       
def get_variable(eval_string, index): 
    index = skip_space(eval_string, index)
    variable = "" 
    if index < len(eval_string) and (eval_string[index].isdigit() or eval_string[index] == '.'): 
        variable, index = search_float(eval_string, index)
        index = skip_space(eval_string, index)
        if index < len(eval_string) and eval_string[index] not in (
                                           '+', '-', '*', '/', '%', '^', 
                                           '>', '<','=', ')', '!', ','
                                           ): 
            raise ValueError("ERROR: РѕР¶РёРґР°Р»СЃСЏ РѕРїРµСЂР°С‚РѕСЂ")
    elif index < len(eval_string) and eval_string[index] in ('-','+'):
        variable, index = znak(eval_string, index)
    elif index < len(eval_string) and eval_string[index] == '(':
        variable, index = get_bracket(eval_string, index)
    elif index < len(eval_string) and eval_string[index].isalpha():  
        str = "" 
        while index < len(eval_string) and (eval_string[index].isalpha() or eval_string[index].isdigit()): 
            str += eval_string[index]
            index += 1
        if (str == 'pi'):
            variable = m.pi
        elif (str == 'e'):
            variable = m.e
        elif (str == 'tau'):
            variable = m.tau
        else: 
            if index < len(eval_string) and eval_string[index] == '(':
                index += 1
                tmp = get_arguments(eval_string, index)  
                variable = wrapper(func_dictionary.get(str.lower(), error), tmp[0])
                index = tmp[1]
                if index < len(eval_string) and eval_string[index] == ')':
                    index += 1
                    index = skip_space(eval_string, index)
            else:  
                raise ValueError("ERROR: Invalid argument (index {})".format(index))
    elif index < len(eval_string) and eval_string[index] == ',':
        return variable, index
    else:
        raise ValueError("ERROR: РѕР±РЅР°СЂСѓР¶РµРЅ РЅРµРёР·РІРµСЃС‚РЅС‹Р№ СЃРёРјРІРѕР» РЅР° РїРѕР·РёС†РёРё {}".format(index))
    return (variable, index)


def get_degree(eval_string, index):
    result, num1, index = 0, 0, skip_space(eval_string, index)
    result, index = get_variable(eval_string, index) 
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == '^':
        index += 1
        num1, index = get_degree(eval_string, index) 
        if (result == 0 and num1 == 0): 
            raise ValueError("ERROR: РІРѕР·РІРµРґРµРЅРёРµ 0 РІ СЃС‚РµРїРµРЅСЊ 0 (РїРѕР·РёС†РёСЏ {})".format(index))
        result **= num1
        index = skip_space(eval_string, index)
    return result, index


def multiply(eval_string, index):
    mult, num1, index = 1, 0, skip_space(eval_string, index)
    mult, index = get_degree(eval_string, index) 
    index = skip_space(eval_string, index)
    while index < len(eval_string) and eval_string[index] in ("*", "/", "%"): 
        znak = ""
        while eval_string[index] in ("*", "/", "%"): 
            znak += eval_string[index]
            index += 1
        num1, index = get_degree(eval_string, index)
        if (znak == '*'):
            mult *= num1
        elif (znak == '/'):
            mult /= num1
        elif (znak == "//"):
            mult //= num1
        elif (znak == '%'):
            mult %= num1
        else:
            raise ValueError("ERROR: РЅРµРёР·РІРµСЃС‚РЅС‹Р№ РѕРїРµСЂР°С‚РѕСЂ (РїРѕР·РёС†РёСЏ {})".format(index))
        index = skip_space(eval_string, index)
    return mult, index

    
def sum(eval_string, index):
    sum, num1 = 0, 0
    sum, index = multiply(eval_string, index)
    index = skip_space(eval_string, index)
    while index < len(eval_string) and eval_string[index] in ("+", "-"):
        znak = eval_string[index]
        index += 1
        num1, index = multiply(eval_string, index)
        if(znak == '+'):
            sum += num1
        elif(znak == '-'):
            sum -= num1
        index = skip_space(eval_string, index)
    return sum, index


def solve_equality(eval_string, index):
    num1, num2, znak = 0, 0, ""
    num1, index = sum(eval_string, index) 
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] not in (">", "=", "<", "!", ")", ","):
        raise Exception("ERROR: РѕР±РЅР°СЂСѓР¶РµРЅ РЅРµРёР·РІРµСЃС‚РЅС‹Р№ СЃРёРјРІРѕР» {} РЅР° РїРѕР·РёС†РёРё {}".format(
                                                                                              eval_string[index], index))
    while index < len(eval_string) and eval_string[index] in (">", "=", "<", "!"):
        while index < len(eval_string) and eval_string[index] in ('>', '=', '<', '!'):
           znak += eval_string[index]
           index += 1
        num2, index = sum(eval_string, index)
        if (znak == '>='):
            result = (num1 >= num2)
        elif (znak == '>'):
            result = (num1 > num2)
        elif (znak == '=='):
            result = (num1 == num2)
        elif (znak == '<'):
            result = (num1 < num2)
        elif (znak == '<='):
            result = (num1 <= num2)
        elif (znak == '!='):
            result = (num1 != num2)
        else:
            raise ValueError("ERROR: РЅРµРёР·РІРµСЃС‚РЅС‹Р№ РѕРїРµСЂР°С‚РѕСЂ")
        return result, index
    return num1, index


def solve(eval_string, index = 0):
    index = skip_space(eval_string, index)
    if index >= len(eval_string):
        raise ValueError("ERROR: РІС‹ РЅРёС‡РµРіРѕ РЅРµ РІРІРµР»Рё")
    result, index = solve_equality(eval_string, index) 
    return result