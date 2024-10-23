import sys

# Read arguments
program_filepath = sys.argv[1]

# Tokenize program
program_lines = []
with open(program_filepath, "r") as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]

program = []
token_counter = 0
label_tracker = {}
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]

    if opcode == "":
        continue
    if opcode.endswith(":"):
        label_tracker[opcode[:-1]] = token_counter  # Track the label positions
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
    elif opcode in ["CEK.EQ.0", "CEK.GT.0"]:
        label = parts[1]
        program.append(label)
        token_counter += 1

# Implementasi stack
class Stack:
    def __init__(self, size):
        self.buf = [0 for _ in range(size)]
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
    elif opcode == "SUB":
        a = stack.pop()
        b = stack.pop()
        stack.push(a - b)
    elif opcode == "MOD":
        b = stack.pop()
        a = stack.pop()
        stack.push(a % b)
    elif opcode == "BUST":
        if pc < len(program) and isinstance(program[pc], str):
            # Jika ada string literal setelah BUST, cetak string tersebut
            string_literal = program[pc]
            pc += 1
            print(string_literal)
        else:
            # Jika tidak ada string literal, cetak nilai dari stack
            if stack.sp >= 0:  # Pastikan stack tidak kosong
                print(stack.pop())
            else:
                print("Stack kosong, tidak ada nilai untuk dicetak.")
    elif opcode == "AMBIL":
        number = int(input())
        stack.push(number)
    elif opcode == "CEK.EQ.0":
        number = stack.top()
        label = program[pc]
        pc += 1
        if number == 0:
            if label in label_tracker:
                pc = label_tracker[label]
            else:
                print(f"Label {label} tidak ditemukan.")
                break
    elif opcode == "CEK.GT.0":
        number = stack.top()
        label = program[pc]
        pc += 1
        if number > 0:
            if label in label_tracker:
                pc = label_tracker[label]
            else:
                print(f"Label {label} tidak ditemukan.")
                break

# Program akan berhenti ketika mencapai "UDAHAN"
