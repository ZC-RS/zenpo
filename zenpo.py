#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
import random
import time
from pyfiglet import Figlet
from colorama import init, Fore, Style

init(autoreset=True)

VERSION = "2.2.0"
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

# -------------------- GAME PANEL --------------------
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
        print("Unknown choice!")

# -------------------- BATTLESHIP --------------------
def battleship():
    print(ascii_banner("Battleship", Fore.CYAN))
    size = 5
    player_board = [['~']*size for _ in range(size)]
    ai_board = [['~']*size for _ in range(size)]

    def print_board(board, hide_ships=False):
        print("  " + " ".join(str(i) for i in range(size)))
        for y, row in enumerate(board):
            display_row = []
            for x, cell in enumerate(row):
                if hide_ships and cell == "S":
                    display_row.append("~")
                else:
                    display_row.append(cell)
            print(str(y) + " " + " ".join(display_row))

    def place_ship(board):
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        board[y][x] = "S"
        return (x, y)

    ai_ship = place_ship(ai_board)
    player_ship = place_ship(player_board)

    print("Your board:")
    print_board(player_board)
    print("\nAttack the AI ship!")

    while True:
        # Player turn
        try:
            coords = input("Enter attack coordinates x y: ").split()
            if len(coords) != 2: continue
            x, y = map(int, coords)
            if ai_board[y][x] == "S":
                print("Hit! You sunk the AI's ship! 🎉")
                break
            else:
                print("Miss!")
                ai_board[y][x] = "X"
        except:
            print("Invalid input.")

        # AI turn
        while True:
            ai_x, ai_y = random.randint(0, size-1), random.randint(0, size-1)
            if player_board[ai_y][ai_x] not in ["X", "H"]:
                if player_board[ai_y][ai_x] == "S":
                    print(f"AI hit your ship at ({ai_x},{ai_y})! You lost! 💥")
                    return
                else:
                    player_board[ai_y][ai_x] = "X"
                    print(f"AI missed at ({ai_x},{ai_y})")
                    break

        print("Current player board:")
        print_board(player_board)

# -------------------- SNAKE --------------------
def snake():
    print(ascii_banner("Snake", Fore.YELLOW))
    import curses

    def play(stdscr):
        curses.curs_set(0)
        h, w = 20, 40
        win = curses.newwin(h, w, 0, 0)
        win.keypad(1)
        win.timeout(100)

        snk_x = w//4
        snk_y = h//2
        snake = [[snk_y, snk_x]]
        food = [h//2, w//2]
        win.addch(food[0], food[1], curses.ACS_PI)

        key = curses.KEY_RIGHT
        score = 0

        while True:
            next_key = win.getch()
            key = key if next_key == -1 else next_key

            head = snake[-1][:]
            if key == curses.KEY_DOWN: head[0] += 1
            if key == curses.KEY_UP: head[0] -= 1
            if key == curses.KEY_LEFT: head[1] -= 1
            if key == curses.KEY_RIGHT: head[1] += 1

            if head in snake or head[0] in [0, h-1] or head[1] in [0, w-1]:
                msg = f"GAME OVER! Score: {score}"
                win.addstr(h//2, w//2 - len(msg)//2, msg)
                win.refresh()
                win.getch()
                break

            snake.append(head)
            if head == food:
                score += 1
                food = None
                while food is None:
                    nf = [random.randint(1, h-2), random.randint(1, w-2)]
                    food = nf if nf not in snake else None
                win.addch(food[0], food[1], curses.ACS_PI)
            else:
                tail = snake.pop(0)
                win.addch(tail[0], tail[1], ' ')

            win.addch(head[0], head[1], curses.ACS_CKBOARD)

    curses.wrapper(play)

# -------------------- TETRIS --------------------
def tetris():
    print(ascii_banner("Tetris", Fore.MAGENTA))
    print("Play Tetris using w/a/s/d (ASCII version)")
    import curses

    shapes = [
        [[1,1,1,1]],       # I
        [[1,1],[1,1]],     # O
        [[0,1,0],[1,1,1]], # T
        [[1,1,0],[0,1,1]], # S
        [[0,1,1],[1,1,0]]  # Z
    ]

    def rotate(shape):
        return [list(row)[::-1] for row in zip(*shape)]

    def play(stdscr):
        curses.curs_set(0)
        h, w = 20, 10
        board = [[0]*w for _ in range(h)]
        key = -1
        current_shape = random.choice(shapes)
        x, y = w//2-len(current_shape[0])//2, 0

        def draw():
            stdscr.clear()
            for r in range(h):
                for c in range(w):
                    if board[r][c]:
                        stdscr.addstr(r, c*2, "[]")
            for r in range(len(current_shape)):
                for c in range(len(current_shape[0])):
                    if current_shape[r][c]:
                        if 0<=y+r<h and 0<=x+c<w:
                            stdscr.addstr(y+r, (x+c)*2, "[]")
            stdscr.refresh()

        while True:
            draw()
            time.sleep(0.2)
            new_y = y+1
            collision = False
            for r in range(len(current_shape)):
                for c in range(len(current_shape[0])):
                    if current_shape[r][c]:
                        if new_y+r>=h or board[new_y+r][x+c]:
                            collision = True
            if collision:
                for r in range(len(current_shape)):
                    for c in range(len(current_shape[0])):
                        if current_shape[r][c]:
                            board[y+r][x+c] = 1
                current_shape = random.choice(shapes)
                x, y = w//2-len(current_shape[0])//2, 0
                if any(board[0]):
                    stdscr.addstr(h//2, 0, "GAME OVER")
                    stdscr.getch()
                    break
            else:
                y += 1

            try:
                key = stdscr.getch()
                if key == ord('a'): x-=1
                if key == ord('d'): x+=1
                if key == ord('s'): y+=1
                if key == ord('w'): current_shape = rotate(current_shape)
            except:
                pass

    curses.wrapper(play)

# -------------------- MINESWEEPER --------------------
def minesweeper():
    print(ascii_banner("Minesweeper", Fore.RED))
    size = 5
    mines = [(random.randint(0,size-1), random.randint(0,size-1)) for _ in range(3)]
    board = [[' ']*size for _ in range(size)]

    def print_board():
        print("  " + " ".join(str(i) for i in range(size)))
        for idx, row in enumerate(board):
            print(str(idx) + " " + " ".join(row))

    while True:
        print_board()
        move = input("Enter coordinates x y: ").split()
        if len(move) != 2: continue
        x, y = map(int, move)
        if (x,y) in mines:
            print("BOOM! You hit a mine 💥")
            break
        else:
            board[y][x] = '0'
        if all(board[y][x]!=' ' for y in range(size) for x in range(size) if (x,y) not in mines):
            print("You cleared the board! 🎉")
            break

# -------------------- HANGMAN --------------------
def hangman():
    print(ascii_banner("Hangman", Fore.GREEN))
    words = ["python","terminal","zenpo","hangman","battleship","snake"]
    word = random.choice(words)
    guessed = set()
    attempts = 6

    while attempts > 0:
        display = [c if c in guessed else '_' for c in word]
        print(" ".join(display))
        if '_' not in display:
            print("You won! 🎉")
            break
        guess = input("Guess a letter: ").lower()
        if guess in guessed: continue
        if guess in word:
            guessed.add(guess)
        else:
            guessed.add(guess)
            attempts -= 1
            print(f"Wrong! Attempts left: {attempts}")
    if attempts == 0:
        print(f"You lost! The word was: {word}")

# -------------------- 2048 --------------------
def game_2048():
    print(ascii_banner("2048", Fore.BLUE))
    size = 4
    board = [[0]*size for _ in range(size)]

    def add_tile():
        empty = [(r,c) for r in range(size) for c in range(size) if board[r][c]==0]
        if empty:
            r,c = random.choice(empty)
            board[r][c] = 2 if random.random()<0.9 else 4

    def print_board():
        for row in board:
            print("\t".join(str(num) if num!=0 else '.' for num in row))
        print()

    def move_left():
        changed = False
        for r in range(size):
            new_row = [i for i in board[r] if i!=0]
            for i in range(len(new_row)-1):
                if new_row[i]==new_row[i+1]:
                    new_row[i]*=2
                    new_row[i+1]=0
            new_row = [i for i in new_row if i!=0]
            new_row += [0]*(size-len(new_row))
            if new_row != board[r]:
                changed = True
                board[r] = new_row
        return changed

    def rotate():
        return [list(x)[::-1] for x in zip(*board)]

    add_tile()
    add_tile()
    while True:
        print_board()
        move = input("Move (w/a/s/d): ").lower()
        changed = False
        if move=='a': changed = move_left()
        elif move=='d': board[:] = rotate(rotate(board)); changed = move_left(); board[:] = rotate(rotate(board))
        elif move=='w': board[:] = rotate(board); changed = move_left(); board[:] = rotate(rotate(rotate(board)))
        elif move=='s': board[:] = rotate(rotate(rotate(board))); changed = move_left(); board[:] = rotate(board)
        else: print("Invalid move"); continue
        if changed: add_tile()
        if any(2048 in row for row in board): print_board(); print("You reached 2048! 🎉"); break
        if all(board[r][c]!=0 for r in range(size) for c in range(size)) and not any(
            board[r][c]==board[r][c+1] for r in range(size) for c in range(size-1)
        ) and not any(board[r][c]==board[r+1][c] for r in range(size-1) for c in range(size)):
            print_board()
            print("Game Over!")
            break
    input("Press Enter to return...")

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


# -------------------- REFRESH --------------------
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
def main():
    parser = argparse.ArgumentParser(prog="zenpo", add_help=False)
    parser.add_argument("-p", action="store_true", help="Show panel with apps")
    parser.add_argument("-refresh", action="store_true", help="Update Zenpo")
    args = parser.parse_args()

    if args.refresh:
        refresh_package()
    elif args.p:
        show_panel()
    else:
        show_main()

if __name__ == "__main__":
    main()
