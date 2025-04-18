from sys import argv

from hardware.cpu.cpu import CPU
from hardware.ram.ram import RAM
from hardware.serial.serial_io import SerialIO

def read_file(filename: str) -> list:
    with open(filename, "r") as file:
        return file.readlines()

def parse_into_instructions(lines: list) -> list[list[str]]:
    tokens = []
    for line in lines:
        if line.startswith("#") or line.startswith("\n"):
            continue
        else:
            tokens.append(line.strip())

    instructions = []

    for token in tokens:
        instructions.append(token.split("    "))

    return instructions

def create_half_byte_instructions(instructions: list[list[str]]) -> list[list[str]]:
    instr_set = {
        "MOV": "0000",
        "ADD": "0001",
        "SUB": "0010",
        "MUL": "0011",
        "DIV": "0100",
        "OUT": "0101"
    }
    
    half_byte_instructions = []
    length = 4

    for i in range(len(instructions)):
        print(instructions[i])
        half_byte_instructions.append([])
        for j in range(len(instructions[i])):
            current_instruction = instructions[i][j]

            if current_instruction.startswith("#"):
                continue
            elif current_instruction in instr_set:
                half_byte = instr_set[current_instruction]
                half_byte_instructions[i].append(half_byte)
            elif current_instruction.startswith("%"): # immediate
                half_byte = format(int(current_instruction.removeprefix("%")), f'0{length}b')
                print(half_byte)
                half_byte_instructions[i].append("0000") # add in a RAM value that doesn't exist as a failsafe
                half_byte_instructions[i].append(half_byte)
            elif current_instruction.startswith("idx"): # register
                half_byte = format(int(current_instruction.removeprefix("idx")), f'0{length}b')
                half_byte_instructions[i].append(half_byte)
            elif current_instruction.startswith("0x"): # RAM address
                half_byte = format(int(current_instruction.removeprefix("0x")), f'0{length}b')
                half_byte_instructions[i].append(half_byte)

    return half_byte_instructions

def compile(filename: str):
    lines = read_file(filename)
    instructions = parse_into_instructions(lines)
    half_byte_instructions = create_half_byte_instructions(instructions)
    print(half_byte_instructions)

    stick = RAM("stick", 0, 1000000000)  # 1GB of RAM
    serial = SerialIO

    for instruction in half_byte_instructions:
        stick.add_instruction(instruction)

    CPU("zev compiler", 6, stick, serial)

if __name__ == "__main__":
    filename = "./test1.zev" # argv[1] will be the production assignment
    compile(filename)