import os
import sys
from datetime import datetime


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_computer_name():
    return os.environ['COMPUTERNAME']


def get_current_time_in_hex():
    current_time = get_current_time()
    time_in_hex = []

    for i in range(0, len(current_time)):
        x = (hex(ord(current_time[i])))[2:].upper()
        time_in_hex.append(x)

    return time_in_hex


def get_computer_name_in_hex():
    computer_name = get_computer_name()
    computer_name_in_hex = []

    for i in range(0, len(computer_name)):
        x = (hex(ord(computer_name[i])))[2:].upper()
        computer_name_in_hex.append(x)

    return computer_name_in_hex


def create_production_hex(file_name):
    f = open(file_name, "w+")

    f.write(
        ":204000000000000000000000000000000000000000000000000000000000000000000000A0\n")
    f.write(
        ":20402000000000000000000000000000000000000000000000000000000000000000000080\n")
    f.write(
        ":20404000000000000000000000000000000000000000000000000000000000000000000060\n")
    f.write(
        ":20406000000000000000000000000000000000000000000000000000000000000000000040\n")
    f.write(
        ":20408000000000000000000000000000000000000000000000000000000000000000000020\n")
    f.write(
        ":2040A000000000000000000000000000000000000000000000000000000000000000000000\n")
    f.write(
        ":2040C0000000000000000000000000000000000000000000000000000000000000000000E0\n")
    f.write(
        ":2040E0000000000000000000000000000000000000000000000000000000000000000000C0\n")
    f.write(
        ":2041000000000000000000000000000000000000000000000000000000000000000000009F\n")
    f.write(
        ":2041200000000000000000000000000000000000000000000000000000000000000000007F\n")
    f.write(
        ":2041400000000000000000000000000000000000000000000000000000000000000000005F\n")
    f.write(
        ":2041600000000000000000000000000000000000000000000000000000000000000000003F\n")
    f.write(
        ":2041800000000000000000000000000000000000000000000000000000000000000000001F\n")
    f.write(
        ":2041A0000000000000000000000000000000000000000000000000000000000000000000FF\n")
    f.write(
        ":2041C0000000000000000000000000000000000000000000000000000000000000000000DF\n")
    f.write(
        ":2041E0000000000000000000000000000000000000000000000000000000000000000000BF\n")
    f.write(
        ":2042000000000000000000000000000000000000000000000000000000000000000000009E\n")
    f.write(
        ":2042200000000000000000000000000000000000000000000000000000000000000000007E\n")
    f.write(
        ":2042400000000000000000000000000000000000000000000000000000000000000000005E\n")
    f.write(
        ":2042600000000000000000000000000000000000000000000000000000000000000000003E\n")
    f.write(":00000001FF\n")

    f.close()


# adds missing zero's to the given line to satisfy the hex file
def add_missing_zeros(line):
    required_len = 73  # number of characters in a line in a hex file

    while len(line) < required_len:
        line += '0'

    return line


def calculate_hex_checksum(line):
    line_to_calculate = line[1:]  # remove ':' from the line
    temp2 = [line_to_calculate[i:i + 2]
             for i in range(0, len(line_to_calculate), 2)]
    sum = 0
    i = 0
    for n in temp2:
        sum += int(temp2[i], 16)
        i += 1
    sum = (sum % 256)
    sum -= 1 << 8
    sum = format(abs(sum), 'x').upper()
    if len(sum) < 2:
        sum = '0' + sum
    return sum


def main():
    file = str(sys.argv[1])

    if os.path.isfile(file) == 0:
        create_production_hex(file)

    with open(file) as f:
        file_content = f.readlines()

    file_content[1] = ':20402000' + \
        ''.join(map(str, get_computer_name_in_hex()))
    file_content[2] = ':20404000' + \
        ''.join(map(str, get_current_time_in_hex()))

    for i in range(1, 3):
        file_content[i] = add_missing_zeros(file_content[i])
        file_content[i] += calculate_hex_checksum(file_content[i])
        file_content[i] += '\n'

    with open(file, 'w') as f:
        f.writelines(file_content)


if __name__ == "__main__":
    main()
