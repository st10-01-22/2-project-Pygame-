import os
import pygame
import sys
from art import tprint


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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def start_screen():
    intro_text = []
    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
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


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '<':
                Tile('hill1', x, y)
            elif level[y][x] == '=':
                Tile('hill2', x, y)
            elif level[y][x] == '>':
                Tile('hill3', x, y)
            elif level[y][x] == '^':
                Tile('hut', x, y)
            elif level[y][x] == '/':
                Tile('forestt', x, y)
            elif level[y][x] == '|':
                Tile('forestd', x, y)
            elif level[y][x] == '0':
                Tile('water', x, y)
            elif level[y][x] == '1':
                Tile('house1', x, y)
            elif level[y][x] == '2':
                Tile('house2', x, y)
            elif level[y][x] == '3':
                Tile('house3', x, y)
            elif level[y][x] == '4':
                Tile('house4', x, y)
            elif level[y][x] == '&':
                Tile('mountain', x, y)
            elif level[y][x] == '5':
                Tile('dark', x, y)
            elif level[y][x] == '!':
                Tile('rock', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(load_image("ходьба вправо.png", (0, 0, 0)), 4, 1, x, y)

    return new_player, x, y


def generate_dungeon_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('floor', x, y)
            elif level[y][x] == '/':
                Tile('wall', x, y)
            elif level[y][x] == '&':
                Tile('ladder', x, y)
            elif level[y][x] == '|':
                Tile('torch', x, y)
            elif level[y][x] == '#':
                Tile('carpet', x, y)
            elif level[y][x] == '5':
                Tile('tp', x, y)
            elif level[y][x] == '@':
                Tile('carpet', x, y)
                new_player = Player(load_image("ходьба вправо.png", (0, 0, 0)), 4, 1, x, y)
            elif level[y][x] == '6':
                Tile('carpet', x, y)
                Slime(load_image("атака слайма.png", (0, 0, 0)), 4, 1, x, y)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'dark' or tile_type == 'tp':
            super().__init__(tiles_group, all_sprites, tp_group)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
        elif tile_type != 'empty':
            super().__init__(tiles_group, all_sprites, barriers_group)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
        else:
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def move(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y

    def get_event(self, sheet, columns, rows, x, y):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)


class Slime(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, pos_x, pos_y):
        super().__init__(slime_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def get_attacked(self, pos, sheet, columns, rows, x, y):
        if pygame.sprite.collide_mask(self, pos):
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.image.get_rect().move(x, y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def start_level():
    player, level_x, level_y = generate_level(load_level('map.txt'))
    camera = Camera()
    running = True
    dist = 7

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_s]:
                x = player.rect.x
                y = player.rect.y
                player.get_event(load_image('ходьба влево вниз.png', (0, 0, 0)), 4, 1, x, y)
                player.move(player.rect.x, player.rect.y + dist)
            if key[pygame.K_w]:
                x = player.rect.x
                y = player.rect.y
                player.get_event(load_image('ходьба вверх.png', (0, 0, 0)), 4, 1, x, y)
                player.move(player.rect.x, player.rect.y - dist)
            if key[pygame.K_d]:
                x = player.rect.x
                y = player.rect.y
                player.get_event(load_image('ходьба вправо.png', (0, 0, 0)), 4, 1, x, y)
                player.move(player.rect.x + dist, player.rect.y)
            if key[pygame.K_a]:
                x = player.rect.x
                y = player.rect.y
                player.get_event(load_image('ходьба влево вниз.png', (0, 0, 0)), 4, 1, x, y)
                player.move(player.rect.x - dist, player.rect.y)
            if key[pygame.K_SPACE]:
                x = player.rect.x
                y = player.rect.y
                player.get_event(load_image('удар вправо.png', (0, 0, 0)), 3, 1, x, y)

        if not pygame.sprite.spritecollideany(player, tp_group):
            screen.fill(pygame.Color("black"))
            all_sprites.draw(screen)
            tiles_group.draw(screen)
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            player_group.draw(screen)
            all_sprites.update()
        else:
            all_sprites.empty()
            player_group.empty()
            tiles_group.empty()
            barriers_group.empty()
            tp_group.empty()
            return 2
        clock.tick(FPS)
        pygame.display.flip()


def dungeon_level():
    player, level_x, level_y,  = generate_dungeon_level(load_level('dangeon_map.txt'))
    camera = Camera()
    running = True
    dist = 7
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_s]:
                x = player.rect.x
                y = player.rect.y
                player.get_event(load_image('ходьба влево вниз.png', (0, 0, 0)), 4, 1, x, y)
                player.move(player.rect.x, player.rect.y + dist)
            if key[pygame.K_w]:
                x = player.rect.x
                y = player.rect.y
                player.get_event(load_image('ходьба вверх.png', (0, 0, 0)), 4, 1, x, y)
                player.move(player.rect.x, player.rect.y - dist)
            if key[pygame.K_d]:
                x = player.rect.x
                y = player.rect.y
                player.get_event(load_image('ходьба вправо.png', (0, 0, 0)), 4, 1, x, y)
                player.move(player.rect.x + dist, player.rect.y)
            if key[pygame.K_a]:
                x = player.rect.x
                y = player.rect.y
                player.get_event(load_image('ходьба влево вниз.png', (0, 0, 0)), 4, 1, x, y)
                player.move(player.rect.x - dist, player.rect.y)
            if key[pygame.K_SPACE]:
                x = player.rect.x
                y = player.rect.y
                c = (x, y)
                player.get_event(load_image('удар вправо.png', (0, 0, 0)), 3, 1, x, y)
                for slime in slime_group:
                    x_2 = slime.rect.x
                    y_2 = slime.rect.y
                    slime.get_attacked(player, load_image('слизень умер.png', (255, 255, 255)), 1, 1, x_2, y_2)

        if not pygame.sprite.spritecollideany(player, tp_group):
            screen.fill(pygame.Color("black"))
            all_sprites.draw(screen)
            tiles_group.draw(screen)
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            player_group.draw(screen)
            slime_group.draw(screen)
            all_sprites.update()
        else:
            all_sprites.empty()
            player_group.empty()
            tiles_group.empty()
            barriers_group.empty()
            tp_group.empty()
            slime_group.empty()
            return 1
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == "__main__":
    size = width, height = 1500, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    barriers_group = pygame.sprite.Group()
    tp_group = pygame.sprite.Group()
    slime_group = pygame.sprite.Group()
    player = None
    FPS = 15
    pygame.init()
    tile_images = {
        'empty': load_image('trava.png'),
        'hill1': load_image('gorka_pr.png'),
        'hill2': load_image('горка.png'),
        'hill3': load_image('gorka_lev.png'),
        'hut': load_image('шалаш.png'),
        'forestt': load_image('лесвверх.png'),
        'forestd': load_image('лесниз.png'),
        'water': load_image('water.png'),
        'house1': load_image('house1.png'),
        'house2': load_image('house2.png'),
        'house3': load_image('house3.png'),
        'house4': load_image('house4.png'),
        'mountain': load_image('mountain.png'),
        'dark': load_image('dark.png'),
        'rock': load_image('rock.png'),
        'ladder': load_image('ladder.png'),
        'wall': load_image('dungeon wall.png'),
        'torch': load_image('torch.png'),
        'floor': load_image('dungeon floor.png'),
        'carpet': load_image('ковёр.png'),
        'tp': load_image('портал.png')
    }
    tile_width = tile_height = 31
    start_screen()
    run_all = True
    flag = 1
    while run_all:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_all = False
        if flag == 1:
            flag = start_level()
        elif flag == 2:
            flag = dungeon_level()

    tprint("MADE BY NOWMAN")
    tprint("DRAWN BY lIGHTYEAR")
    pygame.quit()
