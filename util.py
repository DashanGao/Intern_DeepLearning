
def num_extractor(lines, pattern, recall=[-1]):
    """
    :param lines: a string
    :param pattern: pattern to match, put {num} at number you want to extract
                    multi {num} is supported, but not *, / or other special chars
    :param recall: a list marks return index
    :return: a list of extracted number
    """
    import re
    import numpy as np
    identify = "{num}"

    inter = []
    last = 0
    while True:
        identify_idx = pattern.find(identify, last)
        if identify_idx == -1:
            break
        inter.append(pattern[last:identify_idx])
        last = identify_idx + len(identify)
    inter.append(pattern[last:])
    inter = [x for x in inter if x != '']
    pattern = pattern.replace(identify, r"\d+\.?\d*")

    ret = []
    for idx, i in enumerate(re.finditer(pattern, lines)):
        result_str = i.group()
        for inter_str in inter:
            result_str = result_str.replace(inter_str, "___")
        k = result_str.split("___")
        k = [x for x in k if x != '']

        ret.append(k)
    if recall[0] != -1:
        for idx, item in enumerate(ret):
            ret[idx] = [y for i, y in enumerate(item) if i in recall]
    return np.array(ret, dtype=np.float32)


def parse_json(string, path):
    """
    :param string: string to parse
    :param path: dict path a/b/c
    :return: a list or item
    """
    import json
    step = path.split("/")
    if isinstance(string, str):
        ret = json.loads(string)
        for i in step:
            ret = ret[i]
        return ret
    elif isinstance(string, list):
        
        jlist = [json.loads(x) for x in string] 
        ret = []
        for i in jlist:
            for j in step:
                i = i[j]
            ret.append(i)
        return ret
    else:
        raise TypeError("strin type should be either json list or json string")

def parse_str(string, pattern=" ", type="list", match_num=100000, key_idx=0):
    """
    :param string: string to parse
    :param pattern: split pattern
    :param type: return a list or a dictiong
    :param match_num: split times
    :param key_idx: which idx is key value when type=="dict"
    :return: a list or dict
    """
    if type != "list" and type != "dict":
        raise TypeError("type should be either \"list\" or \"dict\" but " + str(type))
    if string is None:
        raise ValueError("string is none")
    line = string[0].strip().split(pattern)
    if len(line) == 1:
        raise ValueError("Pattern can't match")
    if key_idx >= len(line):
        raise ValueError("key_idx < len(line), " + str(key_idx) + " vs " + str(len(line)))
    if type == "list":
        res = [l.strip().split(pattern, match_num) for l in string]
    elif type == "dict":
        res = {}
        for l in string:
            line = l.strip().split(pattern, match_num)
            key = line.pop(key_idx)
            res[key] = []
            if len(line) != 1:
                res[key] = line
            else:
                res[key] = line[0]
    return res


