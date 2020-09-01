import pygame as pg
from settings import *

class bg(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((WIDTH, HEIGHT))
        self.image.fill(LIGHTGRAY)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        'add top box'
        pg.draw.rect(self.image,DARKGRAY,pg.Rect((SCREEN_BORDER,SCREEN_BORDER),(WIDTH-2*SCREEN_BORDER,TOPLEFT[1])))

        'add tile backdrop'
        pg.draw.rect(self.image,VERYDARKGRAY,pg.Rect((TOPLEFT[0]-2,TOPLEFT[1]+10+SCREEN_BORDER-2),(WIDTH - SCREEN_BORDER*2+5,HEIGHT-TOPLEFT[1]-3*SCREEN_BORDER+5)))

        self.draw_lines()

    def draw_lines(self):
        for x in range(1,TILEX):
            pg.draw.line(self.image,VERYDARKGRAY,(x*TILESIZE + TOPLEFT[0],TOPLEFT[1]+10+SCREEN_BORDER),(x*TILESIZE + TOPLEFT[0],HEIGHT-SCREEN_BORDER))
        for y in range(1,TILEY):
            pg.draw.line(self.image,VERYDARKGRAY,(TOPLEFT[0],TOPLEFT[1]+10+SCREEN_BORDER + y*TILESIZE),(WIDTH - TOPLEFT[0],TOPLEFT[1]+10+SCREEN_BORDER + y*TILESIZE))

    def update(self):
        pass

class tile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE-1, TILESIZE-1))
        self.rect = self.image.get_rect()
        self.pos = tuple((x,y))
        self.pix = self.coord_to_pix(self.pos)
        self.rect.x = self.pix[0]
        self.rect.y = self.pix[1]
        self.neighbors = []
        self.num = 0
        self.revealed = False
        self.mine = False
        self.image.fill(VERYLIGHTGRAY)
        self.flagged = False

    def set_neighbors(self):
        self.num = 0
        self.neighbors = []
        for m in range(3):
            for n in range(3):
                if (self.pos[0]+m-1,self.pos[1]+n-1) in self.game.tiles:
                    self.neighbors.append(self.game.tiles[(self.pos[0]+m-1,self.pos[1]+n-1)])
        for neighbor in self.neighbors:
            if neighbor.mine:
                self.num += 1

    def update(self):
        self.target = self.coord_to_pix(self.pos)

    def coord_to_pix(self,coords):
        return (coords[0]*TILESIZE+1 + TOPLEFT[0],1+coords[1]*TILESIZE + TOPLEFT[1]+2*SCREEN_BORDER)

    def flag(self):
        if self.flagged:
            self.image.fill(VERYLIGHTGRAY)
            self.flagged = False
        else:
            self.image.blit(self.game.flag,(0,0))
            self.flagged = True

    def reveal(self):
        if not self.flagged:
            if self.mine:
                self.game.end()
            else:
                self.revealed = True
                self.image.fill(LIGHTGRAY)
                if self.num == 0:
                    for neighbor in self.neighbors:
                        if not neighbor.revealed:
                            neighbor.reveal()
                else:
                    self.game.draw_text(self.image,str(self.num),15,15,DARKRED,30)
