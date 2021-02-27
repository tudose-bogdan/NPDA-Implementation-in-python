import os

start_input = ""

###### Ordine de citire automat ######

states = []

symbols = []

stack_symbols = []

start_symbol = ""

start_stack = ""

acceptable_states = []

# E - accept on empty stack or F - acceptable state (default is false)
accept_with = ""

# production rules ("read input", "pop stack", "push stack", "next state")
productions = {}

###### ######


def parse_file(filename):
    global productions
    global start_symbol
    global start_stack
    global acceptable_states
    global accept_with

    lines = [line.rstrip() for line in open(filename)]

    # Citim incepand cu linia a 3-a starea de inceput
    # pentru stiva si stari + stari finale + productii

    start_symbol = lines[3]

    start_stack = lines[4]

    acceptable_states.extend(lines[5].split())

    # E - accept on empty stack or F - acceptable state (default is false)
    accept_with = lines[6]

    # Pentru fiecare stare care apare intr-o productie creeam o lista cu posibile viitoare
    # stari in functie de input
    for i in range(7, len(lines)):
        production = lines[i].split()

        configuration = [(production[1], production[2],
                          production[4], production[3], production[5])]

        # Daca apare pentru prima data starea sursa
        # initializam cu lista vida
        if not production[0] in productions.keys():
            productions[production[0]] = []

        configuration = [tuple(s if s != "e" else "" for s in tup)
                         for tup in configuration]

        productions[production[0]].extend(configuration)

    print('Reguli: ', productions)
    print('Simbol start', start_symbol)
    print('Stiva initiala', start_stack)
    print('Stari finale', acceptable_states)
    print('Metoda de acceptare(Empty-E, Final State-F)', accept_with)

    return 1


def translator(inputWord, state, stack, output):
    print(inputWord, state, stack, output)
    if accept_with == 'F':
        if inputWord == []:
            if state in acceptable_states:
                print(output)

    if accept_with == 'E':
        if inputWord == [] and stack == []:
            print(output)

    if inputWord == []:
        char = ''
    else:
        char = inputWord[0]
        inputWord = inputWord[1:]

    if stack == []:
        stack_head = ''
    else:
        stack_head = stack.pop(-1)

    # Nonlambda
    if state in productions.keys():
        for inp, req, push, newState, write in productions[state]:
            if inp == char and stack_head != '' and stack_head == req:
                aux = [c for c in push]
                aux.reverse()
                n_stack = stack + aux
                n_output = output + write
                translator(inputWord, newState, n_stack, n_output)
            if req == '':
                aux = [c for c in push]
                aux.reverse()
                n_stack = stack + [stack_head] + aux
                n_output = output + write
                translator(inputWord, newState, n_stack, n_output)

    # Lambda
    if state in productions.keys():
        for inp, req, push, newState, write in productions[state]:
            if inp == '' and stack_head != '' and stack_head == req:
                aux = [c for c in push]
                aux.reverse()
                n_stack = stack + aux
                n_output = output + write
                translator([char]+inputWord, newState, n_stack, n_output)
            if req == '':
                aux = [c for c in push]
                aux.reverse()
                n_stack = stack + [stack_head] + aux
                n_output = output + write
                translator([char]+inputWord, newState, n_stack, n_output)


parse_file('automat_test_r.txt')

inputWord = input()
while inputWord != 'stop':
    stack = [start_stack]
    word = [c for c in inputWord]
    translator(word, start_symbol, stack, '')
    inputWord = input('New word\n')
