from syntax import ATOM_TO_STRING_CONVERTERS

def pr_str(a_form):
    if type(a_form) == list:
        return pr_list(a_form)
    else:
        return ATOM_TO_STRING_CONVERTERS[type(a_form)](a_form)

def pr_list(a_list):
    return "(%s)" % " ".join(pr_str(a) for a in a_list)
