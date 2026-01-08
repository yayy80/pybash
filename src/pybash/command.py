# command.py
from . import fileutils
import code
import runpy
import sys
import io
import traceback

command_list = []

# --------------------------------------------------
# Base command class
# --------------------------------------------------

class Command:
    def __init_subclass__(cls):
        instance = cls()
        command_list.append(instance)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def function(self, *args):
        return []

# --------------------------------------------------
# Built-in commands
# --------------------------------------------------

class HelpCommand(Command):
    def __init__(self):
        super().__init__("help", "Show available commands")

    def function(self):
        lines = ["Available commands:"]
        for cmd in command_list:
            lines.append(f"- {cmd.name}: {cmd.description}")
        return lines


class LsCommand(Command):
    def __init__(self):
        super().__init__("ls", "List directory contents")

    def function(self, path=None):
        return fileutils.ls(path)


class CdCommand(Command):
    def __init__(self):
        super().__init__("cd", "Change directory")

    def function(self, path=None):
        if path is None:
            return ["cd: missing operand"]
        return fileutils.changedir(path)


class PwdCommand(Command):
    def __init__(self):
        super().__init__("pwd", "Print working directory")

    def function(self):
        return [fileutils.getcurrentdir()]


class ExitCommand(Command):
    def __init__(self):
        super().__init__("exit", "Exit PyBash")

    def function(self):
        raise SystemExit

# --------------------------------------------------
# Python command (CAPTURES OUTPUT)
# --------------------------------------------------

class PythonCommand(Command):
    def __init__(self):
        super().__init__("python", "Run Python file (output captured)")

    def function(self, *args):
        # No args → explain limitation
        if not args:
            return [
                "python: interactive REPL is not available inside the Pygame terminal",
                "python <file.py> will run and capture output"
            ]

        filename = args[0]

        # Capture stdout + stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        buffer = io.StringIO()

        sys.stdout = buffer
        sys.stderr = buffer

        try:
            runpy.run_path(filename, run_name="__main__")
        except FileNotFoundError:
            return [f"python: can't open file '{filename}'"]
        except Exception:
            traceback.print_exc()
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        output = buffer.getvalue().splitlines()
        return output if output else ["(no output)"]

# --------------------------------------------------
# Pygame text editor (pgte)
# --------------------------------------------------

class PgTeCommand(Command):
    def __init__(self):
        super().__init__("pgte", "Open Pygame text editor")

    def function(self, filename=None):
        if filename is None:
            return ["pgte: missing filename"]

        # CONTROL SIGNAL (not text!)
        return [{
            "action": "open_editor",
            "filename": filename
        }]
