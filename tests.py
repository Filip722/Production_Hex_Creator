import unittest
import os
from stm8s_production_hex_creator import *

class NamesTestCase(unittest.TestCase):

    def test_convert_string_to_hex(self):
        banana_string = convert_string_to_hex("banana")
        self.assertEqual(banana_string, '62616E616E61')

    def test_add_zeros(self):
        test_string = add_zeros("test")
        self.assertEqual(len(test_string), 73)

    def test_calculate_hex_checksum(self):
        line = ":2040200046494C49502D4C4150544F500000000000000000000000000000000000000000"
        result = calculate_hex_checksum(line)
        self.assertEqual(result, "0F")

    def test_create_empty_file(self):
        file_name = "test_file.hex"
        make_hex_file(file_name, 128)
        with open(file_name) as file:
            file_content = file.readlines()

        self.assertEqual(file_content[0], ":20400000\n")
        self.assertEqual(file_content[1], ":20402000\n")
        self.assertEqual(file_content[2], ":20404000\n")
        self.assertEqual(file_content[3], ":20406000\n")
        self.assertEqual(file_content[4], ":00000001FF\n")
        os.remove(file_name)


unittest.main()