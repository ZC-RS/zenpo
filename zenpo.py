#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
import pygame
from pyfiglet import Figlet
from colorama import init, Fore, Style

init(autoreset=True)

VERSION = "1.2.6"
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
    print(ascii_banner("Games [BETA]"))
    print(Fore.BLUE + Style.BRIGHT + "Version 1 - Script by a00137\n")
    print("A game console in the terminal for students to play without a history :)\n")
    print("[S] Space Shooting Game 🚀 [W.I.P]")
    print("[A] Among Us [SUS]")
    print("[I] Interactive Chat 💬 [ALPHA]\n")

    choice = input("Choice: ").strip().lower()
    if choice == "s":
        space_shooting_game()
    else:
        print("Coming soon or not implemented yet!")

def space_shooting_game():
    import pygame
    import random
    print("Launching Space Shooting Game 🚀 (Press {Ctrl + C} to quit)\n")
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Shooting Game 🚀 [W.I.P]")
    clock = pygame.time.Clock()

    class Player:
        def __init__(self):
            self.x = WIDTH // 2
            self.y = HEIGHT - 50
            self.speed = 5
            self.health = 100
            self.shield = 50
            self.width = 40
            self.height = 40

        def move(self, keys):
            if keys[pygame.K_LEFT]: self.x -= self.speed
            if keys[pygame.K_RIGHT]: self.x += self.speed
            self.x = max(0, min(self.x, WIDTH - self.width))

        def draw(self):
            pygame.draw.rect(screen, (0, 150, 255), (self.x, self.y, self.width, self.height))

        def take_damage(self, amount):
            if self.shield > 0:
                block = min(self.shield, amount)
                self.shield -= block
                amount -= block
            self.health -= amount

    class Bullet:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.speed = 7
            self.width = 5
            self.height = 10

        def update(self):
            self.y -= self.speed

        def draw(self):
            pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, self.width, self.height))

        def off_screen(self):
            return self.y < 0

    class Enemy:
        def __init__(self, x, y, health=2):
            self.x = x
            self.y = y
            self.speed = 1 + random.random()
            self.health = health
            self.width = 30
            self.height = 30

        def update(self):
            self.y += self.speed

        def draw(self):
            pygame.draw.rect(screen, (255, 50, 50), (self.x, self.y, self.width, self.height))

        def hits_player(self, player):
            return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(
                pygame.Rect(player.x, player.y, player.width, player.height)
            )

        def hits_bullet(self, bullet):
            return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(
                pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
            )

    player = Player()
    bullets = []
    enemies = [Enemy(random.randint(0, WIDTH-30), random.randint(-100, 0)) for _ in range(5)]
    wave = 1
    score = 0
    spawn_delay = 120
    frame_counter = 0

    running = True
    while running:
        clock.tick(60)
        screen.fill((30, 30, 30))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.x + player.width // 2, player.y))

        player.move(keys)
        player.draw()

        for b in bullets[:]:
            b.update()
            b.draw()
            if b.off_screen():
                bullets.remove(b)

        for e in enemies[:]:
            e.update()
            e.draw()

            for b in bullets[:]:
                if e.hits_bullet(b):
                    e.health -= 1
                    bullets.remove(b)
                    if e.health <= 0:
                        enemies.remove(e)
                        score += 10
                    break

            if e.hits_player(player):
                player.take_damage(5)
                enemies.remove(e)

        if not enemies and frame_counter > spawn_delay:
            wave += 1
            enemies = [Enemy(random.randint(0, WIDTH-30), random.randint(-100, 0), health=wave) for _ in range(5 + wave)]
            frame_counter = 0

        frame_counter += 1

        font = pygame.font.SysFont(None, 24)
        screen.blit(font.render(f"Health: {player.health}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Shield: {player.shield}", True, (255, 255, 255)), (10, 30))
        screen.blit(font.render(f"Score: {score}  Wave: {wave}", True, (0, 191, 255)), (10, 50))

        if player.health <= 0:
            screen.blit(font.render("GAME OVER", True, (255, 0, 0)), (WIDTH // 2 - 50, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()

    pygame.quit()
    print("Game exited. Returning to Zenpo panel...")

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

    tree_text = r""" ... """  # (keep your existing tree_text here)

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
