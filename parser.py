from lexer import *
from combinator import *
from tek_ast import *
from functools import *

# Identifiers
tid = Tag(ID)

# String literals
tstr = Tag(STRING)

# Integers
num = Tag(INT) ^ (lambda i: int(i))

# ================================ Main parser ===============================================
def parse(tokens):
    ast = parser()(tokens, 0)
    return ast

def parser():
    return Phrase(stmt_list())

# =============================== Precedence levels ===========================================

aexp_precedence_levels = [
    ['*', '/', '%'],
    ['+', '-'],
]

bexp_precedence_levels = [
    [andoperator],
    [oroperator],
]

# Combinator for binary operator expressions (aexp and bexp)
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser

# ============================== Helper functions ============================================

# Any keyword which has RESERVED tag.
def keyword(kw):
    return Reserved(kw,RES)

# Tries to match any operator in given ops list.
def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

# ===================================== Expressions ==========================================

# ------------------------------------- String Expressions ----------------------------------
def strexp():
    return tstr ^ (lambda s: Strexp(s))

# ------------------------------------- Arithmetic Expressions ------------------------------
 
# Process intexp first, otherwise variable.
def aexp_value():
    return (num ^ (lambda i: IntAexp(i))) | (tid  ^ (lambda v: VarAexp(v)))

# Remove all parenthesis.
def process_group(parsed):
    ((_, p), _) = parsed
    return p

# Combine group together.
def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group

# A term is a value or a group (Doesn't know about precedence yet!)
def aexp_term():
    return aexp_value() | aexp_group()

# Processes binary operators.
def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)

# Final arithmetic expression taking into account precedence.
def aexp():
    return precedence(aexp_term(), aexp_precedence_levels, process_binop)

# ----------------------------- Boolean expressions -------------------------------------

# Convert parsed data to relational operator parser.
def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)

# Realtional operators for boolean expressions.
def bexp_relop():
    relops = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop

# Boolean not is special as it has no left operand.
def bexp_not():
    return keyword(notoperator) + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))

# Processes a bracketed group.
def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group

# A term is a group, not expression or expression with relational operator.
def bexp_term():
    return bexp_not() | bexp_relop() | bexp_group()

# Convert Relational operator into concrete value.
def process_logic(op):
    if op == andoperator:
        return lambda l, r: AndBexp(l, r)
    elif op == oroperator:
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)

# Final boolean expression taking into account precedence.
def bexp():
    return precedence(bexp_term(), bexp_precedence_levels, process_logic)

# ======================================= Statements ===========================================

# Assign values to variables.
def assign_stmt(): 
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return tid + keyword(assignment) + (aexp() | strexp()) ^ process

# If statement (with optional else)
def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)
    return keyword(ifstmt) + bexp() + keyword(thenstmt) + Lazy(stmt_list) + Opt(keyword(elsestmt) + Lazy(stmt_list)) + keyword(endstmt) ^ process

# While statement.
def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword(whilestmt) + bexp() + keyword(dostmt) + Lazy(stmt_list) + keyword(endstmt) ^ process

# Print statement.
def print_stmt():
    def process(parsed):
        (_,s) = parsed
        return PrintStatement(s)
    return keyword(printstmt) + (aexp() | strexp()) ^ process

# A generic statement.
def stmt():
    return assign_stmt() | if_stmt() | while_stmt() | print_stmt()

# List of all statements (seperated by seperator keyword)
def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)
