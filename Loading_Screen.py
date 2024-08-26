import pygame
import threading

pygame.init()

load_screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Please wait while the game is loading')

clock = pygame.time.Clock()

load_bg = pygame.image.load('bar_bg.png')
load_bg_rect = load_bg.get_rect(center=(400, 300))

load_bar = pygame.image.load('bar_bar.png')
load_bar_rect = load_bar.get_rect(midleft=(10, 300))
loading_finished = False
loading_progress = 0
load_bar_width = 8


def run_game():
    global loading_finished
    code_file = open('Game Code.py', 'r')
    game = code_file.read()
    print("before")
    exec(game)
    print("after")
    loading_finished = True


threading.Thread(target=run_game).start()

running = True
while running:
    load_screen.fill((240, 200, 250))

    if not loading_finished:
        for i in range(1, 10):
            load_bar_width = i / 10 * 741

            load_bar = pygame.transform.scale(load_bar, (int(load_bar_width), 180))
            load_bar_rect = load_bar.get_rect(midleft=(30, 300))
            load_screen.blit(load_bg, load_bg_rect)
            load_screen.blit(load_bar, load_bar_rect)

    else:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(30)
pygame.quit()