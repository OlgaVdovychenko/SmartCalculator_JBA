import string
import re


def print_help():
    print("The program calculates the sum or subtraction of numbers")
    print("It supports both unary and binary minus operators")
    print("Remember: two adjacent minus signs turn into a plus.")


def do_addition(a, b):
    return a + b


def do_subtraction(a, b):
    return a - b


def do_multiplication(a, b):
    return a * b


def do_division(a, b):
    try:
        return int(a / b)
    except ZeroDivisionError:
        print("You can't divide by zero")
        return None


def do_power(a, b):
    return a ** b


def do_operation(operation, operand_1, operand_2):
    if operation == '+':
        return do_addition(operand_1, operand_2)
    elif operation == '-':
        return do_subtraction(operand_1, operand_2)
    elif operation == '*':
        return do_multiplication(operand_1, operand_2)
    elif operation == '/':
        return do_division(operand_1, operand_2)
    elif operation == '^':
        return do_power(operand_1, operand_2)


def manage_calculation(num_op):
    operand_1 = num_op.pop(0)
    result = None
    while len(num_op) >= 2:
        operation = num_op.pop(0)
        operand_2 = num_op.pop(0)
        result = do_operation(operation, operand_1, operand_2)
        operand_1 = result
    return result


def is_brackets_ok(expr):
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
        elif not num_op[i].isdigit() and num_op[i][1:].isdigit() and not num_op[i] in '()*/^+-':
            print('Invalid expression')
            return None
    return num_op


def infix_to_postfix(infix_list):
    prec = dict()
    prec['('] = 1
    prec[')'] = 1
    prec['^'] = 4
    prec['*'] = 3
    prec['/'] = 3
    prec['+'] = 2
    prec['-'] = 2

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
    for letter in var:
        if letter not in string.ascii_letters:
            return False
    return True


def assignment_parsing(inp_string):
    lst = inp_string.replace(' ', '').split('=')
    # print(lst)
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


def input_with_var(inp_string):
    # lst = inp_string.split()
    lst = re.findall('[*/^+-]+|[0-9]+|[A-Za-z]+|[()]+', inp_string)
    #print(lst)
    for i in range(len(lst)):
        if lst[i].isalpha():
            if is_var_correct(lst[i]):
                if lst[i] in dict_user_input:
                    lst[i] = dict_user_input[lst[i]]
                else:
                    print('Unknown variable')
                    return None
            else:
                print('Invalid identifier')
                return None
    return lst


dict_user_input = {}
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
                        # print(dict_user_input)
                else:
                    numbers_operations = user_input_parsing(user_input)
                    if numbers_operations:
                        if len(numbers_operations) == 1:
                            print(numbers_operations[0])
                        else:
                            # print(manage_calculation(numbers_operations))
                            p_lst = infix_to_postfix(numbers_operations)
                            # print(p_lst)
                            print(postfix_eval(p_lst))
            else:
                numbers_operations = user_input_parsing(user_input)
                if numbers_operations:
                    if len(numbers_operations) == 1:
                        print(numbers_operations[0])
                    else:
                        # print(manage_calculation(numbers_operations))
                        p_lst = infix_to_postfix(numbers_operations)
                        # print(p_lst)
                        print(postfix_eval(p_lst))
