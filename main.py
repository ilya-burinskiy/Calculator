import sys
from calculator import Calculator

def _main():
    c = Calculator()
    res = None
    expr = input("Enter math expression: ")
    while expr:
        try:
            res = c.calculate(expr)
        except SyntaxError as se:
            print(str(se))
        except ZeroDivisionError as zd:
            print(str(zd))
        except ValueError as ve:
            print(str(ve))
        else:
            print(res)
            c.reset()
            expr = input("Enter math expression: ")
        
if __name__ == "__main__":
    _main()