

def tokenize(p , sentence : str) -> dict:
    return p(sentence)


def read_token(token: dict) -> list:
    """
    'extended' : return list of tokens
    'normal' : returns list of itself
    :param token:
    :return: list:
    """

    if 'expanded' in token.keys():
        result: list = []
        template = {k: v for k, v in token.items() if k != "expanded"}
        for tkn in token['expanded']:
            tkn_: dict = tkn.copy
            tkn_.update(template)
            result.append(tkn_)
    else:
        return [token]


def flatten_tokens(tokens : list) -> list:
    return sum([read_token(tkn) for tkn in tokens ],[])


def find_token(tokens : list, id : int) -> dict:
    for token in tokens:
        if token["id"] == id:
            return token


def give_chidren(tokens, parent_id):
    is_child = lambda tkn: tkn['head'] == parent_id
    return [token for token in tokens if is_child(token)]


def select_text(text: str, beg: int,end: int)-> str:
    return text[beg:end]



