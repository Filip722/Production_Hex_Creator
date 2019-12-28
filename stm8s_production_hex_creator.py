import os
import sys
from datetime import datetime


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_computer_name():
    return os.environ['COMPUTERNAME']


def convert_string_to_hex(input_string):
    output = ""

    for i, _ in enumerate(input_string):
        output += (hex(ord(input_string[i])))[2:].upper()
    return output


def make_hex_file(file_name, number_of_bytes):
    with open(file_name, "w+") as file:
        for line in range(0, (number_of_bytes // 32)):
            file.write(":20")  # start symbol + number of bytes
            file.write("4" + format(line * 2, '02x').upper() + "0")  # address, stm8s format
            file.write("00\n")  # data type
        file.write(":00000001FF\n")  # end of file


def add_zeros(line):
    required_len = 73  # number of characters in a line in a hex file

    while len(line) < required_len:
        line += '0'

    return line


def calculate_hex_checksum(line):
    line_to_calculate = line[1:]  # remove ':' from the line
    hex_list = []

    for i in range(0, len(line_to_calculate), 2):  # make a list of hex values from string
        hex_list.append(line_to_calculate[i:i + 2])

    checksum = sum(int(hex_value, 16)
                   for hex_value in hex_list)  # sum list as int
    checksum = 256 - checksum % 256  # calculate INTEL HEX checksum
    checksum = format(checksum, '02x').upper()  # format the output, removing '0x'
    return checksum


def create_production_hex_file(file_name, number_of_bytes):
    make_hex_file(file_name, int(number_of_bytes))

    with open(file_name) as file:
        file_content = file.readlines()

    for i, _ in enumerate(file_content[:-1]):
        file_content[i] = file_content[i].rstrip()

    file_content[1] += convert_string_to_hex(get_computer_name())
    file_content[2] += convert_string_to_hex(get_current_time())

    for i, _ in enumerate(file_content[:-1]):
        file_content[i] = add_zeros(file_content[i])
        file_content[i] += calculate_hex_checksum(file_content[i])
        file_content[i] += '\n'

    with open(file_name, 'w') as file:
        file.writelines(file_content)


if __name__ == "__main__":
    create_production_hex_file(sys.argv[1], sys.argv[2])
