# CO-project
CO Project group: B-46 institute -IIIT-D yr-2023: The provided code implements an assembler and simulator for a specific architecture or instruction set. It reads a code file provided from automated test cases, performs various checks on the code for syntax errors and semantic correctness, and generates the required outputs.

As per the given ISA all the instructions are implemented using functions defined at the beginning of the code code that updates all the registers, FLAGS register, variables. Then we have initialised dictionaries op(which stores the opcodes), reg(which stores the addresses of registers), regval(which stores the immediate values stored in the registers), empty dictionary var(which stores the immediate values stored in variables), mem(which stores the addresses of variables), labels(which stores the addresses of labels). We have also formed two functions for convertng binary to floating point numbers and vice-versa. Then we have read the file line by line assigned addresses to every instruction, labels and variables. We have done the required computations and after that we have updated all the register values and variable  if any happens we update the FLAGS register after each instruction.

Bonus part:
We have added 5 new instructions ourself with opcode:
10011 : nor r1 r2 r3 : this operation does nor of r2 and r3 then stores it in r1
10100 : nand r1 r2 r3 : this operation does nand of r2 and r3 then store ot in r1
10101 : xnor r1 r2 r3 : this operation does xnor of r2 and r3 then store it in r1
10110 : max r1 r2 : this instruction gets max of r1 and r2 then store it in r1
10111 : min r1 r2 : this instruction gets min of r1 and r2 then store it in r1
