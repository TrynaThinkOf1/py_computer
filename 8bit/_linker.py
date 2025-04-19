def link(machine_code: list[list[str]], filename: str) -> None:
    with open("./zvm.py", "r") as zvm:
        lines = zvm.readlines()

    lines.append("if __name__ == \"__main__\":\n")
    lines.append("    ram = RAM()\n")
    for instr in machine_code:
        lines.append(f"    ram.insert(val={instr})\n")

    with open(filename, "w") as test:
        test.writelines(lines)
