from sys import getsizeof as sizeof

import ram_errors

class RAM:
    def __init__(self, stick_name: str, max_mem_size: int = 1000000) -> None:
        """
        Create a 'RAM-Stick' object that stores memory in key-valie pairs

        :param stick_name: what this piece of memory is called
        :param max_mem_size: how many bytes this object can store, default is 1000000 bytes or 1MB
        """
        self.device_name: str = stick_name
        self.max_mem_size: int = max_mem_size

        self.memory = {}
        self.current_size = sizeof(self.memory)
        
        if self.current_size > self.max_mem_size:
            error_msg = f"Cannot create RAM Stick {self.device_name} because it does not have enough memory"
            del self
            raise ram_errors.OutOfMemoryError(error_msg)

    def __str__(self):
        return f"RAM Stick: {self.device_name}, Size: {self.current_size} bytes, Max Size: {self.max_mem_size} bytes"
    def __repr__(self):
        return self.__str__()
    def __bool__(self):
        return self.current_size < self.max_mem_size

    def add_instruction(self, instructions: list[int]) -> str:
        """
        Add instructions to RAM

        :param instructions: a list of bytes that are machine code instructions
        :return: the address of the added instruction
        """
        for instruction in instructions:
            if len(instruction) != 8:
                error_msg = f"Cannot add instruction {instruction} to RAM because it is an invalid byte"
                raise ram_errors.InvalidMemoryError(error_msg)

        addr = f"0x{len(self.memory) + 1}"
        self.memory[addr] = instructions

        self.current_size = sizeof(self.memory)
        if self.current_size > self.max_mem_size:
            error_msg = f"Cannot add instruction {instruction} to RAM because it exceeds RAM size"
            del self.memory[addr]
            raise ram_errors.OutOfMemoryError(error_msg)
        
        return addr
        
    def get_instruction(self, addr: int) -> list[int]:
        """
        Get an instruction from RAM
        
        :param addr: the address of the instruction
        :return: the instruction stored at the address
        """
        instruction = self.memory.get(addr)
        if instruction is None:
            error_msg = f"Cannot get instruction from address {addr} because it does not exist"
            raise ram_errors.MemoryNotFoundError(error_msg)
        return instruction

if __name__ == "__main__":
    stick1 = RAM(stick_name="stick1", max_mem_size=16000000000)
    stick1.add_instruction([])