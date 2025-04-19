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

    def insert(self, val: Any) -> str:
        addr = f"0x{len(self.memory) + 1}"
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
            "10": lambda sto_reg, imm=None, addr=None: self.MOV(sto_reg, imm, addr),
            "11": lambda this_will_be_none_bc_pointer_stuff, addr: self.DEL(addr),
            "100": lambda val_reg, sto_reg: self.INS(val_reg, sto_reg),
            # skip 5 because thats PTR
            "110": lambda reg: self.OUT(reg)
        }

        self.cycle = 0

        self._cycle()

    def _add_two_binary(self, n1: str, n2: str) -> str:
        maxlen = max(len(n1), len(n2))
        n1 = n1.zfill(maxlen)
        n2 = n2.zfill(maxlen)

        added = []
        carry = 0
        for i in range(maxlen - 1, -1, -1):
            total = int(n1[i]) + int(n2[i]) + carry
            added.append(str(total % 2))
            carry = total // 2

        if carry:
            added.append("1")


        return "".join(reversed(added)).lstrip("0") or "0"

    def _sub_two_binary(self, n1: str, n2: str) -> str:
        # 0) Helper to compare magnitudes
        def is_smaller(a: str, b: str) -> bool:
            a = a.lstrip('0') or '0'
            b = b.lstrip('0') or '0'
            if len(a) != len(b):
                return len(a) < len(b)
            return a < b

        # 1) Handle negativity by swapping if needed
        negative = False
        if is_smaller(n1, n2):
            n1, n2 = n2, n1
            negative = True

        # 2) Pad to equal length
        maxlen = max(len(n1), len(n2))
        n1 = n1.zfill(maxlen)
        n2 = n2.zfill(maxlen)

        result = []
        borrow = 0

        # 3) Subtract bit-by-bit, LSB→MSB
        for i in range(maxlen - 1, -1, -1):
            b1 = int(n1[i])
            b2 = int(n2[i])
            diff = b1 - (b2 + borrow)
            if diff < 0:
                diff += 2
                borrow = 1
            else:
                borrow = 0
            result.append(str(diff))

        # 4) Assemble, strip leading zeros, handle zero result
        res_str = ''.join(reversed(result)).lstrip('0') or '0'
        return ('-' + res_str) if negative else res_str

    def _validate_regs(self, regs: list):
        for i in range(len(regs)):
            if regs[i] < 0 or regs[i] > len(self.regs):
                error_msg = f"Invalid register assignment on line {self.cycle}"
                raise InvalidRegisterError(error_msg)

    def _cycle(self):
        self.cycle += 1
        self._get_next_instruction()

    def _get_next_instruction(self):
        addr = f"0x{self.cycle}"
        self.current_instruction = self.ram.get(addr=addr)
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

    def MOV(self, sto_reg: str, imm: str, addr: str | list):
        sto_reg = int(sto_reg, 2)

        regs = self.regs

        self._validate_regs([sto_reg])

        if imm is not None:
            regs[sto_reg] = imm
        else:
            ptr_reg = int(addr[1], 2)

            if ptr_reg < 0 or ptr_reg > len(regs):
                error_msg = f"Invalid register assignment on line {self.cycle}"
                raise InvalidRegisterError(error_msg)

            addr = regs[ptr_reg]
            num = self.ram.get(addr)
            if num is None:
                error_msg = f"Invalid RAM address on line {self.cycle}"
                raise InvalidAddressError(error_msg)
            regs[sto_reg] = num

        self.regs = regs

        self._cycle()

    def DEL(self, addr: list):
        reg = int(addr[1], 2)

        self._validate_regs([reg])

        addr = self.regs[reg]

        self.ram.delete(addr=addr)

        self._cycle()

    def INS(self, val_reg: str, sto_reg: str) -> str:
        val_reg = int(val_reg, 2)
        sto_reg = int(sto_reg, 2)

        regs = self.regs

        self._validate_regs([val_reg, sto_reg])

        val = regs[val_reg]

        addr = self.ram.insert(val=val)
        regs[sto_reg] = addr

        self.regs = regs

        self._cycle()


    def OUT(self, reg: str):
        reg = int(reg, 2)

        self._validate_regs([reg])

        print(self.regs[reg])

        self._cycle()

    def ADD(self, first_reg: str, second_reg: str, sto_reg: str):
        first_reg = int(first_reg, 2)
        second_reg = int(second_reg, 2)
        sto_reg = int(sto_reg, 2)

        regs = self.regs

        self._validate_regs([first_reg, second_reg, sto_reg])

        num1 = regs[first_reg]
        num2 = regs[second_reg]

        if num1 is None:
            error_msg = f"Empty register assignment on line {self.cycle}"
            raise InvalidRegisterError(error_msg)
        if num2 is None:
            error_msg = f"Empty register assignment on line {self.cycle}"
            raise InvalidRegisterError(error_msg)

        result = self._add_two_binary(num1, num2)
        regs[sto_reg] = result

        self.regs = regs

        self._cycle()

    def SUB(self, first_reg: str, second_reg: str, sto_reg: str):
        first_reg = int(first_reg, 2)
        second_reg = int(second_reg, 2)
        sto_reg = int(sto_reg, 2)

        regs = self.regs

        self._validate_regs([first_reg, second_reg, sto_reg])

        num1 = regs[first_reg]
        num2 = regs[second_reg]

        if num1 is None:
            error_msg = f"Empty register assignment on line {self.cycle}"
            raise InvalidRegisterError(error_msg)
        if num2 is None:
            error_msg = f"Empty register assignment on line {self.cycle}"
            raise InvalidRegisterError(error_msg)

        result = self._sub_two_binary(num1, num2)
        regs[sto_reg] = result

        self.regs = regs

        self._cycle()