def insert(d, s, val, err_on_present = False):
    splt_s = s.split('.', 1)
    topkey = splt_s[0]
    rest = splt_s[1] if len(splt_s) == 2 else None

    if rest:
        if not d.get(topkey, None):
            d[topkey] = {}
        insert(d[topkey], rest, val, err_on_present)
    else:
        # TODO: Check for duplicates
        d[topkey] = val

def get(d, s):
    # Empty path is root of dict
    if len(s) == 0:
        return d

    splt_s = s.split('.', 1)
    topkey = splt_s[0]
    rest = splt_s[1] if len(splt_s) == 2 else None

    if rest == None:
        return d.get(topkey, None)
    elif not d.get(topkey, None):
        return None
    else:
        return get(d[topkey], rest)

def pop(d, k):
    splt_k = k.split('.', 1)
    topkey = splt_k[0]
    rest = splt_k[1] if len(splt_k) == 2 else None

    if rest:
        if not d.get(topkey, None):
            return None
        pop(d[topkey], rest)
    else:
        # TODO: Check for duplicates
        return d.pop(topkey)
