#import threading
from typing import Any, Optional

class OutOfInstructionsError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidInstructionError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidRegisterError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidAddressError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class RAM:
    def __init__(self):
        self.memory = {}

    def get(self, addr: str) -> Any:
        return self.memory.get(addr)

    def insert(self, val: Any, addr: Optional[str] = None) -> str:
        if addr is None:
            addr = f"0x{len(self.memory) + 1}"
            self.memory[addr] = val
            return addr
        else:
            self.memory[addr] = val
            return addr

    def delete(self, addr: str) -> None:
        del self.memory[addr]

    def dump(self):
        self.memory.clear()



class CPU():
    def __init__(self, ram: RAM) -> None:
        self.ram = ram

        self.reg1 = self.reg2 = self.reg3 = self.reg4 = self.reg5 = self.reg6 = self.reg7 = self.reg8 = self.reg9 = self.reg10 = self.reg11 = self.reg12 = self.reg13 = self.reg14 = self.reg15 = None

        self.regs = [self.reg1, self.reg2, self.reg3, self.reg4, self.reg5,
                     self.reg6, self.reg7, self.reg8, self.reg9, self.reg10,
                     self.reg11, self.reg12, self.reg13, self.reg14, self.reg15]

        self.instruction_set = {
            "1": lambda code=0: self.EXT(code),
            "10": lambda reg, imm=None, addr=None: self.MOV(reg, imm, addr),
            "11": lambda addr: self.DEL(addr),
            "100": lambda val, addr=None: self.INS(val, addr),
            "101": lambda reg: self.OUT(reg)
        }

        self.cycle = 0

        self._cycle()

    def _cycle(self):
        self.cycle += 1
        self._get_next_instruction()

    def _get_next_instruction(self):
        addr = f"0x{self.cycle}"
        self.current_instruction = self.ram.get(addr)
        if self.current_instruction is None:
            error_msg = "Program ran out of instructions"
            raise OutOfInstructionsError(error_msg)
        self.execute()

    def execute(self):
        cur_instr = self.current_instruction
        if cur_instr[0] in self.instruction_set:
            self.instruction_set[cur_instr[0]](*cur_instr[1:])
        else:
            error_msg = f"Invalid instruction on line {self.cycle}"
            raise InvalidInstructionError(error_msg)

    def EXT(self, code: str):
        code = int(code, 2)

        exit(code)

    def MOV(self, reg: str, imm: str, addr: str):
        reg = int(reg, 2)

        regs = self.regs

        if reg < 0 or reg > len(regs):
            error_msg = f"Invalid register assignment on line {self.cycle}"
            raise InvalidRegisterError(error_msg)

        if imm is not None:
            regs[reg] = imm
        else:
            addr = f"0x{int(addr, 2)}"
            num = self.ram.get(addr)
            if num is None:
                error_msg = f"Invalid RAM address on line {self.cycle}"
                raise InvalidAddressError(error_msg)
            regs[reg] = num

        self.regs = regs

        self._cycle()


    def OUT(self, reg: str):
        reg = int(reg, 2)

        if reg < 0 or reg > len(self.regs):
            error_msg = f"Invalid register assignment on line {self.cycle}"
            raise InvalidRegisterError(error_msg)

        print(self.regs[reg])

        self._cycle()