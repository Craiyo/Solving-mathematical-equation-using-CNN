import sympy as sp
import re


def add_asterisk_to_x(string):
        operators = ['+', '-', '*', '/', '^']  # List of arithmetic operators
        result = ""

        i = 0
        while i < len(string):
            if string[i] == 'x':  # Check if current character is 'x'
                if i > 0 and string[i - 1].isdigit():
                    # If previous character is a digit, add '*' to the result string
                    result += '*'
                result += 'x'  # Add 'x' to the result string
                i += 1
                if i < len(string) and string[i].isdigit():
                    # If next character is a digit, add '**' to the result string
                    result += '**'
            elif string[i] in operators:
                # If current character is an arithmetic operator, add it to the result string
                result += string[i]
                i += 1
            else:
                # If current character is not 'x' or an arithmetic operator, add it to the result string
                result += string[i]
                i += 1

        return result


def transform(string):
    result = ""
    i = 0
    while i < len(string):
        if string[i] == 'x':  # Check if current character is 'x'
            result += 'x'  # Add 'x' to the result string
            i += 1
            if i < len(string) and string[i].isdigit():
                # If next character is a digit, add '^' to the result string
                result += '^'
        else:
            result += string[i]  # Add current character to the result string
            i += 1

    return result


def reverse_transform(expr):
    # Replace 'x^' with 'x**'
    expr = expr.replace('^', '**')
    # Replace 'x' followed by a digit with 'x*' followed by the digit
    expr = re.sub(r'x(\d)', r'x*\1', expr)
    return expr


def polynomial(equation):
        expr = sp.S(add_asterisk_to_x(equation))
        root = sp.roots(expr, sp.Symbol('x'))
        return root


def integration(equation):
        expr = sp.simplify(add_asterisk_to_x(equation))
        root = sp.integrate(expr, sp.Symbol('x'))
        root = sp.simplify(root)
        return root


def differentiate(equation):
        expr = sp.simplify(add_asterisk_to_x(equation))
        root = sp.differentiate_finite(expr, sp.Symbol('x'))
        root = sp.simplify(root)
        return root
