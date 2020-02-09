from terminal import Terminal
from lexer import Lexer
from copy import copy

class Parser:

    def __init__(self):
        self._lex = Lexer()
        self._curr_terminal = None
        self._prefix = []

    # add/sub operations
    def _parse_prior4(self):
        self._parse_prior3()
        while True:
            if (self._curr_terminal == "ADD"):
                self._match("ADD")
                self._parse_prior3()
                self._prefix.append(Terminal("ADD"))
                continue
            elif self._curr_terminal == "SUB":
                self._match("SUB")
                self._parse_prior3()
                self._prefix.append(Terminal("SUB"))
                continue
            else:
                return 

    # mul/div operations
    def _parse_prior3(self):
        self._parse_prior2()
        while True:
            if (self._curr_terminal == "MUL"):
                self._match("MUL")
                self._parse_prior2()
                self._prefix.append(Terminal("MUL"))
                continue
            elif self._curr_terminal == "DIV":
                self._match("DIV")
                self._parse_prior2()
                self._prefix.append(Terminal("DIV"))
                continue
            else:
                return 

    # unary operations
    def _parse_prior2(self):
        if self._curr_terminal == "NEG":
            self._match("NEG")
            self._parse_prior2()
            self._prefix.append(Terminal("NEG"))
        elif self._curr_terminal == "FUNC":
            temp = self._curr_terminal
            self._match("FUNC")
            self._match("LBRACE")
            self._parse_prior4()
            self._match("RBRACE")
            self._prefix.append(temp)
        else:
            self._parse_prior1()

    # atom operations
    def _parse_prior1(self):
        if self._curr_terminal == "NUM":
            self._prefix.append(self._curr_terminal)
            self._match("NUM")
        elif self._curr_terminal == "LBRACE":
            self._match("LBRACE")
            self._parse_prior4()
            self._match("RBRACE")
        else:
            raise SyntaxError("Unknown syntax")

    def _match(self, term: str):
        if self._curr_terminal == term:
            self._curr_terminal = self._lex.get_terminal()
        else:
            raise SyntaxError("Expected {}, got {}".format(term, self._curr_terminal))

    def parse(self, expr):
        self._lex.set_expr(expr)
        self._curr_terminal = self._lex.get_terminal()
        try:
            self._parse_prior4()
        except SyntaxError:
            raise
        return self._prefix

    def reset(self):
        self._lex.reset()
        self._curr_terminal = None
        self._prefix = []