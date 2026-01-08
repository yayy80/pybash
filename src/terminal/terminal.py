# pygame_terminal.py
import sys
import os

BASE_DIR = os.path.dirname(__file__)
MAIN_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "main"))
sys.path.append(MAIN_DIR)

import pygame
from main_tty import process_command
import linvm
import fileutils

pygame.init()

# ---------------- STATE ----------------
mode = "shell"  # "shell" or "editor"
editor_lines = []
editor_cursor_x = 0
editor_cursor_y = 0
editor_filename = None

buffer = [
    "Welcome to PyBash (Pygame Edition)",
    "Type 'help' to get started."
]
current_input = ""
# --------------------------------------

WIDTH, HEIGHT = 900, 600
FONT_SIZE = 18
LINE_HEIGHT = FONT_SIZE + 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyBash Terminal")

font = pygame.font.SysFont("consolas", FONT_SIZE)
clock = pygame.time.Clock()

BG = (15, 15, 15)
FG = (230, 230, 230)

def prompt():
    return f"{linvm.getuser()}@pybash:{fileutils.getcurrentdir()}$ "

def draw():
    screen.fill(BG)

    if mode == "shell":
        max_lines = (HEIGHT - 40) // LINE_HEIGHT
        visible = buffer[-max_lines:]

        y = 10
        for line in visible:
            text = font.render(line, True, FG)
            screen.blit(text, (10, y))
            y += LINE_HEIGHT

        input_line = font.render(prompt() + current_input, True, FG)
        screen.blit(input_line, (10, HEIGHT - 30))

    elif mode == "editor":
        screen.fill((10, 10, 30))

        y = 10
        for line in editor_lines:
            text = font.render(line, True, FG)
            screen.blit(text, (10, y))
            y += LINE_HEIGHT

        # Cursor
        if editor_lines:
            cx = 10 + font.size(
                editor_lines[editor_cursor_y][:editor_cursor_x]
            )[0]
            cy = 10 + editor_cursor_y * LINE_HEIGHT
            pygame.draw.rect(screen, FG, (cx, cy, 2, LINE_HEIGHT))

    pygame.display.flip()

# ---------------- MAIN LOOP ----------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ---------- EDITOR MODE ----------
        if mode == "editor" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                mode = "shell"
                continue

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                with open(editor_filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(editor_lines))
                continue

            if event.key == pygame.K_RETURN:
                editor_lines.insert(editor_cursor_y + 1, "")
                editor_cursor_y += 1
                editor_cursor_x = 0
                continue

            if event.key == pygame.K_BACKSPACE:
                if editor_cursor_x > 0:
                    line = editor_lines[editor_cursor_y]
                    editor_lines[editor_cursor_y] = (
                        line[:editor_cursor_x - 1] + line[editor_cursor_x:]
                    )
                    editor_cursor_x -= 1
                continue

            if event.unicode and event.unicode.isprintable():
                line = editor_lines[editor_cursor_y]
                editor_lines[editor_cursor_y] = (
                    line[:editor_cursor_x] + event.unicode + line[editor_cursor_x:]
                )
                editor_cursor_x += 1
                continue

        # ---------- SHELL MODE ----------
        if mode == "shell" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                buffer.append(prompt() + current_input)

                try:
                    output = process_command(current_input)
                    for item in output:
                        if isinstance(item, dict) and item.get("action") == "open_editor":
                            editor_filename = item["filename"]
                            mode = "editor"

                            try:
                                with open(editor_filename, "r", encoding="utf-8") as f:
                                    editor_lines = f.read().splitlines()
                            except FileNotFoundError:
                                editor_lines = [""]

                            editor_cursor_x = 0
                            editor_cursor_y = 0
                        else:
                            buffer.append(item)

                except SystemExit:
                    pygame.quit()
                    sys.exit()

                current_input = ""

            elif event.key == pygame.K_BACKSPACE:
                current_input = current_input[:-1]

            else:
                if event.unicode.isprintable():
                    current_input += event.unicode

    draw()
    clock.tick(60)
