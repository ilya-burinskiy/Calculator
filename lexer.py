from terminal import Terminal

class Lexer:

    def __init__(self):
        self._i = 0
        self._n = 0
        self._expr = None
        self._prev_terminal = None

    def set_expr(self, expr):
        self._expr = expr
        self._n = len(expr)

    def is_unary_minus(self) -> bool:
        op = {"ADD", "SUB", "MUL", "DIV", "NEG"}
        if (self._expr[self._i] == '-' and self._prev_terminal in op or 
                                     self._prev_terminal == "LBRACE" or
                                     self._prev_terminal == "FUNC" or
                                     self._prev_terminal is None):
            return True
            
    def check_uminus_syntax(self):
        try:
            is_space = self._expr[self._i + 1] == ' '
        except IndexError:
            raise SyntaxError("Unary minus without operand")
        else: 
            if is_space: 
                raise SyntaxError("Space between unary minus and operand")

    def read_number(self):
        number = ""
        is_float = False
                
        number += self._expr[self._i]
        self._i += 1
        while self._i < self._n:
            if self._expr[self._i].isdigit() or \
                    self._expr[self._i] == '.':
                if self._expr[self._i] == '.': is_float = True
                number += self._expr[self._i]
                self._i += 1
            else: break
        return number, is_float

    def read_function(self):
        functions = {"sin", "cos", "tan", "abs", "ln", "sqrt"}
        func = ""
        
        func += self._expr[self._i]
        self._i += 1
        while self._i < self._n:
            if self._expr[self._i].isalpha():
                func += self._expr[self._i]
                self._i += 1
            else: break
        
        if func in functions:
            return func
        else:
            raise SyntaxError("Unknown function")

    def get_terminal(self):
        create_terminal = lambda: Terminal.from_char(self._expr[self._i])
        is_operator = (lambda: self._expr[self._i] == '+' or 
                               self._expr[self._i] == '-' or
                               self._expr[self._i] == '*' or
                               self._expr[self._i] == '/')
        is_brace = lambda: (self._expr[self._i] == '(' or 
                            self._expr[self._i] == ')')
        while self._i < self._n:

            if self._expr[self._i].isspace():
                self._i += 1
                continue

            elif self._expr[self._i].isdigit():
                number, is_float = self.read_number()
                number = float(number) if is_float else int(number)
                number = Terminal("NUM", number)
                self._prev_terminal = number
                return number

            elif self._expr[self._i].isalpha():
                func = self.read_function()
                func = Terminal("FUNC", func)
                self._prev_terminal = func
                return func

            elif is_operator():
                if self.is_unary_minus():
                    try:
                        self.check_uminus_syntax()
                    except SyntaxError:
                        raise
                    else:
                        neg = Terminal("NEG")
                        self._prev_terminal = neg
                        self._i += 1
                        return neg
                else:
                    op = create_terminal()
                    self._prev_terminal = op
                    self._i += 1
                    return op
            
            elif is_brace():
                brace = create_terminal()
                self._prev_terminal = brace
                self._i += 1
                return brace
            else:
                raise SyntaxError("Unknown symbol")

    def reset(self):
        self._i = 0
        self._n = 0
        self._expr = None
        self._prev_terminal = None