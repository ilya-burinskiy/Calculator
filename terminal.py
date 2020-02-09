class Terminal:

    def __init__(self, name=None, attr=None):
        self._name = name
        self._attr = attr

    @classmethod
    def from_char(cls, char):
        if char == '+':
            return cls("ADD")
        if char == '-':
            return cls("SUB")
        if char == '*':
            return cls("MUL")
        if char == '/':
            return cls("DIV")
        if char == '(':
            return cls("LBRACE")
        if char == ')':
            return cls("RBRACE")

    @property
    def name(self):
        return self._name
    
    @property
    def attr(self):
        return self._attr

    def __eq__(self, other: str):
        return self._name == other

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone

    def __hash__(self):
        return hash(self._name)

    def __str__(self):
        return "<{},{}>".format(self._name, self._attr)

    def __repr__(self):
        return "<{},{}>".format(self._name, self._attr)
