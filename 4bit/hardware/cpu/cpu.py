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
        self.reg_4 = None
        self.reg_5 = None
        self.reg_6 = None
        self.reg_7 = None

        self.regs = [self.reg_0, self.reg_1, self.reg_2, self.reg_3, self.reg_4, self.reg_5, self.reg_6, self.reg_7]

        self.ram = accessible_ram
        self.serial_io = accessible_serial_io

        self.cycle = 0

        self.instruction_set = {
            0: lambda idx1, addr, immediate=None: self.MOV(idx1, addr, immediate),
            1: lambda reg1, reg2, output_reg: self.ADD(reg1, reg2, output_reg),
            2: lambda reg1, reg2, output_reg: self.SUB(reg1, reg2, output_reg),
            3: lambda reg1, reg2, output_reg: self.MUL(reg1, reg2, output_reg),
            4: lambda reg1, reg2, output_reg: self.DIV(reg1, reg2, output_reg),
            5: lambda reg1: self.OUT(reg1),
            15: lambda misc=None, code="0000": self.EXIT(misc, code)
        }

        self.current_instruction = None

        self._cycle()

    def _cycle(self) -> None:
        self.reg_0, self.reg_1, self.reg_2, self.reg_3, self.reg_4, self.reg_5, self.reg_6, self.reg_7 = self.regs
        self.cycle += 1
        self.get_next_instruction()

    def _count_binary_half_byte(self, instruction: str) -> int:
        code = int(instruction, 2)
        return code

    def _verify_regs(self, regs: list[str]) -> bool:
        for reg in regs:
            if reg < 0 or reg > len(self.regs):
                return False, i
        return True, None

    def get_next_instruction(self) -> None:
        try:
            addr = f"0x{self.cycle}"
            self.current_instruction = self.ram.get_instruction(addr)
            if len(self.current_instruction) < 2:
                self._cycle()
        except Exception as e:
            raise Exception("Ran out of instructions!")
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

    def MOV(self, idx1: str, addr: str, immediate: int | None = None) -> None:
        idx1 = self._count_binary_half_byte(idx1)

        regs = self.regs

        if not self._verify_regs([idx1]):
            error_msg = f"Register index out of range: {idx1}"
            raise cpu_errors.InvalidRegisterError(error_msg)

        if immediate is None:
            addr = f"0x{self._count_binary_half_byte(addr)}"

            instr = self.ram.get_instruction(addr)
            regs[idx1] = instr[0]
            print(f"Moved number from address {addr} to register {idx1}")
        else:
            regs[idx1] = immediate
            print(f"Moved immediate {immediate} to register {idx1}")

        self.regs = regs # this unpacking makes all the values fall into place

        self._cycle()

    def ADD(self, idx1: str, idx2: str, idxo: str) -> None:
        idx1 = self._count_binary_half_byte(idx1)
        idx2 = self._count_binary_half_byte(idx2)
        idxo = self._count_binary_half_byte(idxo)

        regs = self.regs

        my_regs = [idx1, idx2, idxo]
        i = self._verify_regs(my_regs)
        if not i[0]:
            error_msg = f"Register index out of range: {my_regs[i[1]]}"
            raise cpu_errors.InvalidRegisterError(error_msg)

        num1 = self._count_binary_half_byte(regs[idx1])
        num2 = self._count_binary_half_byte(regs[idx2])

        op = str(bin(num1 + num2))[2:]
        regs[idxo] = op

        print(f"Added {num1} to {num2} and sent to register {idxo}")

        self.regs = regs

        self._cycle()

    def SUB(self, idx1: str, idx2: str, idxo: str) -> None:
        idx1 = self._count_binary_half_byte(idx1)
        idx2 = self._count_binary_half_byte(idx2)
        idxo = self._count_binary_half_byte(idxo)

        regs = self.regs

        my_regs = [idx1, idx2, idxo]
        i = self._verify_regs(my_regs)
        if not i[0]:
            error_msg = f"Register index out of range: {my_regs[i[1]]}"
            raise cpu_errors.InvalidRegisterError(error_msg)

        num1 = self._count_binary_half_byte(regs[idx1])
        num2 = self._count_binary_half_byte(regs[idx2])

        op = str(bin(num1 - num2))[2:]
        regs[idxo] = op

        print(f"Subtracted {num2} from {num1} and sent to register {idxo}")

        self.regs = regs

        self._cycle()

    def MUL(self, idx1: str, idx2: str, idxo: str) -> None:
        idx1 = self._count_binary_half_byte(idx1)
        idx2 = self._count_binary_half_byte(idx2)
        idxo = self._count_binary_half_byte(idxo)

        regs = self.regs

        my_regs = [idx1, idx2, idxo]
        i = self._verify_regs(my_regs)
        if not i[0]:
            error_msg = f"Register index out of range: {my_regs[i[1]]}"
            raise cpu_errors.InvalidRegisterError(error_msg)

        num1 = self._count_binary_half_byte(regs[idx1])
        num2 = self._count_binary_half_byte(regs[idx2])

        op = str(bin(num1 * num2))[2:]
        regs[idxo] = op

        print(f"Multiplied {num2} by {num1} and sent to register {idxo}")

        self.regs = regs

        self._cycle()

    def DIV(self, idx1: str, idx2: str, idxo: str) -> None:
        idx1 = self._count_binary_half_byte(idx1)
        idx2 = self._count_binary_half_byte(idx2)
        idxo = self._count_binary_half_byte(idxo)

        regs = self.regs

        my_regs = [idx1, idx2, idxo]
        i = self._verify_regs(my_regs)
        if not i[0]:
            error_msg = f"Register index out of range: {my_regs[i[1]]}"
            raise cpu_errors.InvalidRegisterError(error_msg)

        num1 = self._count_binary_half_byte(regs[idx1])
        num2 = self._count_binary_half_byte(regs[idx2])

        op = str(bin(int(num1 / num2)))[2:]
        regs[idxo] = op

        print(f"Divided {num1} by {num2} and sent to register {idxo}")

        self.regs = regs

        self._cycle()

    def OUT(self, idxo: str) -> None:
        idxo = self._count_binary_half_byte(idxo)

        if not self._verify_regs([idxo]):
            error_msg = f"Register index out of range: {idxo}"
            raise cpu_errors.InvalidRegisterError(error_msg)

        num = self.regs[idxo]
        if num is not None:
            self.serial_io.output(self.serial_io, str(int(num, 2)))

            print(f"Outputted the number in register {idxo}")
        else:
            self.serial_io.output(self.serial_io, None)

        self._cycle()

    def EXIT(self, misc: str, code: str) -> None:
        code = self._count_binary_half_byte(code)

        print(f"Exiting exectuing with code: {code}")

        exit(code)