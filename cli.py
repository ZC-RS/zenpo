#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from pyfiglet import Figlet
from colorama import init, Fore, Style

init(autoreset=True)

VERSION = "1.2.3"
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
    print("  -refresh\tUpdate Zenpo to latest GitHub version")
    print("  zenpo\tShow this text")

def show_panel():
    print(ascii_banner("PANEL"))
    print(Fore.LIGHTBLUE_EX + "A general control panel for apps\n")
    print("Press different keys to open apps:\n")

    hotkeys = {
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
        "Y": ("Search Files", ["explorer", "shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}"])
    }

    for key, (desc, *_ ) in hotkeys.items():
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

def refresh_package():
    try:
        # Locate the package folder
        import zenpo
        pkg_dir = os.path.dirname(zenpo.__file__)
        print(f"Refreshing Zenpo in {pkg_dir}...\n")
        # Pull latest from GitHub
        subprocess.run(["git", "pull"], cwd=pkg_dir, check=True)
        # Reinstall editable package
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], cwd=pkg_dir, check=True)
        print("\nZenpo has been updated successfully!")
    except Exception as e:
        print(f"Failed to refresh Zenpo: {e}")

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
