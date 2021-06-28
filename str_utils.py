def dict2params(dicts: dict) -> str:
    result: str = ''
    for key in dicts:
        if isinstance(dicts[key], str):
            result += key + '=\'' + dicts[key] + '\','
        elif isinstance(dicts[key], int) or isinstance(dicts[key], float):
            result += key + '=' + dicts[key] + ','
        else:
            result += ''
    return result[0: len(result) - 1]
