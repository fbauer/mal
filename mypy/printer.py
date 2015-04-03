from syntax import ATOM_TO_STRING_CONVERTERS

def pr_str(a_form):
    if type(a_form) == list:
        return pr_list(a_form)
    elif type(a_form) == dict:
        return pr_dict(a_form)
    elif type(a_form) == tuple:
        return pr_vec(a_form)
    else:
        return ATOM_TO_STRING_CONVERTERS[type(a_form)](a_form)

def pr_list(a_list):
    return "(%s)" % " ".join(pr_str(a) for a in a_list)

def pr_dict(a_dict):
    return "{%s}" % " ".join("%s %s" % (pr_str(k), pr_str(v))
                             for (k, v) in a_dict.items())
def pr_vec(a_vec):
    return "[%s]" % " ".join(pr_str(a) for a in a_vec)
