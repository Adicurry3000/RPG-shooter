from configs import *
import pygame
import math

class Weapons(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self.x =x*TIleSize
        self.y =y*TIleSize
        self._layer = WEAPON_LAYER
        self.groups = self.game.all_sprite, self.game.weaponsshoot
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.width  = TIleSize
        self.height = TIleSize
        self.image= self.game.weaponSpriteSheet.getImg(0,0,self.width,self.height)
        self.rect  = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y  = self.y
        self.animationcounter = 0
    def animation(self):
        Animation = [self.game.weaponSpriteSheet.getImg(0,0,self.width,self.height),
                     self.game.weaponSpriteSheet.getImg(32,0,self.width,self.height),
                     self.game.weaponSpriteSheet.getImg(64,0,self.width,self.height)]
        self.image = Animation[math.floor(self.animationcounter)]
        self.animationcounter+=0.05
        if self.animationcounter >= 3:
            self.animationcounter = 0
    def update(self):
        self.animation()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self.x =x
        self.y =y
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprite, self.game.bullets
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.width  = TIleSize
        self.height = TIleSize
        self.image= self.game.bulletSpriteSheet.getImg(0,0,self.width, self.height)
        self.rect  = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y  = self.y
        self.direction = self.game.player.direction
    def move(self):
        if self.direction == 'right':
            self.rect.x += 6
        if self.direction == 'left':
            self.rect.x -= 6
        if self.direction == 'up':
            self.rect.y -= 6
        if self.direction == 'down':
            self.rect.y += 6
    def update(self):
        self.move()
        self.block_collide()
        self.enemy_collide()
    
    def block_collide(self):
        collide=  pygame.sprite.spritecollide(self, self.game.blocks, False)
        if collide:
            self.kill()
    
    def enemy_collide(self):
        collide=  pygame.sprite.spritecollide(self, self.game.enemy, False)
        if collide:
            collide[0].damage(1)
            self.kill()


class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self.x =x
        self.y =y
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprite, self.game.bullets
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.width  = TIleSize
        self.height = TIleSize
        self.image= self.game.bulletSpriteSheet.getImg(0,0,self.width, self.height)
        self.rect  = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y  = self.y
        self.direction = self.game.enemyobj.direction
    def move(self):
        if self.direction == 'right':
            self.rect.x += 6
        if self.direction == 'left':
            self.rect.x -= 6
        if self.direction == 'up':
            self.rect.y -= 6
        if self.direction == 'down':
            self.rect.y += 6
    def update(self):
        self.move()
        self.block_collide()
        self.player_collide()
    
    def block_collide(self):
        collide=  pygame.sprite.spritecollide(self, self.game.blocks, False)
        if collide:
            self.kill()
    
    def player_collide(self):
        collide=  pygame.sprite.spritecollide(self, self.game.mainPlayer, False)
        if collide:
            self.game.player.damage(1)
            self.kill()
