# command.py
import os
import fileutils
import code
import runpy

command_list = []

class Command:
    def __init_subclass__(cls):
        instance = cls()
        command_list.append(instance)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def function(self, *args):
        return []


class HelpCommand(Command):
    def __init__(self):
        super().__init__("help", "Show available commands")

    def function(self):
        lines = ["Available commands:"]
        for cmd in command_list:
            lines.append(f"- {cmd.name}: {cmd.description}")
        return lines
class PythonCommand(Command):
    def __init__(self):
        super().__init__("python", "Run Python REPL or a Python file")

    def function(self, *args):
        # python → interactive REPL
        if len(args) == 0:
            banner = "PyBash Python REPL (Ctrl-D to exit)"
            code.interact(banner=banner, local={})
            return []

        # python file.py
        filename = args[0]
        try:
            runpy.run_path(filename, run_name="__main__")
            return []
        except FileNotFoundError:
            return [f"python: can't open file '{filename}'"]
        except Exception as e:
            return [f"python error: {e}"]

class PgTeCommand(Command):
    def __init__(self):
        super().__init__("pgte", "Open Pygame text editor")

    def function(self, filename=None):
        if filename is None:
            return ["pgte: missing filename"]

        # Special signal to terminal
        return [{
            "action": "open_editor",
            "filename": filename
        }]

class LsCommand(Command):
    def __init__(self):
        super().__init__("ls", "List directory contents")

    def function(self, directory=None):
        directory = directory or os.getcwd()
        try:
            return os.listdir(directory)
        except Exception:
            return [f"ls: cannot access '{directory}'"]


class CdCommand(Command):
    def __init__(self):
        super().__init__("cd", "Change directory")

    def function(self, directory=None):
        if directory is None:
            return ["cd: missing operand"]
        try:
            os.chdir(directory)
            return []
        except Exception as e:
            return [f"cd: {e}"]


class ExitCommand(Command):
    def __init__(self):
        super().__init__("exit", "Exit PyBash")

    def function(self):
        raise SystemExit
