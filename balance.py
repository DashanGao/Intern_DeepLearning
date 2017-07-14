"""
def input_balance(dic, key_idx, iter):
    parse_dict = {} if isinstance(dic, dict) is False else dic
    if not parse_dict:
        for i in dic:
            key = i.pop(key_idx)
            parse_dict[key] = []
            if len(i) != 1:
                parse_dict[key] = i
            else:
                parse_dict[key] = i[0]
    for i in range(iter):
        for key, value in parse_dict.items():
"""