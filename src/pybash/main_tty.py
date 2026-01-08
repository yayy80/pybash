# main_tty.py
import shlex
from .command import command_list
from . import linvm

linvm.init_commands()

def process_command(user_input: str):
    user_input = user_input.strip()
    if not user_input:
        return []

    try:
        parts = shlex.split(user_input)
    except ValueError as e:
        return [f"Parse error: {e}"]

    cmd_name, *args = parts

    for cmd in command_list:
        if cmd.name == cmd_name:
            result = cmd.function(*args)
            if result is None:
                return []
            if isinstance(result, list):
                return result
            return [str(result)]

    return [f"{cmd_name}: command not found"]
