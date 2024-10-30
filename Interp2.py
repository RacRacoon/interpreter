import re

# Fungsi konversi bilangan
def konversi(angka, basis_masuk, basis_keluar):
    try:
        angka = int(angka, basis_masuk)
        if basis_keluar == 2:
            return bin(angka)[2:]
        elif basis_keluar == 8:
            return oct(angka)[2:]
        elif basis_keluar == 10:
            return str(angka)
        elif basis_keluar == 16:
            return hex(angka)[2:].upper()
        else:
            return "Basis tujuan tidak didukung"
    except ValueError:
        return "Error: Format angka tidak valid"

# Fungsi untuk mengeksekusi perintah
def interpret_line(line, variables):
    if not line.strip() or line.startswith("#"):
        return True

    context = {"konversi": konversi}
    for var_name, var_value in variables.items():
        context[var_name] = var_value

    try:
        # Deklarasi variabel dengan 'meong'
        if line.startswith("meong"):
            match = re.match(r"meong\s+(\w+)\s*=\s*(.+)", line)
            if match:
                var_name, expression = match.groups()
                result = eval(expression, {}, context)
                variables[var_name] = result
            return True

        # Print dengan 'miau'
        elif line.startswith("miau"):
            match = re.findall(r'miau\s*\((.+)\)', line)[0]
            parts = [p.strip() for p in match.split(',')]
            values = []
            for part in parts:
                try:
                    value = eval(part, {}, context)
                    values.append(value)
                except:
                    values.append(part.strip('"'))
            print(*values)
            return True

        # Input dengan 'ngeong'
        elif line.startswith("ngeong"):
            match = re.match(r"ngeong\s+(\w+)\s*=\s*(.+)", line)
            if match:
                var_name, prompt = match.groups()
                prompt = prompt.strip('"')
                variables[var_name] = input(prompt)
            return True

        return True

    except Exception as e:
        print(f"Error pada baris '{line}': {str(e)}")
        return False

# Fungsi utama untuk menjalankan interpreter
def run_kucing_script(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        variables = {}
        for line in lines:
            interpret_line(line.strip(), variables)

    except FileNotFoundError:
        print(f"Error: File {file_path} tidak ditemukan")
    except Exception as e:
        print(f"Error: {str(e)}")

# Jalankan interpreter
if name == "main":

    run_kucing_script("coba.cat")