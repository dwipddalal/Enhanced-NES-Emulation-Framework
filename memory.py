import logging

OAM_SIZE_BYTES = 256

class MemoryBase:
    """Defines the basic memory controller interface."""
    def read(self, address):
        """Reads a byte from a given address. Must be implemented by subclasses."""
        raise NotImplementedError()

    def read_block(self, address, num_bytes):
        """Reads a block of bytes from memory."""
        block = bytearray(num_bytes)
        for i in range(num_bytes):
            block[i] = self.read(address + i)
        return block

    def write(self, address, value):
        """Writes a byte to a given address. Must be implemented by subclasses."""
        raise NotImplementedError()

    def print_memory(self, address, num_bytes, width_bytes=16):
        """Prints a block of memory in a formatted manner."""
        for offset in range(num_bytes):
            if offset % width_bytes == 0:
                if offset > 0:
                    print()
                print(f"${address + offset:04X}:   ", end="")
            value = self.read(address + offset)
            print(f"{value:02X} ", end="")


class BigEmptyRAM(MemoryBase):
    """Represents a large, empty RAM block (64kB)."""
    def __init__(self):
        super().__init__()
        self.ram = bytearray(2 ** 16)  # 64kB of RAM

    def read(self, address):
        return self.ram[address]

    def read_block(self, address, num_bytes):
        return self.ram[address:address + num_bytes]

    def write(self, address, value):
        self.ram[address] = value


class mNESMappedRAM(MemoryBase):
    """Implements the NES CPU memory map."""
    RAM_SIZE = 0x800  # 2kB of internal RAM
    NUM_PPU_REGISTERS = 8

    RAM_END = 0x0800
    PPU_END = 0x4000
    APU_END = 0x4018
    APU_UNUSED_END = 0x4020
    OAM_DMA = 0x4014
    CONTROLLER1 = 0x4016
    CONTROLLER2 = 0x4017
    CART_START = 0x4020

    def __init__(self, ppu=None, apu=None, cart=None, controller1=None, controller2=None, interrupt_listener=None):
        super().__init__()
        self.ram = bytearray(self.RAM_SIZE)
        self.ppu = ppu
        self.apu = apu
        self.cart = cart
        self.controller1 = controller1
        self.controller2 = controller2
        self.interrupt_listener = interrupt_listener

    def read(self, address):
        """Reads a byte from the NES address space."""
        if address < self.RAM_END:
            return self.ram[address % self.RAM_SIZE]
        elif address < self.PPU_END and self.ppu:
            register_ix = address % self.NUM_PPU_REGISTERS
            return self.ppu.read_register(register_ix)
        elif address == self.CONTROLLER1:
            return (self.controller1.read_bit() & 0b00011111) + (0x40 & 0b11100000)
        elif address == self.CONTROLLER2:
            return (self.controller2.read_bit() & 0b00011111) + (0x40 & 0b11100000)
        elif address >= self.CART_START:
            return self.cart.read(address)
        else:
            return 0

    def write(self, address, value):
        """Writes a byte to the NES address space."""
        if address < self.RAM_END:
            self.ram[address % self.RAM_SIZE] = value
        elif address < self.PPU_END and self.ppu:
            self.ppu.write_register(address % self.NUM_PPU_REGISTERS, value)
        elif address == self.OAM_DMA and self.ppu:
            self.run_oam_dma(value)
        elif address == self.CONTROLLER1:
            self.controller1.set_strobe(value)
            self.controller2.set_strobe(value)

    def run_oam_dma(self, page):
        """Handles OAM DMA transfer."""
        logging.debug(f"OAM DMA from page {page:02X}")
        # Perform DMA transfer
        start_address = page << 8
        data_block = self.read_block(start_address, 256)
        self.ppu.write_oam(data_block)
        self.interrupt_listener.raise_oam_dma_pause()


class NESVRAM(MemoryBase):
    """Implements the NES PPU memory map."""
    PATTERN_TABLE_SIZE_BYTES = 4096
    NAMETABLES_SIZE_BYTES = 2048
    PALETTE_SIZE_BYTES = 32
    NAMETABLE_LENGTH_BYTES = 1024

    NAMETABLE_START = 0x2000
    ATTRIBUTE_TABLE_OFFSET = 0x3C0
    PALETTE_START = 0x3F00

    MIRROR_HORIZONTAL = (0, 0, 1, 1)
    MIRROR_VERTICAL = (0, 1, 0, 1)
    MIRROR_FOUR_SCREEN = (0, 1, 2, 3)

    def __init__(self, cart, nametable_size_bytes=2048):
        super().__init__()
        self.cart = cart
        self._nametables = bytearray(nametable_size_bytes)
        self.palette_ram = bytearray(self.PALETTE_SIZE_BYTES)
        self.nametable_mirror_pattern = cart.nametable_mirror_pattern

    def decode_address(self, address):
        """Decodes the address to the correct memory region."""
        if address < self.NAMETABLE_START:
            return self.cart.chr_mem, address % len(self.cart.chr_mem)
        elif address < self.PALETTE_START:
            page = (address - self.NAMETABLE_START) // self.NAMETABLE_LENGTH_BYTES
            offset = (address - self.NAMETABLE_START) % self.NAMETABLE_LENGTH_BYTES
            true_page = self.nametable_mirror_pattern[page]
            return self._nametables, true_page * self.NAMETABLE_LENGTH_BYTES + offset
        else:
            if address in (0x3F10, 0x3F14, 0x3F18, 0x3F1C):
                address -= 0x10
            return self.palette_ram, address % self.PALETTE_SIZE_BYTES

    def read(self, address):
        """Reads a byte from the NES PPU address space."""
        memory, address_decoded = self.decode_address(address)
        return memory[address_decoded]

    def write(self, address, value):
        """Writes a byte to the NES PPU address space."""
        memory, decoded_address = self.decode_address(address)
        memory[decoded_address] = value
