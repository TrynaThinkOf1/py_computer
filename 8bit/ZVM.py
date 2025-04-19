#import threading
from typing import Any, Optional

class OutOfInstructionsError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class RAM:
    def __init__(self):
        self.memory = {}

    def get_from_addr(self, addr: str) -> Any:
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
            "1": lambda code: self.EXT(code),
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
            raise OutOfInstructionsError("Program ran out of instructions")
        self.execute()

    def execute(self):
        cur_instr = self.current_instruction
        if cur_instr in self.instruction_set:
            self.instruction_set[cur_instr[0]](*cur_instr[1:])
