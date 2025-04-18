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

        self.reg_0 = None
        self.reg_1 = None
        self.reg_2 = None
        self.reg_3 = None

        self.ram = accessible_ram
        self.serial_io = accessible_serial_io

        self.cycle = 0

        self.instruction_set = {
            0: lambda addr, reg: self.MOV(addr, reg),
            1: lambda reg1, reg2, output_reg: self.ADD(reg1, reg2, output_reg),
        }

        self.current_instruction = None

        self._cycle()

    def _cycle(self) -> None:
        self.cycle += 1
        print(f"Reg 0: {self.reg_0}")
        print(f"Reg 1: {self.reg_1}")
        print(f"Reg 2: {self.reg_2}")
        print(f"Reg 3: {self.reg_3}")
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
                print("Not an instruction")
                self._cycle()
        except Exception as e:
            self.serial_io.output(self.serial_io, "No more instructions to execute")
            exit(0)
        self.execute()

    def execute(self) -> None:
        instructions = self.current_instruction
        print(f"Executing instruction {instructions}")

        op = self._count_binary_half_byte(instructions[0])
        print(f"Opcode: {op}")

        if op in self.instruction_set:
            print(self.instruction_set[op])
            self.instruction_set[op](*instructions[1:])
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
                self.reg_0 = instr[0]
            case 1:
                instr = self.ram.get_instruction(addr)
                self.reg_1 = instr[0]
            case 2:
                instr = self.ram.get_instruction(addr)
                self.reg_2 = instr[0]
            case 3:
                instr = self.ram.get_instruction(addr)
                self.reg_3 = instr[0]
            case _:
                error_msg = f"There is no register {reg}"
                raise cpu_errors.InvalidRegisterError(error_msg)

        self._cycle()

    def ADD(self, which_reg1: str, which_reg2: str, output_reg: str) -> None:
        which_reg1 = self._count_binary_half_byte(which_reg1)
        which_reg2 = self._count_binary_half_byte(which_reg2)
        output_reg = self._count_binary_half_byte(output_reg)
        print(f"Adding register {which_reg1} to register {which_reg2} and sending to register {output_reg}")

        match which_reg1:
            case 0:
                num1 = self._count_binary_half_byte(self.reg_0)
            case 1:
                num1 = self._count_binary_half_byte(self.reg_1)
            case 2:
                num1 = self._count_binary_half_byte(self.reg_2)
            case 3:
                num1 = self._count_binary_half_byte(self.reg_3)
            case _:
                error_msg = f"There is no register {which_reg1}"
                raise cpu_errors.InvalidRegisterError(error_msg)

        match which_reg2:
            case 0:
                num2 = self._count_binary_half_byte(self.reg_0)
            case 1:
                num2 = self._count_binary_half_byte(self.reg_1)
            case 2:
                num2 = self._count_binary_half_byte(self.reg_2)
            case 3:
                num2 = self._count_binary_half_byte(self.reg_3)
            case _:
                error_msg = f"There is no register {which_reg2}"
                raise cpu_errors.InvalidRegisterError(error_msg)

        op = str(bin(num1 + num2)).removeprefix("0b")

        match output_reg:
            case 0:
                self.reg_0 = op
            case 1:
                self.reg_1 = op
            case 2:
                self.reg_2 = op
            case 3:
                self.reg_3 = op
            case _:
                error_msg = f"There is no register {output_reg}"
                raise cpu_errors.InvalidRegisterError(error_msg)

if __name__ == "__main__":
    stick = RAM("stick1", 0, 1024)
    stick.add_instruction(["0000", "0000", "0100"]) # move the number from address 0x4 to register 0
    stick.add_instruction(["0000", "0001", "0101"]) # move the number from address 0x5 to register 1
    stick.add_instruction(["0001", "0000", "0001", "0010"]) # put the sum of reg 0 and reg 1 into reg 2
    stick.add_instruction(["0111"]) # add the number 7 to address 0x4
    stick.add_instruction(["0011"]) # add the number 3 to address 0x5

    serial = SerialIO

    cpu = CPU("ryzen", 6, stick, serial)
    print(cpu.reg_2)