def print_pretty(print_string: str):
    import pprint
    print_pretty = pprint.PrettyPrinter()
    print_pretty.pprint(print_string)

def print_magenta(print_string: str):
    print('\033[35m' + print_string + '\033[39m')

def print_green(print_string: str):
    print('\033[32m' + print_string + '\033[39m')

def print_yellow(print_string: str):
    print('\033[33m' + print_string + '\033[39m')

def print_red(print_string: str):
    print('\033[31m' + print_string + '\033[39m')