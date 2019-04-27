import math as m

"""

Данный калькулятор написан с помощью метода рекурсивного спуска

Согласно этому методу, программа делится на подпрограммы, каждая из которых обрабатывает свой синтаксис
Если подпрограмма не может обработать синтаксис, она передает обработку синтаксиса другой подпрограмме
И работа программы продолжается, пока не встретится конец строки 
Или ни одна из подпрограмм не сможет обработать встреченный синтаксис

В данном случае каждая подпрограмма реализована в виде функции
Одна функция отвечает за чтение математического объекта (число, функция, константа, скобка, знак числа)
Другая за сложение математических объектов, третья за умножение/деление, четвертая - возведение в степень и т д
Калькулятор получает на входе строку, проходит по ней, никак не изменяя ее, и выдает значение выражения или ошибку

Почти все функции помимо ожидаемого объекта возвращают индекс(позицию) элемента строки, на которой функция заверишла работу
Так как почти все функции так или иначе парсят строку

"""

# Часто встречающися переменные:
# Переменная eval_string - строка, содержащая выражение, которое необходимо вычислить
# Переменная index - индекс(позиция) элемента строки eval_string


# Словарь, в котором ключом является имя математической функции, а значением - объект функции
# В этом калькуляторе работа с функциями происходит путем парсинга из строки имени функции, 
# Обращения к словарю по полученному со строки имени функции
# И если запись о такой функции имеется, данная функция вызывается, когда мы берем значение словаря по ключу
# Если хотите добавить функционал - добавьте в словарь запись вида 'name_func': m.name_func
# Функция при этом должна существовать в библиотеке math
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
    # Возвращает позицию первого встреченного символа - непробела
    while index < len(eval_string) and eval_string[index] == ' ':
        index += 1
    if index > len(eval_string):
        raise ValueError("ERROR: invalid argument")
    return index


def wrapper(Func, Args):
    # Обертка, которая принимает в качестве аргумента имя функции и список, состоящий из аргументов этой функции
    # Сделано для того, чтобы калькулятор мог работать с функциями с произвольным количеством аргументов
    try:
        return Func(*Args)
    except Exception as err:
        print("ERROR: {}".format(err))


def get_arguments(eval_string, index):
    # Если в процессе парсинга сторик встречена функция, запись о которой есть в словаре,
    # И открывающая скобка, то вызывается эта функция. Она возвращает список из аргументов,
    # Перечисленных после открывающей скобки через запятую до закрывающей скобки
    # И позицию на которой функция заверишла работу
    params = []
    while index < len(eval_string) and eval_string[index] != ')':
        # В переменной tmp хранится список из полученного аргумента (1-ый элемент) 
        # И позиции, на которой был завершен парсинг (2-ой элемент)
        temp = solve_equality(eval_string, index) 
        index = temp[1] # Обновление индекса строки, на которой была завершена работа функции sum
        index = skip_space(eval_string, index)
        if index < len(eval_string) and eval_string[index] not in (',', ')'): 
        # Если не встретили конец строки, запятую или закрывающую скобку
            raise ValueError("ERROR: no zapyataya")
        elif index < len(eval_string) and eval_string[index] == ',': 
            index += 1
        params.append(temp[0]) # Добавлем полученный аргумент в список аргументов
    if index < len(eval_string) and eval_string[index] == ')':
        return params, index
    else:
        raise ValueError('ERROR: no closing bracket')


def error(args): 
    raise Exception("ERROR: invalid argument") 


def search_float(eval_string, index): 
    # Считывает со строки число и возвращает кортеж из самого числа и позиции, на которой функция завершила работу
    num = ""  # В этой строке будет храниться число, которое потом будет проеобразовано к int или float
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == '-':  
        num = '-'  
        index += 1
    index = skip_space(eval_string, index)
    while index < len(eval_string): 
        if eval_string[index].isdigit():  
            num += eval_string[index]  
            index += 1
        elif (eval_string[index].isalpha()):  # Если встретили после цифры букву, например 64a, значит что-то не так
            raise ValueError("""ERROR: РѕР±РЅР°СЂСѓР¶РµРЅ РЅРµРёР·РІРµСЃС‚РЅС‹Р№ СЃРёРјРІРѕР» {} РЅР° РїРѕР·РёС†РёРё {}""".format(
                                                                                                       eval_string[index], index))
        else:
            break 
    if (index < len(eval_string) and eval_string[index] == '.'): # Если встретили точку, значит мы встретили дробное число
        num += eval_string[index] # Добавляем точку в строку
        index += 1 
        while index < len(eval_string):
            if eval_string[index].isdigit():
                num += eval_string[index] 
                index += 1
            else:
                break
        return (float(num), index) # # Если встретили точку, значит мы встретили дробное число и вернуть мы должны вернуть дробное число
    else:
        return (int(num), index) # Если точку не встретили, значит должны вернуть целое число


def get_bracket(eval_string, index): # Считает выражение в скобках
    result, num1 = 0, 0
    index += 1
    result, index = solve_equality(eval_string, index) 
    # В скобках может быть любое выражение, а у операции сравнения самый низкий приоритет
    # Поэтому вызываем функцию, решающую неравенства либо передающую управление дальше
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == ')': # Если после подсчета математического выражения встретили скобку
        index += 1 
        return result, index
    else: # Если не встретили скобку
        raise ValueError("ERROR: РІС‹ Р·Р°Р±С‹Р»Рё РґРѕР±Р°РІРёС‚СЊ Р·Р°РєСЂС‹РІР°СЋС‰СѓСЋ СЃРєРѕР±РєСѓ РЅР° РїРѕР·РёС†РёРё {}".format(index))


def znak(eval_string, index):
    """ Обрабатывает выражения вида +-+----+-+--+---1 """
    if eval_string[index] == '+': #Если встречен знак числа плюс
        index += 1 # Смещаем позицию числа
        if index >= len(eval_string): # Если после знака числа (математического оператора) встречен конец строки
            raise ValueError("ERROR: РѕР¶РёРґР°Р»СЃСЏ РѕРїРµСЂР°РЅРґ")
        # Вызываем функцию поиска математического выражения
        # Пока встречаем знаки + и -, будет происходить вызов get_variable
        # Которая будет вызывать znak, которая будет вызывать get_variable
        # Пока get_variable не вернет число
        result, index = get_variable(eval_string, index) 
    elif eval_string[index] == '-': # Если встречен знак числа минус
        index += 1
        if index >= len(eval_string):
            raise ValueError("ERROR: РѕР¶РёРґР°Р»СЃСЏ РѕРїРµСЂР°РЅРґ")
        result, index = get_variable(eval_string, index)
        result *= -1
    return result, index
       
       
def get_variable(eval_string, index): 
    """
       Функция парсит строку и в зависимости от встреченного объекта
       Передает управление соответствующей функции
    """
    index = skip_space(eval_string, index)
    variable = "" # В этой строке будет храниться найденный математический объект
    # Если встретили число или точку (запись .1 допустима)
    if index < len(eval_string) and (eval_string[index].isdigit() or eval_string[index] == '.'): 
        variable, index = search_float(eval_string, index)
        index = skip_space(eval_string, index)
        # Если встретили не математический оператор
        if index < len(eval_string) and eval_string[index] not in (
                                           '+', '-', '*', '/', '%', '^', 
                                           '>', '<','=', ')', '!', ','
                                           ): 
            raise ValueError("ERROR: РѕР¶РёРґР°Р»СЃСЏ РѕРїРµСЂР°С‚РѕСЂ")
    # Если встречено выражение вида --+-math_object
    elif index < len(eval_string) and eval_string[index] in ('-','+'):
        variable, index = znak(eval_string, index)
    # Если встретили открывающую скобку
    elif index < len(eval_string) and eval_string[index] == '(':
        variable, index = get_bracket(eval_string, index)
    # Если встретили букву, то предполагается, что встретили функцию или константу
    elif index < len(eval_string) and eval_string[index].isalpha():  
        str = "" # Здесь будет храниться имя функции или константы
        while index < len(eval_string) and (eval_string[index].isalpha() or eval_string[index].isdigit()): 
            str += eval_string[index]
            index += 1
         # Если встретили математическую константу
         # То сразу возвращаем ее из функции как число
        if (str == 'pi'):
            variable = m.pi
        elif (str == 'e'):
            variable = m.e
        elif (str == 'tau'):
            variable = m.tau
        else: # Если встречена не константа, значит встречена функция
            if index < len(eval_string) and eval_string[index] == '(':
                index += 1
                tmp = get_arguments(eval_string, index) # В tmp лежит кортеж из списка аргументов 
                variable = wrapper(func_dictionary.get(str.lower(), error), tmp[0])
                index = tmp[1]
                if index < len(eval_string) and eval_string[index] == ')':
                    index += 1
                    index = skip_space(eval_string, index)
            # Если не константа и при этом нет открывающей скобки (то есть это не функция)
            # Бросаем исключение
            else:  
                raise ValueError("ERROR: Invalid argument (index {})".format(index))
    # Это условие написано специально для функции get_arguments
    # Она вызывает get_variable, которая находит математическое выражение
    # Считает его, найдет запятую и возвращает результат 
    elif index < len(eval_string) and eval_string[index] == ',':
        return variable, index
    else:
        raise ValueError("ERROR: РѕР±РЅР°СЂСѓР¶РµРЅ РЅРµРёР·РІРµСЃС‚РЅС‹Р№ СЃРёРјРІРѕР» РЅР° РїРѕР·РёС†РёРё {}".format(index))
    return (variable, index)


def get_degree(eval_string, index):
    """
        Производит возведение в степень с помощью рекурсии
        
        Пока встречается ^, происходит рекурсивный вызов этой же функции
        Затем, когда в последнем рекурсивном вызове не найдется ^
        Функция вернет последнее число и в предпоследнем вызове в переменной
        result будет записано предпоследнее число, а в num1 - последнее
   """
    result, num1, index = 0, 0, skip_space(eval_string, index)
    result, index = get_variable(eval_string, index) # Передача управления "вверх"
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == '^':
        index += 1
        num1, index = get_degree(eval_string, index) # Тот самый рекурсивный вызов
        if (result == 0 and num1 == 0): # Нельзя возводить 0 в степень 0
            raise ValueError("ERROR: РІРѕР·РІРµРґРµРЅРёРµ 0 РІ СЃС‚РµРїРµРЅСЊ 0 (РїРѕР·РёС†РёСЏ {})".format(index))
        result **= num1
        index = skip_space(eval_string, index)
    return result, index


def multiply(eval_string, index):
    mult, num1, index = 1, 0, skip_space(eval_string, index)
    mult, index = get_degree(eval_string, index) # Передача управления "вверх"
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
    num1, index = sum(eval_string, index) # Передача управления "вверх"
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] not in (">", "=", "<", "!", ")", ","):
        raise ValueError("ERROR: РѕР±РЅР°СЂСѓР¶РµРЅ РЅРµРёР·РІРµСЃС‚РЅС‹Р№ СЃРёРјРІРѕР» {} РЅР° РїРѕР·РёС†РёРё {}".format(
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
    """
        С вызова этой функции все начинается
        С return этой функции все заканчивается
    """
    index = skip_space(eval_string, index)
    if index >= len(eval_string):
        raise ValueError("ERROR: РІС‹ РЅРёС‡РµРіРѕ РЅРµ РІРІРµР»Рё")
    result, index = solve_equality(eval_string, index) # Передача управления "вверх"
    return result