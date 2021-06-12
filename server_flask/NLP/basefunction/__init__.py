def json2list(json_file):
    _list = list()
    for line in json_file:
        _list.append(line['text'])

    return _list


def list2json(idxs, json_file):
    result = list()
    for idx in idxs:
        result.append(json_file[idx])

    return result


def ctrl_f(keyword, json_file):
    result = list()
    for line in json_file:
        if keyword in line['text']:
            result.append(line)

    return result
