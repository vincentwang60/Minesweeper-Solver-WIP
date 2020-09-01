import pygame as pg
import sys
import random as r
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.mines_left = MINENUMBER
        self.game_over = False
        self.bg = bg(self)
        self.tiles = {}
        self.first_click = False
        for x in range(TILEX):
            for y in range(TILEY):
                self.tiles[(x,y)]= tile(self,x,y)
        self.mouse_pos = []

    def place_mines(self,x,y):
        found = False
        start_tile = None
        while not found:
            mine_list = r.sample(range(0,TILEX*TILEY),MINENUMBER)
            found = True
            for m in range(3):
                for n in range(3):
                    if x+m-1+TILEX*(y+n-1) in mine_list:
                        found = False
        start_tile = self.tiles[(x,y)]
        for tile in self.tiles.values():
            if tile.pos[0]+TILEX*tile.pos[1] in mine_list:
                tile.mine = True
        for a_tile in self.tiles.values():
            a_tile.set_neighbors()
        print(len(self.tiles))
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,"sprites")

        self.flag = pg.image.load(path.join(img_folder,"flag.png")).convert_alpha()
        self.mine = pg.image.load(path.join(img_folder,"mine.png")).convert_alpha()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def end(self,victory):
        self.game_over = True
        for tile in self.tiles.values():
            if tile.mine:
                tile.image.blit(self.mine,(0,0))
        self.bg.update_counter()
        if victory:
            self.draw_text(self.bg.image,'YOU WIN!',int(WIDTH/2),40,VERYDARKGRAY,40)
        else:
            self.draw_text(self.bg.image,'GAME OVER',int(WIDTH/2),40,VERYDARKGRAY,40)

    def victory_check(self):
        for tile in self.tiles.values():
            if not tile.revealed and not tile.mine:
                return False
        return True

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_SPACE:
                    for tile in self.tiles.values():
                        if tile.mine:
                            tile.image.fill(LIGHTRED)
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    for tile in self.tiles.values():
                        if tile.mine:
                            tile.image.fill(VERYLIGHTGRAY)
            if event.type == pg.MOUSEBUTTONDOWN:
                if not self.game_over:
                    self.mouse_pos = pg.mouse.get_pos()
                    if event.button == 1:
                        for tile in self.tiles.values():
                            if tile.rect.collidepoint(self.mouse_pos) and not tile.revealed:
                                if not self.first_click:
                                    self.place_mines(tile.pos[0],tile.pos[1])
                                    self.first_click = True
                                tile.reveal()
                    elif event.button == 3:
                        for tile in self.tiles.values():
                            if tile.rect.collidepoint(self.mouse_pos) and not tile.revealed:
                                if tile.flag():
                                    self.mines_left -= 1
                                else:
                                    self.mines_left += 1
                        self.bg.update_counter()
                    if self.victory_check():
                        self.end(True)

    def draw_text(self,surface,text,x,y,color,size):
        font_name = pg.font.match_font(FONT_NAME)
        font = pg.font.Font(font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_surface,text_rect)

# create the game object
g = Game()
while True:
    g.new()
    g.run()
