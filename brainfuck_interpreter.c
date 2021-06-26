#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BF_CHARSET "<>+-[].,"
#define MAX_CELL_VALUE 255
#define TAPE_LENGTH 32768

char *read_code(FILE *file, size_t *return_codesize)
{
    char *code;
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    code = malloc(file_size);
    if (code == NULL)
    {
        puts("Malloc failed");
        exit(1);
    }

    char c;

    while ((c = fgetc(file)) != EOF)
    {
        if (strchr(BF_CHARSET, c))
            code[(*return_codesize)++] = (char)c;
    }

    code[(*return_codesize)] = '\0';

    return code;
}

void print_jumps(int *jumps, size_t code_size)
{
    int index = 0;
    while (index < code_size)
    {
        printf("%d ", jumps[index]);
        index++;
    }
}

int *prepare_jumps(char *code, size_t code_size)
{
    int *jumps = calloc(code_size, sizeof(int));
    if (jumps == NULL)
    {
        puts("Calloc failed");
        exit(1);
    }

    for (int code_index = 0; code_index < code_size; code_index++)
    {
        // Handle the loops
        if (code[code_index] == '[')
        {
            int open_bracket_index;
            int depth = 0;

            open_bracket_index = code_index;
            code_index++;

            while (code_index < code_size)
            {
                if (code[code_index] == '[')
                    depth++;
                if (code[code_index] == ']')
                {
                    if (depth > 0)
                        depth--;
                    else
                    {
                        jumps[open_bracket_index] = code_index;
                        jumps[code_index] = open_bracket_index;
                        code_index = open_bracket_index;
                        break;
                    }
                }
                code_index++;
            }
        }

        // Handle pointer moves
        if (code[code_index] == '<' ||
            code[code_index] == '>')
        {

            if (code[code_index + 1] != '<' &&
                code[code_index + 1] != '>')
                continue;

            int start_index = code_index;
            int move_count = 0;

            while(code[code_index] == '<' ||
                  code[code_index] == '>')
            {
                  switch (code[code_index])
                  {
                      case '<': move_count--; break;
                      case '>': move_count++; break;
                  }
                  code_index++;
            }

            jumps[start_index] = code_index - 1;
            jumps[start_index + 1] = move_count;
            code_index--;
        }

        // Handle increments and decrements
        if (code[code_index] == '+' ||
            code[code_index] == '-')
        {
            if (code[code_index + 1] != '+' &&
                code[code_index + 1] != '-')
                continue;

            int start_index = code_index;
            int increment_count = 0;

            while(code[code_index] == '+' ||
                  code[code_index] == '-')
            {
                  switch (code[code_index])
                  {
                      case '+': increment_count++; break;
                      case '-': increment_count--; break;
                  }
                  code_index++;
            }

            //printf("increment_count: %d ", increment_count);
            jumps[start_index] = code_index - 1;
            jumps[start_index + 1] = increment_count;
            code_index--;
        }

    }
    return jumps;
}

void interpret(FILE *file)
{
    size_t code_size = 0;
    char *code = read_code(file, &code_size);
    int *jumps = prepare_jumps(code, code_size);

    unsigned char tape[TAPE_LENGTH];
    int pointer = 0;

    //printf("%s\n", code);
    //print_jumps(jumps, code_size);

    for (int code_index = 0; code_index < code_size; code_index++)
    {
        switch(code[code_index])
        {
            case '<':
                if (jumps[code_index] == 0)
                {
                    pointer--;
                    break;
                }
                pointer += jumps[code_index + 1];
                code_index = jumps[code_index];
                break;

            case '>':
                if (jumps[code_index] == 0)
                {
                    pointer++;
                    break;
                }
                pointer += jumps[code_index + 1];
                code_index = jumps[code_index];
                break;

            case '+':
                if (jumps[code_index] == 0)
                {
                    tape[pointer]++;
                    break;
                }
                tape[pointer] += jumps[code_index + 1];
                code_index = jumps[code_index];
                break;

            case '-':
                if (jumps[code_index] == 0)
                {
                    tape[pointer]--;
                    break;
                }
                tape[pointer] += jumps[code_index + 1];
                code_index = jumps[code_index];
                break;

            case '[':
                if (tape[pointer] == 0)
                    code_index = jumps[code_index];
                break;
            case ']':
                if (tape[pointer] != 0)
                    code_index = jumps[code_index];
                break;
            case '.':
                putchar(tape[pointer]);
                fflush(stdout);
                break;
            case ',':
                tape[pointer] = getchar();
                break;
            default:
                puts("Found unknown char");
                exit(1);
                break;
        }
    }
    puts("");
    free(jumps);
    free(code);
}

int main(int argc, char **argv)
{
    FILE *file;

    if (argc < 2)
    {
        puts("File needs to be specifyed");
        exit(1);
    }

    file = fopen(argv[1], "r");

    if (file == NULL)
    {
        printf("Could not open file %s\n", argv[1]);
        exit(1);
    }

    interpret(file);

    fclose(file);
}
