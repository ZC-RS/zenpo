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

# -------------------- FULL GAMES --------------------

# -------------------- Snake --------------------
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
    font = pygame.font.SysFont(None, 36)
    running = True

    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, block): direction = (0, -block)
                if event.key == pygame.K_DOWN and direction != (0, -block): direction = (0, block)
                if event.key == pygame.K_LEFT and direction != (block, 0): direction = (-block, 0)
                if event.key == pygame.K_RIGHT and direction != (-block, 0): direction = (block, 0)

        if direction != (0,0):
            new_head = (snake[0][0]+direction[0], snake[0][1]+direction[1])
            if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
                break
            snake.insert(0,new_head)
            if new_head == food:
                food = (random.randrange(0, WIDTH, block), random.randrange(0, HEIGHT, block))
                score += 1
            else:
                snake.pop()

        screen.fill((0,0,0))
        for s in snake: pygame.draw.rect(screen,(0,255,0), (*s, block, block))
        pygame.draw.rect(screen,(255,0,0), (*food, block, block))
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10,10))
        pygame.display.flip()

    pygame.quit()

# -------------------- Battleship --------------------
def battleship_game():
    pygame.init()
    WIDTH, HEIGHT = 500, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battleship")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    grid_size = 10
    cell = WIDTH//grid_size

    # Mode selection
    print("Battleship Mode:")
    print("[1] Play vs AI")
    print("[2] Play vs Friend")
    mode = input("Choose mode: ").strip()
    if mode not in ['1','2']:
        print("Invalid choice. Returning to panel.")
        return

    # Random ship for player
    def place_ship():
        return [(random.randint(0, grid_size-1), random.randint(0, grid_size-1)) for _ in range(3)]

    player_ship = place_ship()
    if mode=='1':
        ai_ship = place_ship()
        player_hits = []
        ai_hits = []
        ai_guesses = []
    else:
        other_ship = place_ship()
        player1_hits = []
        player2_hits = []
        turn = 1

    running = True
    while running:
        screen.fill((0,0,64))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                gx, gy = x//cell, y//cell

                if mode=='1':
                    # Player guesses AI ship
                    if (gx,gy) in ai_ship and (gx,gy) not in player_hits:
                        player_hits.append((gx,gy))
                    # AI random guess
                    guess = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
                    while guess in ai_guesses: guess = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
                    ai_guesses.append(guess)
                    if guess in player_ship and guess not in ai_hits: ai_hits.append(guess)
                    # Check win
                    if len(player_hits)==len(ai_ship):
                        print("You Win!")
                        running=False
                    if len(ai_hits)==len(player_ship):
                        print("AI Wins!")
                        running=False
                else:
                    if turn==1:
                        if (gx,gy) in other_ship and (gx,gy) not in player1_hits:
                            player1_hits.append((gx,gy))
                        turn=2
                        if len(player1_hits)==len(other_ship):
                            print("Player 1 Wins!")
                            running=False
                    else:
                        if (gx,gy) in player_ship and (gx,gy) not in player2_hits:
                            player2_hits.append((gx,gy))
                        turn=1
                        if len(player2_hits)==len(player_ship):
                            print("Player 2 Wins!")
                            running=False

        # Draw grid
        for i in range(grid_size):
            for j in range(grid_size):
                rect = pygame.Rect(i*cell, j*cell, cell, cell)
                pygame.draw.rect(screen,(0,128,128),rect,1)
                if mode=='1':
                    if (i,j) in player_hits: pygame.draw.rect(screen,(0,255,0),rect)
                    if (i,j) in ai_hits: pygame.draw.rect(screen,(255,0,0),rect)
                else:
                    if (i,j) in player1_hits: pygame.draw.rect(screen,(0,255,0),rect)
                    if (i,j) in player2_hits: pygame.draw.rect(screen,(255,0,0),rect)

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

# -------------------- Tetris (Basic playable) --------------------
def tetris_game():
    pygame.init()
    WIDTH, HEIGHT = 200, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # Simple falling blocks
    block_size = 20
    grid_w = WIDTH//block_size
    grid_h = HEIGHT//block_size
    grid = [[0]*grid_w for _ in range(grid_h)]

    # Pieces
    pieces = [
        [[1,1,1,1]],
        [[1,1],[1,1]],
        [[0,1,0],[1,1,1]],
        [[1,0,0],[1,1,1]],
        [[0,0,1],[1,1,1]],
        [[1,1,0],[0,1,1]],
        [[0,1,1],[1,1,0]]
    ]

    current_piece = random.choice(pieces)
    piece_x, piece_y = grid_w//2-1,0

    def can_move(px,py,shape):
        for y,row in enumerate(shape):
            for x,v in enumerate(row):
                if v:
                    gx,gy = px+x, py+y
                    if gx<0 or gx>=grid_w or gy>=grid_h or grid[gy][gx]:
                        return False
        return True

    def place_piece(px,py,shape):
        for y,row in enumerate(shape):
            for x,v in enumerate(row):
                if v:
                    grid[py+y][px+x]=1

    running = True
    drop_counter = 0
    drop_speed = 10
    while running:
        clock.tick(30)
        drop_counter +=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running=False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and can_move(piece_x-1,piece_y,current_piece): piece_x-=1
                if event.key == pygame.K_RIGHT and can_move(piece_x+1,piece_y,current_piece): piece_x+=1
                if event.key == pygame.K_DOWN and can_move(piece_x,piece_y+1,current_piece): piece_y+=1
                if event.key == pygame.K_UP:
                    rotated = [list(row) for row in zip(*current_piece[::-1])]
                    if can_move(piece_x,piece_y,rotated): current_piece=rotated

        if drop_counter>=drop_speed:
            if can_move(piece_x,piece_y+1,current_piece):
                piece_y+=1
            else:
                place_piece(piece_x,piece_y,current_piece)
                current_piece = random.choice(pieces)
                piece_x,piece_y = grid_w//2-1,0
                # Clear lines
                grid=[row for row in grid if any(v==0 for v in row)]
                while len(grid)<grid_h:
                    grid.insert(0,[0]*grid_w)
            drop_counter=0

        screen.fill((0,0,0))
        for y,row in enumerate(grid):
            for x,v in enumerate(row):
                if v: pygame.draw.rect(screen,(0,255,255),(x*block_size,y*block_size,block_size,block_size))
        for y,row in enumerate(current_piece):
            for x,v in enumerate(row):
                if v: pygame.draw.rect(screen,(255,0,255),((piece_x+x)*block_size,(piece_y+y)*block_size,block_size,block_size))
        pygame.display.flip()
    pygame.quit()

# -------------------- Minesweeper (Basic playable) --------------------
def minesweeper_game():
    pygame.init()
    WIDTH, HEIGHT = 400, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    grid_size = 8
    cell = WIDTH//grid_size
    mines = [(random.randint(0,grid_size-1), random.randint(0,grid_size-1)) for _ in range(10)]
    revealed = []
    flags = []

    def count_adjacent(x,y):
        return sum((nx,ny) in mines for nx in range(x-1,x+2) for ny in range(y-1,y+2))

    running = True
    while running:
        screen.fill((192,192,192))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                gx,gy = mx//cell,my//cell
                if event.button==1:
                    if (gx,gy) in mines:
                        print("Game Over!")
                        running=False
                    else:
                        revealed.append((gx,gy))
                elif event.button==3:
                    if (gx,gy) not in flags: flags.append((gx,gy))
                    else: flags.remove((gx,gy))

        for i in range(grid_size):
            for j in range(grid_size):
                rect = pygame.Rect(i*cell,j*cell,cell,cell)
                pygame.draw.rect(screen,(0,0,0),rect,1)
                if (i,j) in revealed:
                    adj = count_adjacent(i,j)
                    pygame.draw.rect(screen,(200,200,200),rect)
                    text = font.render(str(adj),True,(0,0,0))
                    screen.blit(text,(i*cell+5,j*cell+5))
                elif (i,j) in flags:
                    pygame.draw.rect(screen,(255,0,0),rect)

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

# -------------------- Hangman --------------------
def hangman_game():
    pygame.init()
    WIDTH, HEIGHT = 400, 300
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hangman")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    words = ["python","zenpo","hangman","developer","terminal"]
    word = random.choice(words)
    guessed = set()
    incorrect = 0
    running = True

    while running:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            elif event.type==pygame.KEYDOWN:
                ch = event.unicode.lower()
                if ch.isalpha() and ch not in guessed:
                    guessed.add(ch)
                    if ch not in word: incorrect+=1

        display_word = " ".join([c if c in guessed else "_" for c in word])
        text = font.render(display_word, True, (0,0,0))
        screen.blit(text,(50,HEIGHT//2-20))
        text2 = font.render(f"Incorrect: {incorrect}", True,(255,0,0))
        screen.blit(text2,(50,HEIGHT//2+20))
        if incorrect>=6:
            text3 = font.render("You Lost!", True,(255,0,0))
            screen.blit(text3,(50,HEIGHT//2+60))
        if all(c in guessed for c in word):
            text3 = font.render("You Won!", True,(0,255,0))
            screen.blit(text3,(50,HEIGHT//2+60))

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

# -------------------- 2048 --------------------
def game_2048():
    pygame.init()
    WIDTH, HEIGHT = 400, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None,36)

    grid = [[0]*4 for _ in range(4)]

    def add_new():
        empty=[(i,j) for i in range(4) for j in range(4) if grid[i][j]==0]
        if empty:
            i,j=random.choice(empty)
            grid[i][j]=2 if random.random()<0.9 else 4

    def merge_left(row):
        new=[i for i in row if i!=0]
        for i in range(len(new)-1):
            if new[i]==new[i+1]:
                new[i]*=2
                new[i+1]=0
        new=[i for i in new if i!=0]
        while len(new)<4: new.append(0)
        return new

    add_new()
    add_new()
    running=True
    while running:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            elif event.type==pygame.KEYDOWN:
                moved=False
                if event.key==pygame.K_LEFT:
                    for i in range(4): grid[i]=merge_left(grid[i])
                    moved=True
                elif event.key==pygame.K_RIGHT:
                    for i in range(4): grid[i]=merge_left(grid[i][::-1])[::-1]
                    moved=True
                elif event.key==pygame.K_UP:
                    grid=list(map(list,zip(*grid)))
                    for i in range(4): grid[i]=merge_left(grid[i])
                    grid=list(map(list,zip(*grid)))
                    moved=True
                elif event.key==pygame.K_DOWN:
                    grid=list(map(list,zip(*grid)))
                    for i in range(4): grid[i]=merge_left(grid[i][::-1])[::-1]
                    grid=list(map(list,zip(*grid)))
                    moved=True
                if moved: add_new()

        for i in range(4):
            for j in range(4):
                rect=pygame.Rect(j*100,i*100,100,100)
                pygame.draw.rect(screen,(200,200,200),rect)
                if grid[i][j]:
                    text=font.render(str(grid[i][j]),True,(0,0,0))
                    screen.blit(text,(j*100+35,i*100+35))
                pygame.draw.rect(screen,(0,0,0),rect,2)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

# -------------------- Game Panel ------------------------------------------
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

# -------------------- Control Panel ----------------------------------------------------------------------------------------------------
def show_panel():
    print(ascii_banner("PANEL"))
    print(Fore.LIGHTBLUE_EX + "A general control panel for apps\n")
    print("Press different keys to open apps:\n")

    hotkeys = {
        "GM": ("Interactive Game Mode [V2-BETA]", None),
        "W": ("Send Message [NEW]", None),
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
        "R": ("Run custom script [NOT FUNCTIONAL]", ["C:\\path\\to\\yourscript.bat"]),
        "V": ("Open Registry Editor", ["regedit"]),
        "D": ("Open Event Viewer", ["eventvwr.msc"]),
        "K": ("Open Task Scheduler", ["taskschd.msc"]),
        "G": ("Quick Network Test (ping 8.8.8.8)", ["cmd", "/c", "ping 8.8.8.8"]),
        "F": ("Open Paint", ["mspaint"]),
        "A": ("Open Calculator", ["calc"]),
        "Y": ("Search Files", ["explorer", "shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}"]),
        "=": ("Credits", None)
    }

    for key, (desc, *_ ) in hotkeys.items():
        print(Fore.GREEN + f"[{key}]" + Style.RESET_ALL + f" - {desc}")
    print()

    tree_text = r"""
==================== ZENPO CREDITS ====================

Creator: Zenpo (a00137)
GitHub Repo: https://github.com/ZC-RS/zenpo

Installation:
pip install zenpo       [CURRENT]
pip install phazegod    [BETA]
pip install drizzydrake [COMING]

Email any suggestions to: zenpo.a00137@gmail.com

========================================================
"""


    while True:
        choice = input("Choice: ").strip().upper()
        if choice not in hotkeys:
            print("Unknown option")
            continue

        desc, cmd, *rest = hotkeys[choice]
        shell_flag = rest[0] if rest else False

        if choice == "W":
        whatsapp_message()
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

# -------------------- Refresh --------------------
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

# -------------------- WhatsApp Messaging --------------------
def whatsapp_message():
    print("=== WhatsApp Messaging Feature ===")
    phone = input("Enter recipient phone number (with country code): ")
    msg = input("Enter message to send: ")
    print(f"Simulating sending WhatsApp message to {phone}: {msg}")
    # Here you could integrate pywhatkit or another library
    try:
        import pywhatkit
        pywhatkit.sendwhatmsg_instantly(phone, msg)
        print("Message sent!")
    except Exception as e:
        print(f"Failed to send message: {e}")
