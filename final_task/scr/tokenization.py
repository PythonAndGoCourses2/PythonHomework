from . import settings as st


def delete_whitespaces(expression):
    clean_expression = ""
    for token in expression:
        if token != st.whitespace:
            clean_expression += token
    return clean_expression


def tokenize(expression):
    expression = delete_whitespaces(expression)
    lexeme = ''
    tokenized_expression = []
    data_category = ''
    for token in expression:
        if lexeme:
            if token in data_category:
                lexeme += token
            else:
                tokenized_expression.append(lexeme)
                lexeme = token
                data_category = ''
                for data in st.data_set:
                    if token in data:
                        data_category = data
                        break
        else:
            data_category = ''
            for data in st.data_set:
                if token in data:
                    data_category = data
                    break
            lexeme += token
    tokenized_expression.append(lexeme)
    return tokenized_expression
