#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pyfiglet import Figlet
from colorama import init, Fore, Style

init(autoreset=True)

VERSION = "1.0.0"
CREATOR = "Zenpo"
REPO = "https://github.com/ZC-RS/zenpo"

def ascii_banner(text, colour=Fore.GREEN):
    f = Figlet(font='slant')
    return colour + f.renderText(text)

def show_main():
    print(ascii_banner("a00137"))
    print(Fore.GREEN + f"Creator: {CREATOR}")
    print(Fore.GREEN + f"GitHub Repo: {REPO}\n")
    print(Fore.BLUE + f"Version: {VERSION}\n")
    print(Style.BRIGHT + "Help:")
    print("  -p\tShow panel with apps to open")
    print("  zenpo\tShow this text")
    # add more help lines here as needed

def show_panel():
    print(ascii_banner("PANEL"))
    print(Fore.LIGHTBLUE_EX + "A general control panel for apps\n")
    print("Press different keys to open apps:\n")

    # Hotkeys mapped to (description, command list)
    hotkeys = {
        "X": ("Exit the panel", None),
        "T": ("Open Task Manager", ["taskmgr"]),
        "C": ("Open CMD", ["cmd"]),
        "P": ("Open PowerShell", ["powershell"]),
        "Q": ("Open Control Panel", ["control"]),
        "N": ("Open Notepad", ["notepad"]),
        "B": ("Open default Browser", ["start", ""], True),  # needs shell=True
        "E": ("Open Explorer", ["explorer"]),
        "M": ("Open Microsoft Store", ["ms-windows-store:"]),  # URI
        "S": ("Open Settings", ["start", "ms-settings:"], True),
        "H": ("Open Hosts file in Notepad", ["notepad", r"C:\Windows\System32\drivers\etc\hosts"]),
        "L": ("Lock Workstation", ["rundll32.exe", "user32.dll,LockWorkStation"]),
        "R": ("Run custom script", ["C:\\path\\to\\yourscript.bat"])
    }

    # Display menu dynamically
    for key, (desc, cmd, *rest) in hotkeys.items():
        print(Fore.GREEN + f"[{key}]" + Style.RESET_ALL + f" - {desc}")
    print()

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

        if cmd:
            try:
                subprocess.run(cmd, shell=shell_flag)
            except Exception as e:
                print(f"Failed to run {desc}: {e}")

def main():
    parser = argparse.ArgumentParser(prog="zenpo", add_help=False)
    parser.add_argument("-p", action="store_true", help="Show panel with apps to open")
    args = parser.parse_args()

    if args.p:
        show_panel()
    else:
        show_main()

if __name__ == "__main__":
    main()
