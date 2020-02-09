from parser import Parser
import math

class Calculator:

    def __init__(self):
        self._parser = Parser() 

    def _calculate(self, expr):
        prefix_expr = self._parser.parse(expr)
        binary_ops = {"ADD": lambda a, b: a + b,
                      "SUB": lambda a, b: a - b,
                      "MUL": lambda a, b: a * b,
                      "DIV": lambda a, b: a / b}

        functions = {"sin": lambda a: math.sin(a),
                     "cos": lambda a: math.cos(a),
                     "tan": lambda a: math.tan(a),
                     "abs": lambda a: abs(a),
                     "ln": lambda a: math.log(a, math.e),
                     "sqrt": lambda a: math.sqrt(a)}

        unary_ops = {"NEG": lambda a: -a}
        stack = []
        for term in prefix_expr:
            if term == "NUM":
                stack.append(term.attr)
            elif term in binary_ops:
                r = stack.pop()
                l = stack.pop()
                res = binary_ops[term](l, r)
                stack.append(res)
            elif term.attr in functions:
                operand = stack.pop()
                res = functions[term.attr](operand)
                stack.append(res)
            else:
                operand = stack.pop()
                res = unary_ops[term](operand)
                stack.append(res)
        return stack.pop()

    def calculate(self, expr):
        try:
            res = self._calculate(expr)
        except SyntaxError:
            raise
        except ZeroDivisionError:
            raise
        else:
            return res

    def reset(self):
        self._parser.reset()
