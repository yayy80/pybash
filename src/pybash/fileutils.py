# fileutils.py
import os
from . import linvm

def getcurrentdir():
    return linvm.VIRTUAL_CWD

def ls(path=None):
    try:
        if path is None:
            real = linvm.resolve_path(".")
        else:
            real = linvm.resolve_path(path)

        return os.listdir(real)
    except Exception as e:
        return [f"ls: {e}"]

def changedir(path):
    global linvm

    try:
        real = linvm.resolve_path(path)

        if not os.path.isdir(real):
            return [f"cd: no such directory: {path}"]

        rel = os.path.relpath(real, linvm.PYBASH_ROOT)
        linvm.VIRTUAL_CWD = "/" if rel == "." else "/" + rel.replace("\\", "/")

        return []
    except Exception as e:
        return [f"cd: {e}"]
