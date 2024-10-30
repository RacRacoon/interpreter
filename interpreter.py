import sys

program_filepath = sys.argv[1]

program_lines = []
with open(program_filepath, "r") as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]

program = []
token_counter = 0
label_tracker = {}

# Tokenisasi dan pelacakan label
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]

    if opcode == "":
        continue
    if opcode.endswith(":"):
        label_tracker[opcode[:-1]] = token_counter
        continue

    program.append(opcode)
    token_counter += 1

    if opcode == "DORONG":
        number = int(parts[1])
        program.append(number)
        token_counter += 1
    elif opcode == "CETAK":
        string_literal = ' '.join(parts[1:])[1:-1]
        program.append(string_literal)
        token_counter += 1
    elif opcode in ("LOMPAT.SAMA.0", "LOMPAT.LEBIH.0"):
        label = parts[1]
        program.append(label)
        token_counter += 1

class Stack:
    def __init__(self, size):  # Memperbaiki konstruktor
        self.buf = [0 for _ in range(size)]
        self.sp = -1

    def push(self, number):
        self.sp += 1
        self.buf[self.sp] = number

    def pop(self):
        if self.sp < 0:
            return 0
        number = self.buf[self.sp]
        self.sp -= 1
        return number

def convert_number(value, base_from, base_to):
    # Konversi angka berdasarkan basis yang diberikan
    if base_from == 2:
        decimal_value = int(value, 2)
    elif base_from == 8:
        decimal_value = int(value, 8)
    elif base_from == 10:
        decimal_value = int(value)
    elif base_from == 16:
        decimal_value = int(value, 16)

    if base_to == 2:
        return bin(decimal_value)[2:]  # Mengembalikan sebagai string biner
    elif base_to == 8:
        return oct(decimal_value)[2:]  # Mengembalikan sebagai string oktal
    elif base_to == 10:
        return str(decimal_value)        # Mengembalikan sebagai string desimal
    elif base_to == 16:
        return hex(decimal_value)[2:].upper()  # Mengembalikan sebagai string heksadesimal

pc = 0
stack = Stack(256)

while pc < len(program):
    opcode = program[pc]
    pc += 1

    if opcode == "AMBIL":
        value = input("Masukkan nilai yang ingin dikonversi: ")
        stack.push(value)
        base_from = int(input("Masukkan basis asal (Biner (2), Octal (8), Desimal (10), atau Hexadesimal (16)): "))
        stack.push(base_from)
        base_to = int(input("Masukkan basis tujuan (Biner (2), Octal (8), Desimal (10), atau Hexadesimal (16)): "))
        stack.push(base_to)
    elif opcode == "UBAH":
        base_to = stack.pop()
        base_from = stack.pop()
        value = stack.pop()
        result = convert_number(value, base_from, base_to)
        stack.push(result)
    elif opcode == "CETAK":
        print("Hasil konversi bilangan adalah:", stack.pop())
    elif opcode == "BERHENTI":
        break
