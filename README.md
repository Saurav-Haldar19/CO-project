# CO-project
CO Project group:B-46 institue -IIIT-D yr-2023: The provided code seems to be an implementation of an assembler for a specific architecture or instruction set. It reads an assembly code file, performs various checks on the code for syntax errors and semantic correctness, and generates binary machine code as output.

As per the given ISA all the instructions are implemented using functions defined at the beginning of the code code that updates all the registers, FLAGS register, variables.
Then we have initialised dictionaries op(which stores the opcodes), reg(which stores the addresses of registers), regval(which stores the immediate values stored in the registers), empty dictionary var(which stores the immediate values stored in variables), mem(which stores the addresses of variables), labels(which stores the addresses of labels).
Then we have read the file line by line assigned addresses to every instruction, labels and variables.
Then if no error is encountered we have converted the code in machine code and after that we have updated all the register values and variable values and checked for overflows if any happens we upadte the FLAGS register after each instruction.
And then finally if there is no error the machine code is written on the binary file else the error name with the line no is written on the output file.
