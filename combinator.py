# Every Parser will return either Result or None.
class Result:
    def __init__(self,value,idx):
        self.value = value
        self.idx = idx
    
    def __repr__(self):
        return 'Result(%s, %d)' % (self.value, self.idx)

# Base Parser class.
class Parser:
    def __call__(self,tokens,idx):
        return None
    
    def __add__(self,other):
        return Concat(self,other)

    def __mul__(self,other):
        return Exp(self,other)
    
    def __or__(self,other):
        return Alternate(self,other)

    def __xor__(self,function):
        return Process(self,function)

# Only Process Tags.
class Tag(Parser):
    def __init__(self,tag):
        self.tag = tag

    def __call__(self,tokens,idx):
        if idx < len(tokens) and tokens[idx][1] is self.tag:
            return Result(tokens[idx][0], idx + 1)
        else:
            return None

# Process Reserved tokens.
class Reserved(Parser):
    def __init__(self,value,tag):
        self.value = value
        self.tag = tag

    def __call__(self,tokens,idx):
        if idx < len(tokens) and tokens[idx][0] == self.value and tokens[idx][1] is self.tag:
            return Result(tokens[idx][0], idx + 1)
        else:
            return None

# Left parser concatenated with right parser. If either is unsuccessful, None is returned.
class Concat(Parser):
    def __init__(self, leftParser,rightParser):
        self.leftParser = leftParser
        self.rightParser = rightParser
    
    def __call__(self,tokens,idx):
        left_ans = self.leftParser(tokens,idx)
        if left_ans:
            right_ans = self.rightParser(tokens,left_ans.idx)
            if right_ans:
                ans = (left_ans.value,right_ans.value)
                return Result(ans,right_ans.idx)
        return None

# Left is returned first. If unsuccessful, right is returned.
class Alternate(Parser):
    def __init__(self, leftParser, rightParser):
        self.leftParser = leftParser
        self.rightParser = rightParser

    def __call__(self, tokens, idx):
        left_ans = self.leftParser(tokens, idx)
        if left_ans:
            return left_ans
        else:
            right_ans = self.rightParser(tokens, idx)
            return right_ans

# Optinal text. (Else) No tokens are consumed.
class Opt(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, idx):
        result = self.parser(tokens, idx)
        if result:
            return result
        else:
            return Result(None, idx)



# Parser is passed to function and function's return value is returned.
class Process(Parser):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, idx):
        result = self.parser(tokens, idx)
        if result:
            result.value = self.function(result.value)
            return result

# Takes a 0-argument function which returns a parser.
# Will not call the function to get the parser until it's applied
class Lazy(Parser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens, idx):
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens, idx)

# Takes a single input parser, applies it, and returns its result normally.
# Will fail if its input parser did not consume all of the remaining tokens.
class Phrase(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, idx):
        result = self.parser(tokens, idx)
        if result and result.idx == len(tokens):
            return result
        else:
            return None

# Match an expression which consists of a list of elements separated by seperator.
class Exp(Parser):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens, idx):
        result = self.parser(tokens, idx)

        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(result.value, right)
        next_parser = self.separator + self.parser ^ process_next
        next_result = result
        while next_result:
            next_result = next_parser(tokens, result.idx)
            if next_result:
                result = next_result
        return result
