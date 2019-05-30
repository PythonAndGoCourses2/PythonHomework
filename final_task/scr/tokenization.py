from . import settings as st


def tokenize(expression):
    # expression = delete_whitespaces(expression)
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
    tokenized_expression = delete_whitespace(tokenized_expression)
    return tokenized_expression


def delete_whitespace(tokenized_expression):
    clean_tokenized_expression = []
    for token in tokenized_expression:
        if token != ' ':
            clean_tokenized_expression.append(token)
    return clean_tokenized_expression
