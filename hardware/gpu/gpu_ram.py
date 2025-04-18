from sys import getsizeof as sizeof

import hardware.ram.ram_errors

class GPU_RAM:
    def __init__(self, stick_name: str, stick_num: int, max_mem_size: int = 1000000) -> None:
        """
        Create a 'GPU-RAM Stick' object that stores memory in key-valie pairs

        :param stick_name: what this piece of memory is called
        :param stick_num: which stick of GPU-RAM in the array is this
        :param max_mem_size: how many bytes this object can store, default is 1000000 bytes or 1MB
        """
        self.device_name: str = stick_name
        self.stick_num: int = stick_num
        self.max_mem_size: int = max_mem_size

        self.memory = {}
        self.current_size = sizeof(self.memory)

        if self.current_size > self.max_mem_size:
            error_msg = f"Cannot create GPU-RAM Stick {self.device_name} because it does not have enough memory"
            del self
            raise ram_errors.OutOfMemoryError(error_msg)

    def __str__(self):
        return f"GPU-RAM Stick: {self.device_name}, Size: {self.current_size} bytes, Max Size: {self.max_mem_size} bytes"

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return self.current_size < self.max_mem_size

    def add_instruction(self, instructions: list[int]) -> str:
        """
        Add instructions to GPU-RAM

        FOR ALL OPCODES - LOOK IN ../opcodes.txt

        instructions should be a list of instances of 4 binary digits per instruction

        :param instructions: a list of bytes that are machine code instructions
        :return: the address of the added instruction
        """
        addr = f"{self.stick_num}x{len(self.memory) + 1}"
        self.memory[addr] = instructions

        self.current_size = sizeof(self.memory)
        if self.current_size > self.max_mem_size:
            error_msg = f"Cannot add instruction {instruction} to GPU-RAM because it exceeds GPU-RAM size"
            del self.memory[addr]
            raise ram_errors.OutOfMemoryError(error_msg)

        return addr

    def get_instruction(self, addr: int) -> list[int]:
        """
        Get an instruction from GPU-RAM
        Deletes the instructions as soon as its gotten

        :param addr: the address of the instruction
        :return: the instruction stored at the address
        """
        instruction = self.memory.get(addr)
        if instruction is None:
            error_msg = f"Cannot get instruction from address {addr} because it does not exist"
            raise ram_errors.MemoryNotFoundError(error_msg)

        del self.memory[addr]

        return instruction