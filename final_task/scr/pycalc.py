from PythonHomework.final_task.scr import tokenize
from PythonHomework.final_task.scr import convert_to_RPN
from PythonHomework.final_task.scr import calculate
from PythonHomework.final_task.scr import create_parser
from PythonHomework.final_task.scr import define_funcs_in_expression


def main():
    try:
        expression = create_parser()
        if expression:
            tokenized_expression = tokenize(expression)
            prepared_tokenizer_exp = define_funcs_in_expression(tokenized_expression)
            converted_expression = convert_to_RPN(prepared_tokenizer_exp)
            print(calculate(converted_expression))
        else:
            raise Exception('EXPRESSION is empty')
    except Exception as error:
        print("ERROR: " + str(error))


if __name__ == '__main__':
    main()
