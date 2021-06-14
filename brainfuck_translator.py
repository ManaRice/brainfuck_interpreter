import sys
import os
import numpy as np

BF_CHARSET = "<>+-[].,"     # The brainfuckk charset
CC         = "gcc"          # The c compiler
CC_OPTS    = "-O2"          # Compiler options

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


def translate(file, filename):
    # Create or open exising c file with filename
    c_file = open(f"{filename}.c", "w")

    # Create list of characters that are only the bf code
    bf_code = [c for c in file.read() if c in BF_CHARSET]

    # Write the c "header"
    c_file.write(
"""\
/*
    Generated with ManaRice brainfuck translator
*/

#include <stdio.h>

unsigned char tape[32768];
int pointer = 0;

int main()
{
""")

    # Instruction index
    index = 0

    # Loop through the program until the index has surpassed the code length aka EOF
    while index < len(bf_code):

        char = bf_code[index] # Set char to currently read character of the bf program

        # Generate c code for all the bf characters
        if char == '<':
            c_file.write("pointer--;\n")
        if char == '>':
            c_file.write("pointer++;\n")
        if char == '+':
            c_file.write("tape[pointer]++;\n")
        if char == '-':
            c_file.write("tape[pointer]--;\n")
        if char == '[':
            c_file.write("while (tape[pointer] != 0) {\n")
        if char == ']':
            c_file.write("}\n")
        if char == '.':
            c_file.write("putchar(tape[pointer]);\nfflush(stdout);\n")
        if char == ',':
            c_file.write("tape[pointer] = getchar();\n")

        index += 1

    # Write the end of main curly brace and close the file
    c_file.write("puts(\"\");\n")
    c_file.write("}\n")
    c_file.close()

# Function that compiles the code and runs the compiled file
def run(filename):
    os.system(f"{CC} {CC_OPTS} {filename}.c -o {filename}")
    if os.name == "posix":
        os.system(f"./{filename}")
    if os.name == "nt":
        os.system(filename)


if __name__ == "__main__":
    argv = sys.argv[1:]
    argc = len(argv)

    # Making sure we have a filename atleast or exit
    if argc < 1:
        usage()
        sys.exit()

    filename, fileending = argv[0].split('.')

    # Open the file
    bf_file = safe_open(argv[0])

    # Run translator
    translate(bf_file, filename)
    # Compile and run executable
    run(filename)

    # Close the file before exit
    bf_file.close()
