#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from pyfiglet import Figlet
from colorama import init, Fore, Style

init(autoreset=True)

VERSION = "2.0.0"
CREATOR = "Zenpo"
REPO = "https://github.com/ZC-RS/zenpo"

def ascii_banner(text, colour=Fore.GREEN):
    f = Figlet(font='slant')
    return colour + f.renderText(text)

def show_main():
    print(ascii_banner("Zenpo"))
    print(Fore.GREEN + f"Creator: {CREATOR}")
    print(Fore.GREEN + f"GitHub Repo: {REPO}\n")
    print(Fore.BLUE + f"Version: {VERSION}\n")
    print(Style.BRIGHT + "Help:")
    print("        zenpo -p\tShow panel with apps to open")
    print("        zenpo -refresh\tUpdate Zenpo to latest GitHub version")
    print("        zenpo\tShow this text")

# -------------------- Game Panel --------------------
def launch_game_panel():
    print(ascii_banner("Games [V2]"))
    print(Fore.BLUE + Style.BRIGHT + "Version 2 - Script by a00137\n")
    print("A game console in the terminal for students to play without a history :)\n")
    print("[B] Battleship")
    print("[S] Snake")
    print("[T] Tetris")
    print("[M] Minesweeper")
    print("[H] Hangman")
    print("[2] 2048\n")

    choice = input("Choice: ").strip().lower()
    if choice == "b":
        battleship()
    elif choice == "s":
        snake()
    elif choice == "t":
        tetris()
    elif choice == "m":
        minesweeper()
    elif choice == "h":
        hangman()
    elif choice == "2":
        game_2048()
    else:
        print("Unknown choice or not implemented yet!")

# -------------------- Placeholder Games --------------------
def battleship():
    print(ascii_banner("Battleship", Fore.CYAN))
    print("Two-player game: place ships and guess coordinates.")
    input("Press Enter to return to the game panel...")

def snake():
    print(ascii_banner("Snake", Fore.YELLOW))
    print("Move around, eat food, grow longer, die if you hit walls or yourself.")
    input("Press Enter to return to the game panel...")

def tetris():
    print(ascii_banner("Tetris", Fore.MAGENTA))
    print("Falling blocks, rotate with keys, clear lines, classic fun!")
    input("Press Enter to return to the game panel...")

def minesweeper():
    print(ascii_banner("Minesweeper", Fore.RED))
    print("Grid of numbers and mines. Flag mines and uncover tiles.")
    input("Press Enter to return to the game panel...")

def hangman():
    print(ascii_banner("Hangman", Fore.GREEN))
    print("Guess letters of a hidden word. Easy to scale difficulty.")
    input("Press Enter to return to the game panel...")

def game_2048():
    print(ascii_banner("2048", Fore.BLUE))
    print("Merge numbers on a grid using arrow keys. Fun in ASCII!")
    input("Press Enter to return to the game panel...")

# -------------------- Control Panel --------------------
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

    tree_text = r""" ... """  # keep existing tree if needed

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

# -------------------- Package Refresh --------------------
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

# -------------------- Main --------------------
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
