import sys

# Membaca argumen
program_filepath = sys.argv[1]

# Membaca dan memproses program dari file
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
        label_tracker[opcode[:-1]] = token_counter  # Lacak posisi label
        continue

    program.append(opcode)
    token_counter += 1

    if opcode == "PUSH":
        number = int(parts[1])
        program.append(number)
        token_counter += 1
    elif opcode == "BUST" and len(parts) > 1:
        string_literal = ' '.join(parts[1:])[1:-1]
        program.append(string_literal)
        token_counter += 1
    elif opcode in ["CEK.KALO.0", "CEK.NGGAK.0"]:
        label = parts[1]
        program.append(label)
        token_counter += 1

# Implementasi stack
class Stack:
    def __init__(self, size):
        self.buf = [0] * size
        self.sp = -1

    def push(self, number):
        self.sp += 1
        self.buf[self.sp] = number

    def pop(self):
        if self.sp < 0:
            raise IndexError("Pop dari stack kosong")
        number = self.buf[self.sp]
        self.sp -= 1
        return number

    def top(self):
        if self.sp < 0:
            raise IndexError("Top dari stack kosong")
        return self.buf[self.sp]

# Eksekusi program
pc = 0
stack = Stack(256)

while pc < len(program) and program[pc] != "UDAHAN":
    opcode = program[pc]
    pc += 1

    if opcode == "PUSH":
        number = program[pc]
        pc += 1
        stack.push(number)
    elif opcode == "POP":
        stack.pop()
    elif opcode == "ADD":
        a = stack.pop()
        b = stack.pop()
        stack.push(a + b)
    elif opcode == "KURANGIN":
        a = stack.pop()
        b = stack.pop()
        stack.push(a - b)
    elif opcode == "MOD":
        b = stack.pop()
        a = stack.pop()
        stack.push(a % b)
    elif opcode == "BUST":
        if pc < len(program) and isinstance(program[pc], str):
            # Cetak string literal jika ada
            string_literal = program[pc]
            pc += 1
            print(string_literal)
        else:
            # Cetak nilai dari stack jika tidak ada string literal
            if stack.sp >= 0:
                print(stack.pop())
            else:
                print("Stack kosong, tidak ada nilai untuk dicetak.")
    elif opcode == "AMBIL":
        try:
            number = int(input("Masukkan angka: "))
            stack.push(number)
        except ValueError:
            print("Input tidak valid, masukkan angka!")
    elif opcode == "CEK.KALO.0":
        number = stack.pop()
        label = program[pc]
        pc += 1
        if number == 0:
            pc = label_tracker.get(label, pc)
    elif opcode == "CEK.NGGAK.0":
        number = stack.pop()
        label = program[pc]
        pc += 1
        if number != 0:
            pc = label_tracker.get(label, pc)
    elif opcode == "GANTIBINER":
        number = stack.pop()
        print(bin(number)[2:])  # Konversi ke biner dan cetak tanpa '0b'
        stack.push(number)      # Memasukkan kembali angka asli ke stack
    elif opcode == "GANTIHEXA":
        number = stack.pop()
        print(hex(number)[2:])  # Konversi ke heksadesimal dan cetak tanpa '0x'
        stack.push(number)      # Memasukkan kembali angka asli ke stack
    elif opcode == "GANTIOKTA":
        number = stack.pop()
        print(oct(number)[2:])  # Konversi ke oktal dan cetak tanpa '0o'
        stack.push(number)      # Memasukkan kembali angka asli ke stack

# Program berhenti saat mencapai "UDAHAN"
