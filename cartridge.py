from .memory import MemoryBase

class CartridgeBase(MemoryBase):
    """
    Base class for NES cartridges. Cartridges provide separate memory spaces for the CPU and PPU.
    This is facilitated through read_ppu and write_ppu methods for PPU memory access.
    """

    def __init__(self):
        super().__init__()
        self.nametable_mirror = None

    def read_ppu(self, address):
        """Read a byte from the PPU memory. Must be implemented in subclasses."""
        raise NotImplementedError()

    def write_ppu(self, address, value):
        """Write a byte to the PPU memory. Must be implemented in subclasses."""
        raise NotImplementedError()


class NESCartridgeType0(CartridgeBase):
    """
    Represents a basic NES Cartridge (Type 0 / MMC0). 
    Includes up to 8kB RAM, 32kB PRG ROM, and 8kB CHR ROM.
    """
    RAM_START_ADDRESS = 0x6000
    PRG_ROM_START_ADDRESS = 0x8000
    CHR_ROM_START_ADDRESS = 0x0000

    def __init__(self, prg_rom_data=None, chr_rom_data=None, ram_kb_size=8, prg_rom_start=None, nametable_mirror=(0, 0, 1, 1)):
        super().__init__()

        # Initialize RAM (CPU connected)
        if ram_kb_size not in [2, 4, 8]:
            raise ValueError("RAM size for Cartridge Type 0 should be 2, 4, or 8kB")
        self.cpu_ram = bytearray(ram_kb_size * 1024)

        # Initialize PRG ROM with supplied data (CPU connected)
        self.prg_rom = bytearray(prg_rom_data)
        if len(self.prg_rom) not in [16 * 1024, 32 * 1024]:
            raise ValueError("PRG ROM size for Cartridge Type 0 should be 16 or 32kB")

        # Initialize CHR ROM with supplied data (PPU connected), or use RAM if not supplied
        if chr_rom_data:
            self.chr_memory = bytearray(chr_rom_data)
            if len(self.chr_memory) != 8 * 1024:
                raise ValueError("CHR ROM size for Cartridge Type 0 should be 8kB")
        else:
            self.chr_memory = bytearray(8 * 1024)  # Use RAM

        self.prg_rom_start_address = prg_rom_start if prg_rom_start else self.PRG_ROM_START_ADDRESS
        self.nametable_mirror = nametable_mirror

    def read(self, address):
        """Reads from either RAM or PRG ROM based on the address."""
        if address < self.PRG_ROM_START_ADDRESS:
            # Access RAM
            return self.cpu_ram[address % len(self.cpu_ram)]
        else:
            # Access PRG ROM
            return self.prg_rom[(address - self.prg_rom_start_address) % len(self.prg_rom)]

    def write(self, address, value):
        """Writes to RAM. Writing to ROM has no effect and issues a warning."""
        if address < self.PRG_ROM_START_ADDRESS:
            # Write to RAM
            self.cpu_ram[address % len(self.cpu_ram)] = value
        else:
            # Attempt to write to ROM, which should not be possible
            print("WARNING: Attempt to overwrite PRG ROM")

    def read_ppu(self, address):
        """Reads a byte from CHR memory."""
        return self.chr_memory[address % len(self.chr_memory)]

    def write_ppu(self, address, value):
        """Writes a byte to CHR memory, usually not allowed so it issues a warning."""
        print("WARNING: Attempt to overwrite CHR ROM")
        self.chr_memory[address % len(self.chr_memory)] = value
