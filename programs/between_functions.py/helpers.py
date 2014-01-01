def between(a, l, h):
    result = []
    for a_i in a:
        if (l < a_i) and (a_i < h):
            result.append(a_i)
    return result

def common(a, b):
    result = []
    for a_i in a:
        if a_i in b:
            result.append(a_i)
    return result
