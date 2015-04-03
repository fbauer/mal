"""Implementation of the mal lisp reader

Uses some undocumented re features:

  - scanner method of regular expression objects
  - lastgroup attribute of match object

They are described in the following effbot article:

http://effbot.org/zone/xml-scanner.htm
"""
import re
from syntax import TOKEN_RE, STRING_TO_ATOM_CONVERTERS

def read_str(input_string):
    reader = tokenizer(input_string)
    tok = next(reader)
    return read_form(tok, reader)

def tokenizer(input_string):
    scanner = TOKEN_RE.scanner(input_string)
    while 1:
        m = scanner.match()
        if m is None:
            break
        if m.lastgroup not in ("t_whitespace", "t_comment"):
            yield m

def read_form(tok, tokens):

    if tok.group(0) == "(":
        return read_list(tokens)
    elif tok.group(0) == "{":
        return read_hashmap(tokens)
    elif tok.group(0) == "[":
        return read_vector(tokens)
    # reader macros
    elif tok.lastgroup in ("t_quote", "t_splice_unquote", "t_unquote",
                           "t_quasiquote", "t_deref"):
        return reader_macro(tok, tokens)
    else:
        return read_atom(tok)

def read_list(tokens):
    a_list = []
    for tok in tokens:
        if tok.group(0) == ")":
            break
        else:
            a_list.append(read_form(tok, tokens))
    return a_list

def read_hashmap(tokens):
    a_dict = {}
    for tok in tokens:
        if tok.group(0) == "}":
            break
        else:
            a_dict[read_form(tok, tokens)] = read_form(next(tokens), tokens)
    return a_dict

def read_vector(tokens):
    a_list = []
    for tok in tokens:
        if tok.group(0) == "]":
            break
        else:
            a_list.append(read_form(tok, tokens))
    return tuple(a_list)

def read_atom(the_token):
    convert = STRING_TO_ATOM_CONVERTERS[the_token.lastgroup]
    return convert(the_token.group(0))

def reader_macro(the_token, tokens):
    convert = STRING_TO_ATOM_CONVERTERS[the_token.lastgroup]
    return [convert(the_token.group(0)),
            read_form(next(tokens), tokens)]
