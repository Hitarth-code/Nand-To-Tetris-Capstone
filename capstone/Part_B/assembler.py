#!/usr/bin/env python3
"""
Hack Assembler
Nand to Tetris Capstone Project
Personal Number K = 30 (K % 3 == 0)
Extra Feature: Exports all labels and variables with addresses to symbols.txt
"""

import sys
import os

# Predefined symbols mapping
PREDEFINED_SYMBOLS = {
    "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7,
    "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576
}

# Computation bit patterns (7 bits: a + c1..c6)
COMP_TABLE = {
    # a = 0
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "A+D": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "A&D": "0000000",
    "D|A": "0010101",
    "A|D": "0010101",
    # a = 1
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "M+D": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "M&D": "1000000",
    "D|M": "1010101",
    "M|D": "1010101",
}

# Destination bit patterns (3 bits: d1..d3)
DEST_TABLE = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

# Jump bit patterns (3 bits: j1..j3)
JUMP_TABLE = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def clean_line(line):
    """Strip comments and surrounding whitespace."""
    comment_pos = line.find("//")
    if comment_pos != -1:
        line = line[:comment_pos]
    return line.strip().replace(" ", "")


def assemble(source_path):
    if not os.path.exists(source_path):
        print(f"Error: file not found: {source_path}")
        return

    with open(source_path, "r") as f:
        lines = f.readlines()

    # Pass 1: Build symbol table with labels
    symbol_table = PREDEFINED_SYMBOLS.copy()
    labels_dict = {}
    instructions = []
    rom_address = 0

    for line in lines:
        cleaned = clean_line(line)
        if not cleaned:
            continue
        if cleaned.startswith("(") and cleaned.endswith(")"):
            label = cleaned[1:-1]
            symbol_table[label] = rom_address
            labels_dict[label] = rom_address
        else:
            instructions.append(cleaned)
            rom_address += 1

    # Pass 2: Allocate variables and generate binary machine code
    binary_lines = []
    variables_dict = {}
    next_var_address = 16

    for inst in instructions:
        if inst.startswith("@"):
            value = inst[1:]
            if value.isdigit():
                addr = int(value)
            else:
                if value not in symbol_table:
                    symbol_table[value] = next_var_address
                    variables_dict[value] = next_var_address
                    next_var_address += 1
                addr = symbol_table[value]
            # 16-bit binary representation with leading 0
            binary_code = format(addr, "016b")
            binary_lines.append(binary_code)
        else:
            # C-instruction parsing: dest=comp;jump
            dest = ""
            jump = ""
            comp = inst

            if "=" in comp:
                dest, comp = comp.split("=")
            if ";" in comp:
                comp, jump = comp.split(";")

            c_bits = COMP_TABLE.get(comp, "0000000")
            d_bits = DEST_TABLE.get(dest, "000")
            j_bits = JUMP_TABLE.get(jump, "000")

            binary_code = f"111{c_bits}{d_bits}{j_bits}"
            binary_lines.append(binary_code)

    # Write .hack output
    output_path = os.path.splitext(source_path)[0] + ".hack"
    with open(output_path, "w") as f:
        for b in binary_lines:
            f.write(b + "\n")
    print(f"Assembled successfully: {output_path} ({len(binary_lines)} instructions)")

    # Extra Feature (K % 3 == 0): Save all labels and variables with addresses to symbols.txt
    symbols_output_path = os.path.join(os.path.dirname(source_path) or ".", "symbols.txt")
    with open(symbols_output_path, "w") as f:
        f.write("=== LABELS ===\n")
        f.write(f"{'Label Name':<25} {'ROM Address':<15}\n")
        f.write("-" * 40 + "\n")
        for lbl, addr in labels_dict.items():
            f.write(f"{lbl:<25} {addr:<15}\n")

        f.write("\n=== VARIABLES ===\n")
        f.write(f"{'Variable Name':<25} {'RAM Address':<15}\n")
        f.write("-" * 40 + "\n")
        for var, addr in variables_dict.items():
            f.write(f"{var:<25} {addr:<15}\n")

        f.write("\n=== PREDEFINED SYMBOLS ===\n")
        f.write(f"{'Symbol Name':<25} {'Address':<15}\n")
        f.write("-" * 40 + "\n")
        for sym, addr in PREDEFINED_SYMBOLS.items():
            f.write(f"{sym:<25} {addr:<15}\n")

    print(f"Symbols exported to: {symbols_output_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        # Default to Box.asm if present in current directory
        target_file = "Box.asm" if os.path.exists("Box.asm") else None

    if not target_file or not os.path.exists(target_file):
        print("Usage: python assembler.py <file.asm>")
        sys.exit(1)

    assemble(target_file)
