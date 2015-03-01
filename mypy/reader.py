"""Implementation of the mal lisp reader

Uses some undocumented re features:

  - scanner method of regular expression objects
  - lastgroup attribute of match object

They are described in the following effbot article:

http://effbot.org/zone/xml-scanner.htm
"""
import re
from syntax import TOKEN_RE, STRING_TO_ATOM_CONVERTERS

class Reader():
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.lookahead = None

    def next(self):
        if self.lookahead is not None:
            token = self.lookahead
            self.lookahead = None
            return token
        return next(self.tokens)

    def peek(self):
        if self.lookahead is not None:
            token = self.lookahead
            self.lookahead = None
            return token
        else:
            self.lookahead = next(self.tokens)
            return self.lookahead

def read_str(input_string):
    reader = Reader(tokenizer(input_string))
    return read_form(reader)

def tokenizer(input_string):
    scanner = TOKEN_RE.scanner(input_string)
    while 1:
        m = scanner.match()
        if m is None:
            break
        if m.lastgroup not in ("t_whitespace", "t_comment"):
            yield m

def read_form(a_reader):
    tok = a_reader.peek()
    if tok.group(0) == "(":
        return read_list(a_reader)
    else:
        return read_atom(a_reader)

def read_list(a_reader):
    a_list = []
    while a_reader.peek().group(0) != ")":
        a_list.append(read_form(a_reader))
    return a_list

def read_atom(a_reader):
    the_token = a_reader.next()
    convert = STRING_TO_ATOM_CONVERTERS[the_token.lastgroup]
    return convert(the_token.group(0))
