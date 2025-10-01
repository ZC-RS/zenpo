#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
import pygame
import random
from pyfiglet import Figlet
from colorama import init, Fore, Style

init(autoreset=True)

VERSION = "2.0.0"
CREATOR = "Zenpo"
REPO = "https://github.com/ZC-RS/zenpo"

def ascii_banner(text, colour=Fore.GREEN):
    f = Figlet(font='slant')
    return colour + f.renderText(text)

# -------------------- GAMES --------------------
def snake_game():
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    block = 20
    snake = [(WIDTH//2, HEIGHT//2)]
    direction = (0, 0)
    food = (random.randrange(0, WIDTH, block), random.randrange(0, HEIGHT, block))
    score = 0

    running = True
    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: direction = (0, -block)
                if event.key == pygame.K_DOWN: direction = (0, block)
                if event.key == pygame.K_LEFT: direction = (-block, 0)
                if event.key == pygame.K_RIGHT: direction = (block, 0)

        if direction != (0, 0):
            new_head = (snake[0][0]+direction[0], snake[0][1]+direction[1])
            if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
                break
            snake.insert(0, new_head)
            if new_head == food:
                food = (random.randrange(0, WIDTH, block), random.randrange(0, HEIGHT, block))
                score += 1
            else:
                snake.pop()

        screen.fill((0,0,0))
        for s in snake: pygame.draw.rect(screen, (0,255,0), (*s, block, block))
        pygame.draw.rect(screen, (255,0,0), (*food, block, block))
        pygame.display.flip()

    pygame.quit()

def battleship_game():
    pygame.init()
    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battleship")
    clock = pygame.time.Clock()

    grid_size = 10
    cell = WIDTH // grid_size
    ship = [(random.randint(0,9), random.randint(0,9))]
    hits = []

    font = pygame.font.SysFont(None, 24)
    running = True
    while running:
        screen.fill((0,0,64))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                gx, gy = x//cell, y//cell
                if (gx, gy) in ship: hits.append((gx,gy))

        for i in range(grid_size):
            for j in range(grid_size):
                rect = pygame.Rect(i*cell, j*cell, cell, cell)
                pygame.draw.rect(screen, (0,128,128), rect, 1)
                if (i,j) in hits: pygame.draw.rect(screen, (255,0,0), rect)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def tetris_game():
    pygame.init()
    WIDTH, HEIGHT = 200, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 24)
    running = True
    while running:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
        text = font.render("Tetris Placeholder", True, (255,255,255))
        screen.blit(text, (20, HEIGHT//2))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def minesweeper_game():
    pygame.init()
    WIDTH, HEIGHT = 400, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    running = True
    while running:
        screen.fill((192,192,192))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
        text = font.render("Minesweeper Placeholder", True, (0,0,0))
        screen.blit(text, (50, HEIGHT//2))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

def hangman_game():
    pygame.init()
    WIDTH, HEIGHT = 400, 300
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hangman")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    running = True
    while running:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
        text = font.render("Hangman Placeholder", True, (0,0,0))
        screen.blit(text, (50, HEIGHT//2))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

def game_2048():
    pygame.init()
    WIDTH, HEIGHT = 400, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    running = True
    while running:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
        text = font.render("2048 Placeholder", True, (0,0,0))
        screen.blit(text, (50, HEIGHT//2))
        pygame.display.flip()
        clock.tick(30)

# -------------------- GAME PANEL --------------------
def launch_game_panel():
    print(ascii_banner("Games [V2]"))
    print("[1] Snake")
    print("[2] Battleship")
    print("[3] Tetris")
    print("[4] Minesweeper")
    print("[5] Hangman")
    print("[6] 2048")

    choice = input("Select a game: ").strip()
    if choice=='1': snake_game()
    elif choice=='2': battleship_game()
    elif choice=='3': tetris_game()
    elif choice=='4': minesweeper_game()
    elif choice=='5': hangman_game()
    elif choice=='6': game_2048()
    else: print("Unknown choice")

# -------------------- CONTROL PANEL --------------------
def show_panel():
    print(ascii_banner("PANEL"))
    print(Fore.LIGHTBLUE_EX + "A general control panel for apps\n")
    print("Press different keys to open apps:\n")

    hotkeys = {
        "GM": ("Interactive Game Mode [V2]", None),
        "X": ("Exit the panel", None),
        "T": ("Open Task Manager", ["taskmgr"]),
        "C": ("Open CMD", ["cmd"]),
        "P": ("Open PowerShell", ["powershell"]),
        "Q": ("Open Control Panel", ["control"]),
        "N": ("Open Notepad", ["notepad"]),
        "B": ("Open default Browser", ["start", ""], True),
        "E": ("Open Explorer", ["explorer"]),
        "M": ("Open Microsoft Store", ["start", "ms-windows-store:"], True),
        "S": ("Open Settings", ["start", "ms-settings:"], True),
        "H": ("Open Hosts file in Notepad", ["notepad", r"C:\Windows\System32\drivers\etc\hosts"]),
        "L": ("Lock Workstation", ["rundll32.exe", "user32.dll,LockWorkStation"]),
        "R": ("Run custom script", ["C:\\path\\to\\yourscript.bat"]),
        "V": ("Open Registry Editor", ["regedit"]),
        "D": ("Open Event Viewer", ["eventvwr.msc"]),
        "K": ("Open Task Scheduler", ["taskschd.msc"]),
        "G": ("Quick Network Test (ping 8.8.8.8)", ["cmd", "/c", "ping 8.8.8.8"]),
        "F": ("Open Paint", ["mspaint"]),
        "A": ("Open Calculator", ["calc"]),
        "Y": ("Search Files", ["explorer", "shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}"]),
        "=": ("Show Tree", None)
    }

    for key, (desc, *_ ) in hotkeys.items():
        print(Fore.GREEN + f"[{key}]" + Style.RESET_ALL + f" - {desc}")
    print()

    tree_text = r""" ... """

    while True:
        choice = input("Choice: ").strip().upper()
        if choice not in hotkeys:
            print("Unknown option")
            continue

        desc, cmd, *rest = hotkeys[choice]
        shell_flag = rest[0] if rest else False

        if choice == "X":
            print("Exiting panel.")
            break
        elif choice == "GM":
            launch_game_panel()
            break
        elif choice == "=":
            print(tree_text)
            continue

        if cmd:
            try:
                subprocess.run(cmd, shell=shell_flag)
            except Exception as e:
                print(f"Failed to run {desc}: {e}")

# -------------------- PACKAGE REFRESH --------------------
def refresh_package():
    try:
        import zenpo
        pkg_dir = os.path.dirname(zenpo.__file__)
        print(f"Refreshing Zenpo in {pkg_dir}...\n")
        subprocess.run(["git", "pull"], cwd=pkg_dir, check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], cwd=pkg_dir, check=True)
        print("\nZenpo has been updated successfully!")
    except Exception as e:
        print(f"Failed to refresh Zenpo: {e}")

# -------------------- MAIN --------------------
def show_main():
    print(ascii_banner("Zenpo"))
    print(Fore.GREEN + f"Creator: {CREATOR}")
    print(Fore.GREEN + f"GitHub Repo: {REPO}\n")
    print(Fore.BLUE + f"Version: {VERSION}\n")
    print(Style.BRIGHT + "Help:")
    print("        zenpo -p\tShow panel with apps to open")
    print("        zenpo -refresh\tUpdate Zenpo to latest GitHub version")
    print("        zenpo\tShow this text")

def main():
    parser = argparse.ArgumentParser(prog="zenpo", add_help=False)
    parser.add_argument("-p", action="store_true", help="Show panel with apps to open")
    parser.add_argument("-refresh", action="store_true", help="Update Zenpo to latest GitHub version")
    args = parser.parse_args()

    if args.refresh:
        refresh_package()
    elif args.p:
        show_panel()
    else:
        show_main()

if __name__ == "__main__":
    main()
