# main.py
from main_tty import process_command
import linvm
import fileutils

print("Welcome to PyBash!")
print("Type 'help' to see commands.")

while True:
    try:
        prompt = f"{linvm.getuser()}@pybash:{fileutils.getcurrentdir()}$ "
        cmd = input(prompt)
        output = process_command(cmd)
        for line in output:
            print(line)
    except SystemExit:
        print("Exiting PyBash...")
        break
