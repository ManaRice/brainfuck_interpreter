import sys
import os
import numpy as np

BF_CHARSET     = "<>+-[].,"     # The brainfuck charset

def safe_open(file_path):
    f = None
    try:
        f = open(file_path, "r")
        return f
    except:
        print(f"Could not find file {file_path}")
        sys.exit()

def safe_create(name, number=-1):
    f = None
    try:
        if number < 0:
            f = open(name, "w")
        else:
            f = open(f"{name}{number}", "w")
        return f
    except:
        return safe_create(name, number+1)

# If i want to do some kind of option support in the future
def usage():
    print("usage:")
    print("bf <file1.bf> ")


def translate(file):

    depth = 0

    index = 0

    python_file = safe_create("bf_program.py")
    bf_code_string  = file.read()

    bf_code = ""
    for c in bf_code_string:
        if c in BF_CHARSET:
            bf_code += c

    python_file.write("""
import sys
import numpy as np
TAPE_LENGTH    = 10000             # Length of internal 'tape'. Reffered to tape as homage to the Turing Mashine

tape            = np.zeros(TAPE_LENGTH, dtype=int)      # Tape is a numpy array of ints that is prefilled with zeros
pointer         = 0                                     # Pointer is the variable that points to a cell
loop_depth_list = list()                                # Used as LIFO dequeue or similar to stor the indexes we want to jump to at the end of the loop
index           = 0                                     # Currently read character of the program
""")


    # Loop through the program until the index has surpassed the code length aka EOF
    while index < len(bf_code):

        char = bf_code[index] # Set char to currently read character of the bf program

        if char == '<':
            handle_pointer_left(python_file,depth)
        if char == '>':
            handle_pointer_right(python_file,depth)
        if char == '+':
            handle_plus(python_file,depth)
        if char == '-':
            handle_minus(python_file,depth)
        if char == '[':
            depth = handle_open_bracket(python_file,depth)
        if char == ']':
            depth -= 1
        if char == '.':
            handle_output(python_file,depth)
        if char == ',':
            handle_input(python_file,depth)

        index += 1


    python_file.close()



def run():
    os.system("python bf_program.py")

def handle_pointer_left(file,depth):
    tabs = ""
    for i in range(depth):
        tabs += "\t"
    file.write(f"{tabs}pointer -= 1\n")

def handle_pointer_right(file,depth):
    tabs = ""
    for i in range(depth):
        tabs += "\t"
    file.write(f"{tabs}pointer += 1\n")

def handle_plus(file,depth):
    tabs = ""
    for i in range(depth):
        tabs += "\t"
    file.write(f"{tabs}tape[pointer] += 1\n")

def handle_minus(file,depth):
    tabs = ""
    for i in range(depth):
        tabs += "\t"
    file.write(f"{tabs}tape[pointer] -= 1\n")

def handle_open_bracket(file,depth):
    tabs = ""
    for i in range(depth):
        tabs += "\t"
    file.write(f"{tabs}while tape[pointer] != 0:\n")
    return depth+1

def handle_output(file,depth):
    tabs = ""
    for i in range(depth):
        tabs += "\t"
    file.write(f"{tabs}print(chr(tape[pointer]), end='', flush=True)\n")
def handle_input(file,depth):
    tabs = ""
    for i in range(depth):
        tabs += "\t"
    file.write(f"{tabs}tape[pointer] = ord(sys.stdin.read(1))\n")

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
    translate(bf_file)
    run()

    # Close the file before exit
    bf_file.close()
