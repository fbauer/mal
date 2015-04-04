

def set(env, symbol, value):
    env[0][symbol] = value

def find(env, symbol):
    for environ in env:
        if symbol in environ:
            return environ

def get(env, symbol):
    environ = find(env, symbol)
    if environ:
        return environ[symbol]
    else:
        raise KeyError("%s is undefined" % symbol)
