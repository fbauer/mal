#!python3
try:
    import readline
except ImportError:
    print("no readline")
    pass

def READ(*args):
    return args[0]

def EVAL(*args):
    return args[0]

def PRINT(*args):
    return args[0]

def rep(*args):
    return PRINT(EVAL(READ(*args)))


def mainloop():
    while(1):
        try:
            line = input("mal-user> ")
            if line in ("",):
                continue
            print(rep(line))
        # exit on Ctrl-D
        except EOFError:
            return
        
if __name__ == "__main__":
    mainloop()
