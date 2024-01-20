import pickle
import logging
import pygame

from mos6502 import MOS6502
from memory import mNESMappedRAM
from ppu import MarioPPU
from rom import ROM
from utils import Screen, KeyboardController, ControllerBase

import pyximport; pyximport.install()


class NES:
    """Represents the NES system, combining all components and their interlinks."""
    PPU_CYCLES_PER_CPU_CYCLE = 3
    FRAMERATE_FPS = 480

    def __init__(self, rom_file, screen_scale=3, log_file=None, log_level=None, prg_start=None):
        """Initializes the NES system with ROM data and hardware components."""
        self.setup_logging(log_file, log_level)
        rom = ROM(rom_file, py_compatibility_mode=True)
        self.cart = rom.get_cart(prg_start)

        self.controller1 = KeyboardController()
        self.controller2 = ControllerBase(active=False)

        self.interrupt_listener = Interrupter()
        self.ppu = MarioPPU(cart=self.cart, interrupt_listener=self.interrupt_listener)

        self.screen = Screen(ppu=self.ppu, scale=screen_scale, py_compatibility_mode=True)
        self.ppu.screen = self.screen
        self.screen_scale = screen_scale

        self.memory = NESMappedRAM(ppu=self.ppu,
                                   apu=None,
                                   cart=self.cart,
                                   controller1=self.controller1,
                                   controller2=self.controller2,
                                   interrupt_listener=self.interrupt_listener
                                   )

        self.cpu = MOS6502(memory=self.memory, undocumented_support_level=2, stack_underflow_causes_exception=False)
        self.cpu.reset()

    def setup_logging(self, log_file, log_level):
        """Configures logging for the NES emulator."""
        if log_file is None or log_level is None:
            logging.disable()
            return

        logging.addLevelName(LOG_MEMORY, "MEMORY")
        logging.addLevelName(LOG_PPU, "PPU")
        logging.addLevelName(LOG_CPU, "CPU")

        logging.basicConfig(filename=log_file, level=logging.NOTSET, format='%(asctime)-15s %(source)-5s %(message)s', filemode='w')
        logging.root.setLevel(log_level)

    def __getstate__(self):
        return self.memory.__getstate__()

    def __setstate__(self, state):
        self.cart, self.controller1, self.controller2, self.interrupt_listener, self.cpu, self.memory, self.screen_scale = state
        self.screen = Screen(scale=self.screen_scale)

    def save(self):
        with open("test.p", "wb") as f:
            pickle.dump(self, f, protocol=4)

    @staticmethod
    def load(file):
        with open(file, "rb") as f:
            nes = pickle.load(f)
        nes.screen._special_init()
        return nes

    def step(self):
        """Runs one instruction on the CPU and the corresponding cycles on the PPU."""
        if self.interrupt_listener.any_active():
            if self.interrupt_listener.nmi_active:
                cpu_cycles = self.cpu.trigger_nmi()
                self.interrupt_listener.reset_nmi()
            elif self.interrupt_listener.irq_active:
                raise NotImplementedError("IRQ is not implemented")
            elif self.interrupt_listener.oam_dma_pause:
                cpu_cycles = self.cpu.oam_dma_pause()
                self.interrupt_listener.reset_oam_dma_pause()
        else:
            cpu_cycles = self.cpu.run_next_instr()

        return self.ppu.run_cycles(cpu_cycles * self.PPU_CYCLES_PER_CPU_CYCLE)

    def run(self):
        """Runs the NES indefinitely, handling frame timing and exit signals."""
        pygame.init()
        clock = pygame.time.Clock()

        show_hud = True

        while True:
            vblank_started = False
            while not vblank_started:
                vblank_started = self.step()

            self.controller1.update()
            self.controller2.update()

            fps = clock.get_fps()
            if show_hud:
                self.screen.add_text(f"{fps:.0f} fps", (10, 10), (0, 255, 0) if fps > 55 else (255, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        show_hud = not show_hud
                    if event.key == pygame.K_0:
                        self.save()
                        self.screen.add_text("saved", (100, 10), (255, 128, 0))

            self.screen.show()
            clock.tick(self.FRAMERATE_FPS)


class Interrupter:
    """Handles interrupts for the emulator."""
    def __init__(self):
        self._nmi = False
        self._irq = False
        self.oam_dma_pause = False

    def raise_nmi(self):
        self._nmi = True

    def reset_nmi(self):
        self._nmi = False

    def reset_oam_dma_pause(self):
        self.oam_dma_pause = False

    def raise_oam_dma_pause(self):
        self.oam_dma_pause = True

    def any_active(self):
        return self._nmi or self._irq or self.oam_dma_pause

    @property
    def nmi_active(self):
        return self._nmi

    @property
    def irq_active(self):
        return self._irq


pynes = NES("/mnt/e/nes-main/nes-main/Super_mario_brothers.nes")
pynes.run()
