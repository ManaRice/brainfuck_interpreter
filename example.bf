Brainfuck code taken from wikipedia and slightly modified

This code takes the values of Cell #0 and Cell #1 as the dividend and divisor respecivly
and thereafter leaves the quotient in Cell #2 and outputs to stdout
I've added so that we can output the result as ascii if the result is one digit long

Starting tape

0 0 0 0 0 0 0 0 0
^

Load Values
++++++>++

9 3 0 0 0 0 0 0 0
  ^

Duplicate Values
<[->>+>+<<<]>>>[-<<<+>>>]<<[->>+>+<<<]>>>[-<<<+>>>]<<

9 3 9 3 0 0 0 0 0
^

I Cant decipher this monster
Way to nested to do that
[>[>>>>[-]<<<<<[->>+>>>+<<<<<]>>[-<<+>>]<[-<->>+<<[>>-<<[->>>+<<<]
]>>>[-<<<+>>>]<[-<[-]>]<]<[<[->>+>+<<<]>>>[-<<<+>>>]>>+<<<<[->>+<<]]>>[-<<+
>>]<]<<[->+>+<<]>[-<+>]>>>>>[-<<+<+>>>]<<<[-<->]+<[>-<[-]]>[>[-]>+<<-]<<][-
]>[-]>>[-<<+>>]>[-<<<<+>>>>]<<<

6 2 3 0 0 0 0 0 0
      ^
Add 48 to make it the ascii value for 3 in this case 51
+++++++[<+++++++>-]<-.

6 2 51 0 0 0 0 0 0
    ^
