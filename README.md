# Enhanced-NES-Emulation-Framework

![DALL·E 2024-01-09 22 07 08 - A logo for a NES Emulator repository, featuring the 6502 processor  The logo should have a retro style, reminiscent of the NES era  It should include ](https://github.com/dwipddalal/Enhanced-NES-Emulation-Framework/assets/91228207/01482431-ebb0-4d21-a07b-861c8d64bb72)


Level of Abstraction in CPU 6502


The NES game used on this Emulator is Super Mario taken from [this](https://www.nesfiles.com/NES/Super_Mario_Bros/) website


<img width="748" alt="image" src="https://github.com/dwipddalal/Enhanced-NES-Emulation-Framework/assets/91228207/29fc1cef-4ea3-409c-baa5-e18b418bb229">





**INSTRUCTION_SET Dictionary**:
   - This is a comprehensive dictionary mapping instruction mnemonics (like "ADC", "AND", "ASL", etc.) to their corresponding `InstructionSet`. Each `InstructionSet` contains:
     - The name of the instruction.
     - A dictionary of `AddressModes` to `Instruction` objects, detailing how the instruction behaves with different addressing modes, including the opcode (bytecode), the size of the instruction in bytes, and the number of CPU cycles it takes to execute.



