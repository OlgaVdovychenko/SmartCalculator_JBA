import string
import re


def print_help():
    """
    Function describe the work of SmartCalculator
    """
    print("The program calculates the sum or subtraction of numbers")
    print("It supports both unary and binary minus operators")
    print("Remember: two adjacent minus signs turn into a plus")
    print('The program calculates the arithmetical expression')
    print('It supports all arithmetical operations and parentheses')
    print('The calculator supports both unary and binary minus operators')
    print('Remember: two adjacent minus signs turn into a plus.')
    print('Sequence of * and / will result an error message')
    print('The program supports the calculations with variables')
    print('If you want to stop calculations, enter "/exit"')


def do_operation(operation: str, operand_1, operand_2):
    """
    Function takes operator and two operands
    and returns the result of corresponding arithmetic operation.
    Possible operations:
    addition: +
    subtraction: -
    integer division: /
    multiplication: *
    power: ^
    For the case of an integer division, when division by zero,
    the function returns None
    :param operation: str (+, -, /, *, ^)
    :param operand_1: int or float
    :param operand_2: int or float
    :return: result of operation or None
    """
    if operation == '+':
        return operand_1 + operand_2
    elif operation == '-':
        return operand_1 - operand_2
    elif operation == '*':
        return operand_1 * operand_2
    elif operation == '/':
        try:
            return int(operand_1/operand_2)
        except ZeroDivisionError:
            print("You can't divide by zero")
            return None
    elif operation == '^':
        return operand_1 ** operand_2


def is_brackets_ok(expr):
    """
    Function checks the correctness of parentheses placement
    in arithmetic expression
    :param expr:
    :return: True (if parentheses placement is correct) or None
    """
    brackets_stack = []
    for elem in expr:
        if elem == '(':
            brackets_stack.append(elem)
        elif elem == ')':
            try:
                brackets_stack.pop()
            except IndexError:
                return False
    if brackets_stack:
        return False
    return True


def user_input_parsing(line):
    """
    Function parses the expression entered by user and returns list
    of operands and operations in infix notation.
    If variables are used in expression, the values of these variables
    will be substituted.
    In the case of incorrect expression or using the undefined variables,
    function returns None.
    :param line: srt
    :return: list of operands and operations in infix notation or None
    """
    # num_op = line.split()
    if not is_brackets_ok(line):
        print('Invalid expression')
        return None
    num_op = re.findall('[*/^+-]+|[0-9]+|[A-Za-z]+|[()]+', line)
    # print(num_op)
    if num_op[0] == '-':
        num_op[1] = '-' + num_op[1]
        num_op.pop(0)
    # print(num_op)
    for i in range(len(num_op)):
        if num_op[i][0] in '*/^+-' and not num_op[i][1:].isdigit() and len(num_op[i]) > 1:
            if num_op[i][0] == '+':
                num_op[i] = '+'
            elif num_op[i][0] == '-':
                if len(num_op[i]) % 2:
                    num_op[i] = '-'
                else:
                    num_op[i] = '+'
            else:
                print('Invalid expression')
                return None
        elif num_op[i].isalpha():
            if is_var_correct(num_op[i]):
                if num_op[i] in dict_user_input:
                    num_op[i] = dict_user_input[num_op[i]]
                else:
                    print('Unknown variable')
                    return None
            else:
                print('Invalid identifier')
                return None
        elif not num_op[i].isdigit() and not num_op[i][1:].isdigit() and not num_op[i] in '()*/^+-':
            print('Invalid expression')
            return None
    return num_op


def infix_to_postfix(infix_list):
    """
    Function converts the expression in infix notation to the
    postfix notation
    Function takes a list of operands and operators and returns the list
    of operands and operators in postfix notation
    :param infix_list: list
    :return: list of operand and operations in postfix notation
    """
    prec = {'(': 1, ')': 1,
            '+': 2, '-': 2,
            '*': 3, '/': 3,
            '^': 4}
    postfix_list = []
    operators_stack = []
    for token in infix_list:
        if token.isdigit() or token[1:].isdigit():
            postfix_list.append(token)
        elif token == '(':
            operators_stack.append(token)
        elif token == ')':
            top_token = operators_stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = operators_stack.pop()
        else:
            while operators_stack and prec[operators_stack[-1]] >= prec[token]:
                postfix_list.append(operators_stack.pop())
            operators_stack.append(token)
    while operators_stack:
        postfix_list.append(operators_stack.pop())
    return postfix_list


def postfix_eval(postfix_list):
    """
    Function evaluates the expression in postfix notation
    Function takes the list of operands and operators in postfix
    expression and returns the result of calculation,
    :param postfix_list: list of operands and operators in postfix notation
    :return: result of calculation
    """
    operand_stack = []
    for token in postfix_list:
        if token.isdigit() or token[1:].isdigit():
            operand_stack.append(int(token))
        else:
            operand_2 = operand_stack.pop()
            operand_1 = operand_stack.pop()
            result = do_operation(token, operand_1, operand_2)
            operand_stack.append(result)
    return operand_stack.pop()


def is_var_correct(var):
    """
    Function checks whether the name of variable is correct.
    In variable name only letters of Latin alphabet can be used.
    :param var: str, name of variable
    :return: True or False
    """
    for letter in var:
        if letter not in string.ascii_letters:
            return False
    return True


def assignment_parsing(inp_string):
    """
    Function parses the assignment statement and remembers
    the values of variables
    """
    lst = inp_string.replace(' ', '').split('=')
    if is_var_correct(lst[0]):
        if lst[1].isdigit():
            dict_user_input[lst[0]] = lst[1]
        elif is_var_correct(lst[1]):
            if lst[1] in dict_user_input:
                dict_user_input[lst[0]] = dict_user_input[lst[1]]
            else:
                print('Unknown variable')
        else:
            print('Invalid identifier')
    else:
        print('Invalid identifier')


def manage_calculation(line):
    """
    Function takes the expression and manage its processing
    :param line: str, expression
    :return: result of calculation
    """
    numbers_operations = user_input_parsing(line)
    if numbers_operations:
        if len(numbers_operations) == 1:
            return numbers_operations[0]
        else:
            # print(manage_calculation(numbers_operations))
            p_lst = infix_to_postfix(numbers_operations)
            # print(p_lst)
            return postfix_eval(p_lst)
    return None


dict_user_input = {}
if __name__ == "__main__":
    while True:
        user_input = input().strip()
        if user_input.startswith('/'):
            if user_input == '/exit':
                print('Bye!')
                break
            elif user_input == '/help':
                print_help()
            else:
                print('Unknown command')
        else:
            if len(user_input) == 0:
                continue
            else:
                if user_input[0].isalpha():
                    if user_input.isalpha():
                        if user_input in dict_user_input:
                            print(dict_user_input[user_input])
                        else:
                            print('Unknown variable')
                    elif '=' in user_input:
                        if user_input.count('=') > 1:
                            print('Invalid assignment')
                        else:
                            assignment_parsing(user_input)
                    else:
                        print(manage_calculation(user_input))
                else:
                    print(manage_calculation(user_input))
