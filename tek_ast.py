class Equality:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)
#============================== String Expressions ===============================#

class Strexp(Equality):
    def __init__(self,s):
        self.s = s
    
    def __repr__(self):
        return 'Strexp(%s)' %(self.s)
    
    def eval(self,env):
        return self.s[1:-1]

#============================== Arithmetic Expressions ===============================#
class Aexp(Equality):
    pass

# Integer Arithmetic Expression.
class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i

    def eval(self, env):
        return self.i

# Variable Arithmetic Expression.
class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VarAexp(%s)' % self.name

    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            return 0

# Arithmetic Expression with binary operator in between.
class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.op, self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        elif self.op == '%':
            value = left_value % right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return int(value)

#============================== Boolean Expressions ===============================#
class Bexp(Equality):
    pass

# Relational operator in boolean expression.
class RelopBexp(Bexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'RelopBexp(%s, %s, %s)' % (self.op, self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '=':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value

# And expression.
class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'AndBexp(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value and right_value

# Or expression.
class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'OrBexp(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value or right_value

# Not expression.
class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return '\nNotBexp(%s)' % self.exp

    def eval(self, env):
        value = self.exp.eval(env)
        return not value

#============================== Statements ===============================#
class Statement(Equality):
    pass

# Assign values to identifiers.
class AssignStatement(Statement):
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp

    def __repr__(self):
        return '\nAssignStatement(%s, %s)' % (self.name, self.exp)

    def eval(self, env):
        value = self.exp.eval(env)
        env[self.name] = value

# Multiple statements followed by semicolon.
class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return '%s, %s' %(self.first, self.second) # '\nCompoundStatement(%s, %s)' % (self.first, self.second)

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)

# If condition.
class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def __repr__(self):
        return '\nIfStatement(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        if condition_value:
            self.true_stmt.eval(env)
        else:
            if self.false_stmt:
                self.false_stmt.eval(env)

# While loop
class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return '\nWhileStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        while condition_value:
            self.body.eval(env)
            condition_value = self.condition.eval(env)

# Print value.
class PrintStatement(Statement):
    def __init__(self,ans):
        self.ans = ans
    
    def __repr__(self):
        return '\nPrintStatement(%s)' % (self.ans)
    
    def eval(self,env):
        ans = self.ans.eval(env)
        print(ans)
