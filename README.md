# Production_Hex_Creator
Simple script to generate a file for EEPROM in the STM8S for production data with time of programming and computer name

## What does it do:
It creates a STM8S003 EEPROM hexfile with:
1. Computer name of the user running the script on memory addres 0x4020
2. Current time of running the script on memory address 0x4040

## How to use:
Run by "py main.py "filename", where file name is a path with filename to use

For example: py main.py "C:/production/EEPROM.hex"
