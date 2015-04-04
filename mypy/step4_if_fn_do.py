#!python3
import reader
import printer
import operator
from functools import partial, reduce
import env
import syntax

repl_env = [{}]

for symbol, function in {'+': partial(reduce, operator.add),
                         '-': partial(reduce, operator.sub),
                         '*': partial(reduce, operator.mul),
                         '/': partial(reduce, operator.floordiv),}.items():
    env.set(repl_env, symbol, function)

try:
    import readline
except ImportError:
    print("no readline support")
    pass

def READ(*args):
    return reader.read_str(args[0])

def EVAL(ast, environment):
    if ast and type(ast) == list:
        if ast[0] == "let*":
            newenv = [{}] + repl_env
            let_bindings = ast[1]
            for sym, val in zip(let_bindings[0::2],
                                let_bindings[1::2]):
                env.set(newenv, sym, EVAL(val, newenv))
            return EVAL(ast[2], newenv)
        elif ast[0] == "def!":
            symbol = ast[1]
            value = EVAL(ast[2], environment)
            env.set(environment, symbol, value)
            return env.get(environment, symbol)
        else:
            fn = env.get(environment, ast[0])
            args = [EVAL(arg, environment) for arg in ast[1:]]
            return fn(args)
    elif ast and type(ast) == dict:
        return dict((EVAL(k, environment),
                     EVAL(v, environment)) for (k, v) in ast.items())
    elif ast and type(ast) == tuple:
        return tuple(EVAL(i, environment) for i in ast)
    elif ast and type(ast) == syntax.symbol:
        return env.get(environment, ast)
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
