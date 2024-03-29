# Enhanced-NES-Emulation-Framework - MarioEmulator

![DALL·E 2024-01-09 22 07 08 - A logo for a NES Emulator repository, featuring the 6502 processor  The logo should have a retro style, reminiscent of the NES era  It should include ](https://github.com/dwipddalal/Enhanced-NES-Emulation-Framework/assets/91228207/01482431-ebb0-4d21-a07b-861c8d64bb72)


Status of work:
- Currently I am working on code and process documentation for this emulator written in python.
- Working on adding additional features that were not present in the original NES
  
- [Here](https://github.com/dwipddalal/C-emulator), I am working on writing the same code in C++ for faster performance.

Level of Abstraction in CPU 6502

## What it looks like!
<img width="743" alt="image" src="https://github.com/dwipddalal/Enhanced-NES-Emulation-Framework/assets/91228207/24abdd17-3a4b-465a-a1b3-2a01a76cc92a">



### Emulation Process

- Upon initializing, the emulator loads a ROM file, which is the game to be played. It sets up the emulated environment, including CPU, PPU, and memory.
- It enters a main loop, akin to the NES's own operational cycle. In this loop, it executes CPU instructions, updates the PPU for graphics, and handles input from the controllers.
- The emulator manages interrupts, crucial for timing and synchronization in games, through the `Interrupter` class.
- It simulates the original NES display on a modern screen, including options for scaling the display to suit different resolutions.

### Save States and User Interaction

- Unique to emulators is the ability to save and load the exact state of the game at any point, a feature not available on the original NES hardware. This is handled through Python's `pickle` module.
- The emulator also incorporates additional user interaction features like a heads-up display (HUD) toggle and real-time performance metrics (like FPS).

**INSTRUCTION_SET Dictionary**:
   - This is a comprehensive dictionary mapping instruction mnemonics (like "ADC", "AND", "ASL", etc.) to their corresponding `InstructionSet`. Each `InstructionSet` contains:
     - The name of the instruction.
     - A dictionary of `AddressModes` to `Instruction` objects, detailing how the instruction behaves with different addressing modes, including the opcode (bytecode), the size of the instruction in bytes, and the number of CPU cycles it takes to execute.


## References
   - https://github.com/docmarionum1/py65emu
   - https://www.masswerk.at/6502/6502_instruction_set.html
   - http://www.obelisk.me.uk/6502/addressing.html
   - https://www.csh.rit.edu/~moffitt/docs/6502.html
   - https://github.com/jameskmurphy/nes/tree/main
   - http://www.6502.org/tutorials/vflag.html
   - http://www.6502.org/tutorials/decimal_mode.html
   - http://6502.org/tutorials/6502opcodes.html#PC
   - https://www.masswerk.at/6502/assembler.html
   - https://www.pagetable.com/?p=410
   - http://www.righto.com/2012/12/the-6502-overflow-flag-explained.html



