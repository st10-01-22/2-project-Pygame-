import pygame
import sys
from art import tprint
import os


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('test1.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    size = width, height = 1500, 700
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    barriers_group = pygame.sprite.Group()
    player = None
    FPS = 50
    pygame.init()
    running = True
    start_screen()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        player_group.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    tprint("MADE BY NOWMAN")
    pygame.quit()
