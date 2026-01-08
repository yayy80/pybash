# linvm.py
import os
import getpass

# --------------------------------------------------
# PYBASH ROOT (REAL DIRECTORY ON DISK)
# --------------------------------------------------

PYBASH_ROOT = os.path.abspath(
    os.path.expanduser("~/pybash_root")
)

# Directory layout inside PyBash
DIRS = [
    "home",
    f"home/{getpass.getuser()}",
    "bin",
    "tmp",
]

# Create root and subdirectories if missing
os.makedirs(PYBASH_ROOT, exist_ok=True)
for d in DIRS:
    os.makedirs(os.path.join(PYBASH_ROOT, d), exist_ok=True)

# --------------------------------------------------
# VIRTUAL FILESYSTEM STATE
# --------------------------------------------------

# Virtual current working directory (POSIX-style)
VIRTUAL_CWD = "/home/" + getpass.getuser()

# --------------------------------------------------

def init_commands():
    pass

def getuser():
    return getpass.getuser()

def resolve_path(path: str) -> str:
    """
    Convert a PyBash path to a real OS path.
    Prevents escaping the PyBash root.
    """
    global VIRTUAL_CWD

    # Absolute virtual path
    if path.startswith("/"):
        virtual = path
    else:
        virtual = os.path.join(VIRTUAL_CWD.lstrip("/"), path)

    # Normalize and map to real filesystem
    real = os.path.normpath(
        os.path.join(PYBASH_ROOT, virtual.lstrip("/"))
    )

    # Security: prevent escape
    if not real.startswith(PYBASH_ROOT):
        raise PermissionError("Access outside PyBash root is not allowed")

    return real
