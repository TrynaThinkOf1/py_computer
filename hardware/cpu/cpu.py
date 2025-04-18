import threading
from typing import Optional

from hardware.ram.ram import RAM
from hardware.nic.nic import NIC
from hardware.serial.serial_io import SerialIO
from hardware.ssd.ssd import SSD
from hardware.gpu.gpu import GPU

class CPU:
    def __init__(self, device_name: str, cores: int, accessible_ram: RAM, accessible_serial_io: SerialIO) -> None:
        """
        Create a new CPU object

        :param device_name:
        :param cores:
        """
        self.device_name = device_name
        self.cores = cores
        self.threads = cores * 2

        self.reg_1 = {}
        self.reg_2 = {}
        self.reg_3 = {}
        self.reg_4 = {}

        self.ram = accessible_ram
        self.serial_io = accessible_serial_io

        self.cycle = 0

        self.instruction_set = {
            0: self.MOV
        }

        self.current_instruction = None

    def cycle(self) -> None:
        self.cycle += 1
        self.get_next_instruction()

    def _count_instruction(self, instruction: str) -> int:
        code = 0

        digits = list(reversed(list(instruction)))

        if digits[0] == "1":
            code += 1
        if digits[1] == "1":
            code += 2
        if digits[2] == "1":
            code += 4
        if digits[3] == "1":
            code += 8

        return code

    def get_next_instruction(self) -> None:
        try:
            self.current_instruction = self.ram.get_instruction(f"0x{self.cycle}")
            self.execute()
        except Exception:
            self.serial_io.output("No more instructions to execute")
            exit(0)

    def execute(self) -> None:
        instructions = self.current_instruction

        for instruction in instructions:
            op = self._count_instruction(instruction)


    def MOV(self, addr: str, reg: Optional[int], immediate: Optional[int]) -> None:
        pass