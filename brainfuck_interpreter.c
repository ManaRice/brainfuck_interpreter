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


int *prepare_jumps(char *code, size_t code_size)
{
    int *jumps = malloc(code_size * sizeof(int));
    if (jumps == NULL)
    {
        puts("Malloc failed");
        exit(1);
    }

    int code_index = 0;
    int open_bracket_index;
    int depth = 0;
    for (;code_index < code_size; code_index++)
    {
        if (code[code_index] != '[')
            continue;

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
    return jumps;
}


void interpret(FILE *file)
{
    size_t code_size = 0;
    char *code = read_code(file, &code_size);
    int *jumps = prepare_jumps(code, code_size);


    unsigned char tape[TAPE_LENGTH];
    int pointer = 0;


    long code_index = 0;

    for (;code_index < code_size; code_index++)
    {
        switch(code[code_index])
        {
            case '<':
                if (pointer == 0)
                    pointer = TAPE_LENGTH - 1;
                else
                    pointer--;
                break;

            case '>':
                if (pointer == TAPE_LENGTH - 1)
                    pointer = 0;
                else
                    pointer++;
                break;

            case '+':
                if (tape[pointer] == MAX_CELL_VALUE)
                    tape[pointer] = 0;
                else
                    tape[pointer]++;
                break;

            case '-':
                if (tape[pointer] == 0)
                    tape[pointer] = MAX_CELL_VALUE;
                else
                    tape[pointer]--;
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
        printf("Could not open file %s\n", argv[0]);
        exit(1);
    }

    interpret(file);

    fclose(file);
}
