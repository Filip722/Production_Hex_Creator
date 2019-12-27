# Production_Hex_Creator
Simple script to generate a file for EEPROM in the STM8S for production data with current time (of programming) and computer name

## What does it do:
It creates a STM8S EEPROM hexfile with:
1. Computer name of the user running the script on memory addres 0x4020
2. Current time of running the script on memory address 0x4040

## How to use:
create_production_hex_file(file_name, number_of_bytes)

For example, on STM8S003: 

    'py stm8s_production_hex_creator.py "C:/production/EEPROM.hex" 128'
