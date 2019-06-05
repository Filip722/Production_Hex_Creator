import os, sys
from datetime import datetime


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_computer_name():
    return os.environ['COMPUTERNAME']


def get_current_time_in_hex():
    current_time = get_current_time()
    time_in_hex = []
    i = 0

    for letters in current_time:
        x = (hex(ord(current_time[i])))[2:].upper()
        time_in_hex.append(x)
        i += 1

    return time_in_hex


def get_computer_name_in_hex():
    computer_name = get_computer_name()
    computer_name_in_hex = []
    i = 0

    for letters in computer_name:
        x = (hex(ord(computer_name[i])))[2:].upper()
        computer_name_in_hex.append(x)
        i += 1

    return computer_name_in_hex


def create_production_hex(file_name):
    f = open(file_name, "w+")

    f.write(":204000000000000000000000000000000000000000000000000000000000000000000000A0\n")
    f.write(":20402000000000000000000000000000000000000000000000000000000000000000000080\n")
    f.write(":20404000000000000000000000000000000000000000000000000000000000000000000060\n")
    f.write(":20406000000000000000000000000000000000000000000000000000000000000000000040\n")
    f.write(":20408000000000000000000000000000000000000000000000000000000000000000000020\n")
    f.write(":2040A000000000000000000000000000000000000000000000000000000000000000000000\n")
    f.write(":2040C0000000000000000000000000000000000000000000000000000000000000000000E0\n")
    f.write(":2040E0000000000000000000000000000000000000000000000000000000000000000000C0\n")
    f.write(":2041000000000000000000000000000000000000000000000000000000000000000000009F\n")
    f.write(":2041200000000000000000000000000000000000000000000000000000000000000000007F\n")
    f.write(":2041400000000000000000000000000000000000000000000000000000000000000000005F\n")
    f.write(":2041600000000000000000000000000000000000000000000000000000000000000000003F\n")
    f.write(":2041800000000000000000000000000000000000000000000000000000000000000000001F\n")
    f.write(":2041A0000000000000000000000000000000000000000000000000000000000000000000FF\n")
    f.write(":2041C0000000000000000000000000000000000000000000000000000000000000000000DF\n")
    f.write(":2041E0000000000000000000000000000000000000000000000000000000000000000000BF\n")
    f.write(":20420000000000000000000000000000000000000000000000000000000000000000000000\n")
    f.write(":20422000000000000000000000000000000000000000000000000000000000000000000000\n")
    f.write(":20424000000000000000000000000000000000000000000000000000000000000000000000\n")
    f.write(":2042600000000000000000000000000000000000000000000000000000000000000000003E\n")
    f.write(":00000001FF\n")

    f.close()


def add_missing_zeros(line):
    required_len = 73

    while len(line) < required_len:
        line += '0'
    return line


def calculate_hex_checksum(line):
    line_to_calculate = line[1:]
    temp2 = [line_to_calculate[i:i + 2] for i in range(0, len(line_to_calculate), 2)]
    sum = 0
    i = 0
    for n in temp2:
        sum += int(temp2[i], 16)
        i += 1
    sum = (sum % 256)
    sum -= 1 << 8
    sum = format(abs(sum), 'x').upper()
    return sum


file = str(sys.argv[1])

if os.path.isfile(file) == 0:
    create_production_hex(file)

with open(file) as f:
    file_content = f.readlines()

file_content[16] = ':20420000' + ''.join(map(str, get_computer_name_in_hex()))
file_content[17] = ':20422000' + ''  # space for custom data, serial number
file_content[18] = ':20424000' + ''.join(map(str, get_current_time_in_hex()))

file_content[16] = add_missing_zeros(file_content[16])
file_content[17] = add_missing_zeros(file_content[17])
file_content[18] = add_missing_zeros(file_content[18])

file_content[16] += calculate_hex_checksum(file_content[16])
file_content[17] += calculate_hex_checksum(file_content[17])
file_content[18] += calculate_hex_checksum(file_content[18])

file_content[16] += '\n'
file_content[17] += '\n'
file_content[18] += '\n'

with open(file, 'w') as f:
    f.writelines(file_content)
