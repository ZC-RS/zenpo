#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from pyfiglet import Figlet
from colorama import init, Fore, Style

init(autoreset=True)

VERSION = "1.2.5"
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

def launch_game_panel():
    print(ascii_banner("Games V1"))
    print(Fore.BLUE + Style.BRIGHT + "Version 1.0 - Script by a00137\n")
    print("A game console in the terminal for students to play without a history :)\n")
    print("[S] Space Shooting Game 🚀 [W.I.P]")
    print("[A] Among Us [SUS]")
    print("[I] Interactive Chat 💬 [ALPHA]; Chat with other people on your network, using zenpo!\n")

    choice = input("Choice: ").strip().lower()
    if choice == "s":
        space_shooting_game()
    else:
        print("Coming soon or not implemented yet!")

def space_shooting_game():
    import curses
    import random
    import time

    def main(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        sh, sw = stdscr.getmaxyx()
        player_x, player_y = sw//2, sh-2
        bullets = []
        enemies = [{"x": random.randint(1, sw-2), "y": 1, "health": 2} for _ in range(5)]
        score = 0
        wave = 1

        while True:
            stdscr.clear()
            key = stdscr.getch()

            if key == curses.KEY_LEFT and player_x > 1:
                player_x -= 1
            elif key == curses.KEY_RIGHT and player_x < sw-2:
                player_x += 1
            elif key == ord(" "):
                bullets.append({"x": player_x, "y": player_y-1})

            for b in bullets[:]:
                b["y"] -= 1
                if b["y"] < 0:
                    bullets.remove(b)

            for e in enemies[:]:
                e["y"] += 0.1
                for b in bullets:
                    if int(b["x"]) == int(e["x"]) and int(b["y"]) == int(e["y"]):
                        e["health"] -= 1
                        if b in bullets:
                            bullets.remove(b)
                        if e["health"] <= 0:
                            enemies.remove(e)
                            score += 10
                        break
                if int(e["x"]) == player_x and int(e["y"]) == player_y:
                    stdscr.addstr(sh//2, sw//2-5, "GAME OVER", curses.A_BOLD)
                    stdscr.refresh()
                    time.sleep(2)
                    return

            if not enemies:
                wave += 1
                enemies = [{"x": random.randint(1, sw-2), "y": 1, "health": wave} for _ in range(5 + wave)]

            stdscr.addstr(player_y, player_x, "^")
            for b in bullets:
                stdscr.addstr(int(b["y"]), int(b["x"]), "|")
            for e in enemies:
                stdscr.addstr(int(e["y"]), int(e["x"]), "V")

            stdscr.addstr(0, 2, f"Score: {score} Wave: {wave}")
            stdscr.refresh()
            time.sleep(0.05)

    curses.wrapper(main)

def show_panel():
    print(ascii_banner("PANEL"))
    print(Fore.LIGHTBLUE_EX + "A general control panel for apps\n")
    print("Press different keys to open apps:\n")

    hotkeys = {
        "GM": ("Interactive Game Mode [BETA]", None),
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

    tree_text = r"""
C:\
└── users
    ├── a00157
    │   ├── year 7 project
    │   │   ├── intro.docx
    │   │   ├── experiment_photos.jpg
    │   │   └── results.xlsx
    │   ├── science club photos
    │   │   ├── lab1.png
    │   │   └── lab2.png
    │   └── coding practice
    │       ├── hello_world.py
    │       └── arrays_task.py
    ├── a00123
    │   ├── year 9 rowing
    │   │   ├── team_list.pdf
    │   │   └── timings.csv
    │   └── sports kit list
    │       └── checklist.docx
    ├── b00115
    │   ├── year 8 bandlab
    │   │   ├── chorus.mp3
    │   │   └── mixdown.wav
    │   └── guitar tabs
    │       └── chords.txt
    ├── b00184
    │   ├── year 7 project
    │   │   ├── plan.docx
    │   │   └── diagram.png
    │   └── maths challenge
    │       └── answers.pdf
    ├── x00119
    │   ├── year X subjects (all subjects)
    │   │   ├── maths.docx
    │   │   ├── history.docx
    │   │   └── science.docx
    │   └── programming club 2024
    │       └── scratch_game.sb3
    ├── x00147
    │   ├── year 8 bandlab
    │   │   ├── song1.wav
    │   │   ├── bassline.mp3
    │   │   └── lyrics.txt
    ├── y00142
    │   ├── year 9 rowing
    │   │   ├── regatta_schedule.pdf
    │   │   ├── training_log.xlsx
    │   │   └── safety_rules.docx
    ├── y00133
    │   ├── year 7 project
    │   │   ├── outline.docx
    │   │   ├── poster.png
    │   │   └── bibliography.docx
    │   └── sketches
    │       ├── sketch1.jpg
    │       └── sketch2.jpg
    ├── z00173
    │   ├── year 8 bandlab
    │   │   ├── riff.wav
    │   │   ├── vocal_take.mp3
    │   │   └── notes.txt
    ├── z00158
    │   ├── year X subjects (all subjects)
    │   │   ├── english.docx
    │   │   ├── chemistry.docx
    │   │   └── art.docx
    │   └── python scripts
    │       ├── calculator.py
    │       └── quiz.py
    ├── u00177
    │   ├── year 7 project
    │   │   ├── hypothesis.docx
    │   │   ├── experiment.jpg
    │   │   └── conclusion.docx
    ├── u00124
    │   ├── year 9 rowing
    │   │   ├── practice_videos.mp4
    │   │   └── kit_checklist.docx
    ├── gareth
    │   ├── audit logs
    │   │   ├── 2024.txt
    │   │   └── flip
    |   |   └── 2025.txt
    │   └── others
    │       └── zenpo_plan.txt
    ├── garethbuild
    │   ├── year X subjects (all subjects)
    │   │   ├── maths.docx
    │   │   ├── physics.docx
    │   │   └── dt.docx
    │   ├── CAD designs
    │   │   ├── chassis.stl
    │   │   └── arm.stl
    │   └── maker fair entry
    │       ├── entry_form.pdf
    │       └── photos.png
    ├── admin
    │   ├── system scripts
    │   │   ├── backup.ps1
    │   │   └── cleanup.bat
    │   ├── staff-only policies
    │   │   └── policy2024.pdf
    │   └── backups
    │       ├── backup1.zip
    │       └── backup2.zip
    └── administrator
        ├── root-settings
        │   ├── registry.reg
        │   └── network.cfg
        ├── audits
        │   └── audit2024.pdf
        ├── security logs
        │   ├── log1.txt
        │   └── log2.txt
        ├── logon
        │   ├── intro.docx
        │   └── draft.docx
        └── network configs
            ├── router.conf
            └── firewall.rules
"""

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
