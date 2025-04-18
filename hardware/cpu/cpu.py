import threading
from typing import Optional

from hardware.ram.ram import RAM
from hardware.nic.nic import NIC
from hardware.serial.serial_io import SerialIO
from hardware.ssd.ssd import SSD
from hardware.gpu.gpu import GPU

import cpu_errors

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

        self.reg_0 = {}
        self.reg_1 = {}
        self.reg_2 = {}
        self.reg_3 = {}

        self.ram = accessible_ram
        self.serial_io = accessible_serial_io

        self.cycle = 0

        self.instruction_set = {
            0: lambda addr, reg: self.MOV(addr, reg)
        }

        self.current_instruction = None

        self._cycle()

    def _cycle(self) -> None:
        self.cycle += 1
        self.get_next_instruction()

    def _count_binary_half_byte(self, instruction: str) -> int:
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
            addr = f"0x{self.cycle}"
            self.current_instruction = self.ram.get_instruction(addr)
            self.execute()
        except Exception as e:
            self.serial_io.output(self.serial_io, "No more instructions to execute")
            #exit(0)

    def execute(self) -> None:
        instructions = self.current_instruction

        op = self._count_binary_half_byte(instructions[0])

        if op in self.instruction_set:
            self.instruction_set[op](instructions[1], instructions[2])
            self._cycle()
        else:
            error_msg = f"The instruction {instructions[0]} is not a valid operation"
            raise cpu_errors.InvalidInstructionError(error_msg)

    def MOV(self, reg: str, addr: str) -> None:
        reg = self._count_binary_half_byte(reg)
        addr = f"0x{self._count_binary_half_byte(addr)}"
        match reg:
            case 0:
                instr = self.ram.get_instruction(addr)
                self.reg_0[addr] = instr
            case 1:
                instr = self.ram.get_instruction(addr)
                self.reg_1[addr] = instr
            case 2:
                instr = self.ram.get_instruction(addr)
                self.reg_2[addr] = instr
            case 3:
                instr = self.ram.get_instruction(addr)
                self.reg_3[addr] = instr
            case _:
                error_msg = f"There is no register {reg}"
                raise cpu_errors.InvalidRegisterError(error_msg)


if __name__ == "__main__":
    stick = RAM("stick1", 0, 1024)
    stick.add_instruction(["0000", "0011", "0010"]) # this will move the number from address 0x2 to register 2
    stick.add_instruction(["1111"]) # this will add the number 15 to address 0x2

    #print(stick.get_instruction("0x1"))
    #print(stick.get_instruction("0x2"))

    serial = SerialIO

    cpu = CPU("ryzen", 6, stick, serial)
    print(cpu.reg_3)