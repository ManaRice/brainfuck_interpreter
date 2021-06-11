'''
    A Brainfuck interpreter made in the most naive way possible by ManaRice

    Made for the purpose of wanting one and thinking it wasn't to hard to create one myself
    I made some silly choises on the way of implementing, but i didn't bother to care

    Example run, any file and extension allowed:

        python brainfuck_interpreter.py example.bf
'''

import sys
import os
import time
import numpy as np

TAPE_LENGTH    = 10000          # Length of internal 'tape'. Reffered to tape as homage to the Turing Mashine
MAX_CELL_VALUE = 255            # Max value at each cell of the 'tape'
RUN_SLOW       = False          # If you want the interpreter to run slower than usual. For debugging mostly
BF_CHARSET     = "<>+-[].,"     # The brainfuck charset


# Function to open file by Filepath or exit if the file was not found
def safe_open(file_path):
    f = None
    try:
        f = open(file_path, "r")
        return f
    except:
        print(f"Could not find file {file_path}")
        sys.exit()

# If i want to do some kind of option support in the future
def usage():
    print("usage:")
    print("bf <file1.bf> ")

# Just print message and exits
def raise_error(message):
    print(message)
    sys.exit()

# This is the ugly interpreter that takes in the bf file
def interpret(file):


    tape            = np.zeros(TAPE_LENGTH, dtype=int)      # Tape is a numpy array of ints that is prefilled with zeros
    pointer         = 0                                     # Pointer is the variable that points to a cell
    loop_depth_list = list()                                # Used as LIFO dequeue or similar to stor the indexes we want to jump to at the end of the loop
    bf_code_string  = file.read()                           # Read the file into a sting we can index character by character
    index           = 0                                     # Currently read character of the program

    # Remove the unnessesary characters from the file
    # Not the best code, but it works i guess
    bf_code = ""
    for c in bf_code_string:
        if c in BF_CHARSET:
            bf_code += c

    # Loop through the program until the index has surpassed the code length aka EOF
    while index < len(bf_code):

        if RUN_SLOW:
            time.sleep(0.01) # Mostly used for debugging


        char = bf_code[index] # Set char to currently read character of the bf program

        # Decrement pointer, wrap if below zero
        if char == '<':

            if pointer == 0:
                pointer = TAPE_LENGTH-1
            else:
                pointer -= 1

        # Increment pointer, wrap if above TAPE_LENGTH
        if char == '>':

            if pointer == TAPE_LENGTH-1:
                pointer = 0
            else:
                pointer += 1

        # Increment the number in the pointed cell
        if char == '+':

            if tape[pointer] == MAX_CELL_VALUE:
                tape[pointer] = 0
            else:
                tape[pointer] += 1

        # Decrement the number in the pointed cell
        if char == '-':

            if tape[pointer] == 0:
                tape[pointer] = MAX_CELL_VALUE
            else:
                tape[pointer] -= 1

        # Begin loop
        if char == '[':
            # If current cell is not zero, save index in list to loop back to
            if tape[pointer] != 0:
                loop_depth_list.append(index)
            # Else, we find the corresponding closing bracket and begin the execution from there
            else:
                # We use this try statement to ensure an closing bracket, otherwise we raise an "syntax error"
                try:
                    # Save the bracket depth so we can stop at the right corresponding bracket
                    bracket_depth = 0
                    while True:
                        index += 1
                        # Increase bracket depth if we find opening bracket
                        if bf_code[index] == '[':
                            bracket_depth += 1
                        # Decrease bracket depth if we find closing bracket if this isnt the corresponding bracket
                        if bf_code[index] == ']':
                            if bracket_depth == 0:
                                break
                            bracket_depth -= 1
                except:
                    raise_error("Missing ] (closing bracket)")

        # Loop back to the corresponding loop or raise "Syntax error"
        if char == ']':
            if len(loop_depth_list) != 0:
                index = loop_depth_list.pop()
                continue
            else:
                raise_error("Missing [ (opening bracket) to ] (closing bracket)")

        # Output the currently pointed cells value as ascii char
        if char == '.':
            print(chr(tape[pointer]), end='', flush=True)

        # Print the current buffered output and get a char as input and appent the ascii value to the currently pointed cell
        if char == ',':
            tape[pointer] = ord(sys.stdin.read(1))

        # Read next character from bf program
        index += 1


if __name__ == "__main__":
    argv = sys.argv[1:]
    argc = len(argv)

    # Making sure we have a filename atleast or exit
    if argc < 1:
        usage()
        sys.exit()

    # Open the file
    bf_file = safe_open(argv[0])

    # Run interpreter
    interpret(bf_file)

    # Close the file before exit
    bf_file.close()
