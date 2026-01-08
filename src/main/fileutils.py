import os
import sys
import getpass
username = ""

def getusername():
    return getpass.getuser()

def getcurrentdir():
    return os.getcwd()


def ls(directory):
    try:
        files = os.listdir(directory)
        for file in files:
            print(file)
    except Exception as e:
        print(f"ls: cannot access '{directory}': No such file or directory", file=sys.stderr)

def getcurrentdir():
    return os.getcwd()

def changedir(directory):
    try:
        os.chdir(directory)
    except Exception as e:
        print(f"cd: {e}", file=sys.stderr)
def quit():
    sys.exit(0)