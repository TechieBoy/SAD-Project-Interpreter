import sys
from parser import *
from lexer import *

# Print lexer and parser output.
debugmode = True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please enter filename.',file=sys.stderr)
        sys.exit(1)
    filename = sys.argv[1]
    
    text = open(filename).read()

    tokens = lex(text)
    if debugmode == True:
        print('=============================================================== Output from lexer ===============================================================\n')
        for token in tokens:
            print (token)

    parse_result = parse(tokens)
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        sys.exit(1)
    if debugmode == True:
        print('\n=============================================================== Output from parser ===============================================================\n')
        print (parse_result.value)

    ast = parse_result.value
    env = {}
    if debugmode == True:
        print('\n=============================================================== Program Output ===================================================================\n')
    ast.eval(env)

    if debugmode == True:
        print('\n=============================================================== Final variable values ============================================================\n')
        for name in env:
            print(name, ": ", env[name])