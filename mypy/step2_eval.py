#!python3
import reader
import printer
import operator
from functools import partial, reduce


repl_env = {'+': partial(reduce, operator.add),
            '-': partial(reduce, operator.sub),
            '*': partial(reduce, operator.mul),
            '/': partial(reduce, operator.floordiv),}
try:
    import readline
except ImportError:
    print("no readline support")
    pass

def READ(*args):
    return reader.read_str(args[0])

def EVAL(ast, env):
    if ast and type(ast) == list:
        fn = repl_env[ast[0]]
        args = [EVAL(arg, env) for arg in ast[1:]]
        return fn(args)
    elif ast and type(ast) == dict:
        for k, v in ast.items():
            ast[k] = EVAL(v, env)
    elif ast and type(ast) == tuple:
        return tuple(EVAL(i, env) for i in ast)
    else:
        return ast

def PRINT(*args):
    return printer.pr_str(args[0])

def rep(*args):
    return PRINT(EVAL(READ(*args), repl_env))


def mainloop():
    while(1):
        try:
            line = input("mal-user> ")
            if line in ("",):
                continue
            try:
                print(rep(line))
            except Exception as e:
                print(e)
        # exit on Ctrl-D
        except EOFError:
            return
        
if __name__ == "__main__":
    mainloop()
