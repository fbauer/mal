"""Implementation of the mal syntax table
"""
import re

def constant(the_constant):
    def _constant(a_string):
        return the_constant
    return _constant

def identity(x):
    return x

def to_bool(s):
    return {'true': True, 'false': False}[s]

def from_bool(a):
    return {True: 'true', False: 'false'}[a]

SYNTAX_TABLE = (
    ("t_whitespace", r"[\s,]+", "ignore", None, str),
    ("t_comment", r";.*", "ignore", None, str),
    ("t_nil", r"nil", constant(None), constant("nil"), type(None)),
    ("t_bool", r"true|false", to_bool, from_bool, type(True)),
    ("t_integer", r"[0-9]+", int, str, type(1)),
    ("t_splice_unquote", r"""~@""", constant("splice-unquote"), str, str), 
    ("t_delim", r"[\[\]{}()'`~^@]", identity, identity, str),
    ("t_string", r'''"(?:\\.|[^\\"])*"''', identity, identity, str),
    ("t_symbol", r"""[^\s\[\]{}('"`,;)]*""", identity, identity, str),
)

TOKEN_RE = re.compile("|".join(r"(?P<%s>%s)" % t[0:2] for t in SYNTAX_TABLE), re.VERBOSE)

STRING_TO_ATOM_CONVERTERS = dict((t[0], t[2]) for t in SYNTAX_TABLE)
ATOM_TO_STRING_CONVERTERS = dict((t[4], t[3]) for t in SYNTAX_TABLE)
