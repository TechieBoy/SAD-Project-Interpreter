import sys
import re

# TAGS
RES = 'RESERVED'
INT = 'INT'
ID  = 'ID'
STRING = 'STRING'

# keywords
assignment = '<-'
ifstmt = 'agar'
thenstmt = 'toh'
elsestmt = 'nahi-toh'
endstmt = 'khatam'
whilestmt = 'jab-tak'
dostmt = 'tab-tak'
printstmt = 'bolo'
andoperator = 'aur'
oroperator = 'ya'
notoperator = 'not'

# Syntax matchers
token_expressions = [
    (r'[ \n\t]+',        None),   # Whitespace
    (r'@[^\n]*',         None),   # Comments
    (r'<-',              RES),    # Assignment
    (r'\(',              RES),    # Open parenthesis
    (r'\)',              RES),    # Close parenthesis
    (r';',               RES),    # Compound statement seperator
    (r'\+',              RES),    # Additon operator
    (r'\-',              RES),    # Subtraction operator
    (r'\*',              RES),    # Multiplication operator
    (r'/',               RES),    # Division operator
    (r'%',               RES),    # Modulo operator
    (r'<=',              RES),    # Less than equals
    (r'<',               RES),    # Less than
    (r'>=',              RES),    # Greater than equals
    (r'>',               RES),    # Greater than 
    (r'=',               RES),    # Equals
    (r'!=',              RES),    # Not equals
    (r'aur',             RES),    # Boolean and
    (r'ya',              RES),    # Boolean or
    (r'not',             RES),    # Boolean not
    (r'bolo',            RES),    # Print
    (r'agar',            RES),    # if
    (r'toh',             RES),    # then
    (r'nahi\-toh',       RES),    # else
    (r'jab\-tak',        RES),    # while
    (r'tab\-tak',        RES),    # do
    (r'khatam',          RES),    # end block
    (r'\".*\"',          STRING), # String
    (r'[0-9]+',          INT),    # Integer
    (r'[A-za-z]\w*',     ID)      # Identifier
]

# Lexer
def lex(chars):
    i = 0
    tokens = []
    while i < len(chars):
        match = None
        for t in token_expressions:
            pattern,tag = t
            reg = re.compile(pattern)
            match = reg.match(chars,i)
            if match:
                ans = match.group(0)
                if tag:
                    token = (ans,tag)
                    tokens.append(token)
                break
        if not match:
            print("Illegal character: ", chars[i],file=sys.stderr)
            sys.exit(1)
        else:
            i = match.end(0)
    return tokens
