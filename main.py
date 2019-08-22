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

    for i, _ in enumerate(current_time):
        hex_char = (hex(ord(current_time[i])))[2:].upper()
        time_in_hex.append(hex_char)

    return time_in_hex


def get_computer_name_in_hex():
    computer_name = get_computer_name()
    computer_name_in_hex = []

    for i, _ in enumerate(computer_name):
        hex_char = (hex(ord(computer_name[i])))[2:].upper()
        computer_name_in_hex.append(hex_char)

    return computer_name_in_hex


def create_production_hex(file_name):
    file = open(file_name, "w+")

    file.write(
        ":204000000000000000000000000000000000000000000000000000000000000000000000A0\n")
    file.write(
        ":20402000000000000000000000000000000000000000000000000000000000000000000080\n")
    file.write(
        ":20404000000000000000000000000000000000000000000000000000000000000000000060\n")
    file.write(
        ":20406000000000000000000000000000000000000000000000000000000000000000000040\n")
    file.write(
        ":20408000000000000000000000000000000000000000000000000000000000000000000020\n")
    file.write(
        ":2040A000000000000000000000000000000000000000000000000000000000000000000000\n")
    file.write(
        ":2040C0000000000000000000000000000000000000000000000000000000000000000000E0\n")
    file.write(
        ":2040E0000000000000000000000000000000000000000000000000000000000000000000C0\n")
    file.write(
        ":2041000000000000000000000000000000000000000000000000000000000000000000009F\n")
    file.write(
        ":2041200000000000000000000000000000000000000000000000000000000000000000007F\n")
    file.write(
        ":2041400000000000000000000000000000000000000000000000000000000000000000005F\n")
    file.write(
        ":2041600000000000000000000000000000000000000000000000000000000000000000003F\n")
    file.write(
        ":2041800000000000000000000000000000000000000000000000000000000000000000001F\n")
    file.write(
        ":2041A0000000000000000000000000000000000000000000000000000000000000000000FF\n")
    file.write(
        ":2041C0000000000000000000000000000000000000000000000000000000000000000000DF\n")
    file.write(
        ":2041E0000000000000000000000000000000000000000000000000000000000000000000BF\n")
    file.write(
        ":2042000000000000000000000000000000000000000000000000000000000000000000009E\n")
    file.write(
        ":2042200000000000000000000000000000000000000000000000000000000000000000007E\n")
    file.write(
        ":2042400000000000000000000000000000000000000000000000000000000000000000005E\n")
    file.write(
        ":2042600000000000000000000000000000000000000000000000000000000000000000003E\n")
    file.write(":00000001FF\n")

    file.close()


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
    file_name = str(sys.argv[1])

    if os.path.isfile(file_name) == 0:
        create_production_hex(file_name)

    with open(file_name) as file:
        file_content = file.readlines()

    file_content[1] = ':20402000' + \
        ''.join(map(str, get_computer_name_in_hex()))
    file_content[2] = ':20404000' + \
        ''.join(map(str, get_current_time_in_hex()))

    for i in range(1, 3):
        file_content[i] = add_missing_zeros(file_content[i])
        file_content[i] += calculate_hex_checksum(file_content[i])
        file_content[i] += '\n'

    with open(file_name, 'w') as file:
        file.writelines(file_content)


if __name__ == "__main__":
    main()
