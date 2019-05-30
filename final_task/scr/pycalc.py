from tokenization import tokenize
from reverse_polish_notation import convert_to_RPN
from evaluate import calculate
from command_line_parser import create_parser
from expression_backend_script import define_funcs_in_expression


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
