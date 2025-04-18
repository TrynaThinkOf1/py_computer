import threading
from typing import Optional

from hardware.ram.ram import RAM
from hardware.nic.nic import NIC
from hardware.serial.serial_io import SerialIO
from hardware.ssd.ssd import SSD
from hardware.gpu.gpu import GPU

import hardware.cpu.cpu_errors as cpu_errors

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

        self.reg_0 = None
        self.reg_1 = None
        self.reg_2 = None
        self.reg_3 = None

        self.ram = accessible_ram
        self.serial_io = accessible_serial_io

        self.cycle = 0

        self.instruction_set = {
            0: lambda idx1, addr: self.MOV(idx1, addr),
            1: lambda reg1, reg2, output_reg: self.ADD(reg1, reg2, output_reg),
            2: lambda reg1, reg2, output_reg: self.SUB(reg1, reg2, output_reg),
            3: lambda reg1, reg2, output_reg: self.MUL(reg1, reg2, output_reg),
            4: lambda reg1, reg2, output_reg: self.DIV(reg1, reg2, output_reg),
            5: lambda reg1: self.PRINT(reg1)
        }

        self.current_instruction = None

        self._cycle()

    def _cycle(self) -> None:
        self.cycle += 1
        self.get_next_instruction()

    def _count_binary_half_byte(self, instruction: str) -> int:
        code = 0

        digits = list(reversed(list(instruction)))

        for i in range(len(digits)):
            if digits[i] == "1":
                match i:
                    case 0:
                        code += 1
                    case 1:
                        code += 2
                    case 2:
                        code += 4
                    case 3:
                        code += 8
                    case 4:
                        code += 16
                    case 5:
                        code += 32
                    case 6:
                        code += 64
                    case 7:
                        code += 128

        return code

    def get_next_instruction(self) -> None:
        try:
            addr = f"0x{self.cycle}"
            self.current_instruction = self.ram.get_instruction(addr)
            if len(self.current_instruction) < 3:
                self._cycle()
        except Exception as e:
            self.serial_io.output(self.serial_io, "No more instructions to execute")
            print(f"Register 0: {self.reg_0}")
            print(f"Register 1: {self.reg_1}")
            print(f"Register 2: {self.reg_2}")
            print(f"Register 3: {self.reg_3}")
            exit(0)
        self.execute()

    def execute(self) -> None:
        instructions = self.current_instruction

        op = self._count_binary_half_byte(instructions[0])

        if op in self.instruction_set:
            self.instruction_set[op](*instructions[1:])
            self._cycle()
        else:
            error_msg = f"The instruction {instructions[0]} is not a valid operation"
            raise cpu_errors.InvalidInstructionError(error_msg)

    def MOV(self, idx1: str, addr: str) -> None:
        idx1 = self._count_binary_half_byte(idx1)
        addr = f"0x{self._count_binary_half_byte(addr)}"

        regs = [self.reg_0, self.reg_1, self.reg_2, self.reg_3]

        if idx1 < 0 or idx1 > len(regs):
            error_msg = f"Register index out of range: {idx1}"
            raise cpu_errors.InvalidRegisterError(error_msg)

        instr = self.ram.get_instruction(addr)
        regs[idx1] = instr[0]

        self.reg_0, self.reg_1, self.reg_2, self.reg_3 = regs # this unpacking makes all the values fall into place

        self._cycle()

    def ADD(self, idx1: str, idx2: str, idxo: str) -> None:
        idx1 = self._count_binary_half_byte(idx1)
        idx2 = self._count_binary_half_byte(idx2)
        idxo = self._count_binary_half_byte(idxo)

        regs = [self.reg_0, self.reg_1, self.reg_2, self.reg_3]

        if idx1 < 0 or idx1 > len(regs):
            error_msg = f"Register index out of range: {idx1}"
            raise cpu_errors.InvalidRegisterError(error_msg)
        if idx2 < 0 or idx2 > len(regs):
            error_msg = f"Register index out of range: {idx2}"
            raise cpu_errors.InvalidRegisterError(error_msg)
        if idxo < 0 or idxo > len(regs):
            error_msg = f"Register index out of range: {idxo}"
            raise cpu_errors.InvalidRegisterError(error_msg)

        num1 = self._count_binary_half_byte(regs[idx1])
        num2 = self._count_binary_half_byte(regs[idx2])

        op = str(bin(num1 + num2)).removeprefix("0b")
        regs[idxo] = op

        self.reg_0, self.reg_1, self.reg_2, self.reg_3 = regs

        self._cycle()