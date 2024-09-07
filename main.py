from configs import *
from sprites import *
from weapons import *
import pygame
import sys 

class Spritesheet:
    def __init__(self, path):
        self.spritesheet = pygame.image.load(path).convert()

    def getImg(self, x,y, width, height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.spritesheet,(0,0),(x,y, width,height))
        sprite.set_colorkey(BLACK)

        return sprite

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.terrainSpriteSheet = Spritesheet(r'')
        self.playerSpriteSheet = Spritesheet(r'')
        self.enemySpriteSheet = Spritesheet(r'')
        self.weaponSpriteSheet = Spritesheet(r'')
        self.bulletSpriteSheet = Spritesheet(r'')
        self.running = True
        self.Block_collide  = False
        self.Enemy_collide  = False
    def createTileMap(self):
        for i , row in enumerate(tileMap):
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column == 'B':
                    Block(self,j,i)
                elif column == 'P':
                    self.player  = Player(self,9,12)
                elif column == 'E':
                    self.enemyobj = Enemy(self,j,i)
                elif column == 'R':
                    Water(self,j,i)
                elif column == 'W':
                    Weapons(self,j,i)
                    # Bullet(self,i,j)
                
    def create(self):
        self.all_sprite = pygame.sprite.LayeredUpdates()
        self.blocks  = pygame.sprite.LayeredUpdates()
        self.enemy = pygame.sprite.LayeredUpdates()
        self.water = pygame.sprite.LayeredUpdates()
        self.mainPlayer = pygame.sprite.LayeredUpdates()
        self.weaponsshoot = pygame.sprite.LayeredUpdates()
        self.bullets = pygame.sprite.LayeredUpdates()
        self.healthbar = pygame.sprite.LayeredUpdates()
        self.createTileMap()
    def update(self):
        self.all_sprite.update()
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprite.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def camera(self):
        pressed = pygame.key.get_pressed()
        if self.Block_collide==False and self.Enemy_collide == False:
            if pressed[pygame.K_LEFT]:
                for i, sprites in enumerate(self.all_sprite):
                    sprites.rect.x +=PLAYER_CHANGE
            elif pressed[pygame.K_RIGHT]:
                for i, sprites in enumerate(self.all_sprite):
                    sprites.rect.x -=PLAYER_CHANGE
            elif pressed[pygame.K_UP]:
                for i, sprites in enumerate(self.all_sprite):
                    sprites.rect.y +=PLAYER_CHANGE
            elif pressed[pygame.K_DOWN]:
                for i, sprites in enumerate(self.all_sprite):
                    sprites.rect.y -=PLAYER_CHANGE




    def main(self):
        while self.running:
            self.events()
            self.camera()
            self.update()
            self.draw()

game = Game()
game.create()

while game.running:
    game.main()


pygame.quit()
sys.exit()