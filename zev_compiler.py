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

def compile(filename: str):
    lines = read_file(filename)
    instructions = parse_into_instructions(lines)

    stick = RAM("stick", 0, 1000000000)  # 1GB of RAM
    serial = SerialIO

    for instruction in instructions:
        stick.add_instruction(instruction)

    CPU("zev compiler", 6, stick, serial)

if __name__ == "__main__":
    filename = "./test1.zev" # argv[1] will be the production assignment
    compile(filename)