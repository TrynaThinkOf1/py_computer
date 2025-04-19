from _linker import link

class SyntaxError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

def _get_tokens(lines: list[str]) -> list[list[str]]:
    unproc_token_sets = []
    proc_token_sets = []
    for line in lines:
        if "\\t" in line and "    " in line:
            # make sure that they user EITHER tabs OR spaces for each line, but one line can use tabs while another uses spaces
            error_msg = f"Inconsistent use of tabs and spaces: [{line}] @ [line no.]: {lines.index(line) + 1}"
            raise SyntaxError(error_msg)
        elif "    " in line:
            if not line.startswith("#"): # filter out full-line comments
                unproc_token_sets.append(line.removesuffix("\n").split("    "))
        elif "\\t" in line:
            if not line.startswith("#"):
                unproc_token_sets.append(line.removesuffix("\n").split("\\t"))

    for i in range(len(unproc_token_sets)):
        proc_token_sets.append([])
        for j in range(len(unproc_token_sets[i])):
            if not unproc_token_sets[i][j].startswith("#"): # filter out after-code comments
                proc_token_sets[i].append(unproc_token_sets[i][j])

    return proc_token_sets

def _create_machine_code_instructions(token_set: list[list[str]]) -> list[list[str]]:
    machine_code_instructions = []

    instruction_set = {
        "EXT": "1", # 1
        "MOV": "10", # 2
        "DEL": "11", # 3
        "INS": "100", # 4
        # skip 5 because thats PTR
        "OUT": "110", # 6
    }

    convert_imm = lambda imm: bin(int(imm.removeprefix("$")))[2:]
    convert_reg = lambda reg: bin(int(reg.removeprefix("reg")))[2:]
    convert_addr = lambda addr: bin(int(addr.removeprefix("0x")))[2:]

    for tokens in token_set:
        machine_code_instructions.append([])
        for token in tokens:
            if token in instruction_set:
                machine_code_instructions[-1].append(instruction_set[token])
                continue

            if token.startswith("reg"):
                machine_code_instructions[-1].append(convert_reg(token))
                continue

            if token.startswith("*"):
                reg = convert_reg(token[1:]) # remove the *
                machine_code_instructions[-1].append(None) # so that there is no imm
                machine_code_instructions[-1].append(["101", reg])

            if token.startswith("0x"):
                machine_code_instructions[-1].append(convert_addr(token))
                continue

            if token.startswith("$"):
                machine_code_instructions[-1].append(convert_imm(token))
                continue

    return machine_code_instructions

def compile(filename: str):
    with open(filename, "r") as f:
        lines = f.readlines()

    token_sets = _get_tokens(lines)
    print(token_sets)

    machine_code_instructions = _create_machine_code_instructions(token_sets)
    print(machine_code_instructions)

    link(machine_code_instructions, f"{filename.split(".")[0]}.py")

    print(f"Compiled into object: {filename}.py\nTo execute, run \"python {filename}.py\"")

if __name__ == "__main__":
    #from sys import argv
    filename = "calculator_2.zev" # argv[1]
    compile(filename)