# pybash_core.py
import shlex
from command import command_list
import linvm

def process_command(user_input: str):
    output = []

    user_input = user_input.strip()
    if not user_input:
        return output

    try:
        parts = shlex.split(user_input)
    except ValueError as e:
        return [f"Parse error: {e}"]

    cmd_name = parts[0]
    args = parts[1:]

    for cmd in command_list:
        if cmd.name == cmd_name:
            result = cmd.function(*args)

            if isinstance(result, list):
                output.extend(result)
            elif isinstance(result, str):
                output.append(result)

            return output

    return [f"{cmd_name}: command not found"]
