
import pygame
from configs import *
from weapons import *
import random
import math 


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self.x =x*TIleSize
        self.y =y*TIleSize
        self._layer = BLOCKS_LAYER
        self.groups = self.game.all_sprite, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.width  = TIleSize
        self.height = TIleSize
        self.image= self.game.terrainSpriteSheet.getImg(991,541,self.width,self.height)
        self.rect  = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y  = self.y

        
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self.x =x*TIleSize
        self.y =y*TIleSize
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.width  = TIleSize
        self.height = TIleSize
        self.image= self.game.terrainSpriteSheet.getImg(447,353,self.width,self.height)
        self.rect  = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y  = self.y

class Water(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self.x =x*TIleSize
        self.y =y*TIleSize
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprite, self.game.water
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.width  = TIleSize
        self.height = TIleSize
        self.image= self.game.terrainSpriteSheet.getImg(865,160,self.width,self.height)
        self.rect  = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y  = self.y
        self.animationcounter = 1
    def animation(self):
        Animation = [self.game.terrainSpriteSheet.getImg(865,160,self.width,self.height),
                    self.game.terrainSpriteSheet.getImg(897,160,self.width,self.height),
                    self.game.terrainSpriteSheet.getImg(928,160,self.width,self.height)]
        self.image = Animation[math.floor(self.animationcounter)]
        self.animationcounter+=0.01
        if self.animationcounter >= 3:
            self.animationcounter = 0
    def update(self):
        self.animation()

class Player(pygame.sprite.Sprite):
    def __init__(self,game,x,y) :
        self.game = game
        self._layer = PLAYER_LAYER

        self.x =x*TIleSize
        self.y =y*TIleSize

        self.groups = self.game.all_sprite, self.game.mainPlayer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.healthbar = Player_Healthbar(game, x,y)
        self.eqip = False

        self.width  = TIleSize
        self.height = TIleSize

        self.x_change = 0
        self.y_change = 0

        self.image= self.game.playerSpriteSheet.getImg(0,0,self.width,self.height)
        self.rect  = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y  = self.y
        self.animationcounter = 0 
        self.direction = 'right'  

        self.shootstate = 'shoot'
        self.counter = 0
        self.waitTime = 20 

        self.particle_counter = 0
        self.particle_wait = 2

        self.health = PLAYER_HEALTH
        
    def movement(self):
        self.particle_counter+=1
        if self.particle_counter ==self.particle_wait:
            Particle(self.game, self.rect.x+ random.randrange(0,32), self.rect.y+32)
        press = pygame.key.get_pressed()

        if press[pygame.K_LEFT]:
            self.x_change = self.x_change - PLAYER_CHANGE
            self.direction = 'left'
        elif press[pygame.K_RIGHT]:
            self.x_change = self.x_change + PLAYER_CHANGE
            self.direction = 'right'
        elif press[pygame.K_UP]:
            self.y_change = self.y_change - PLAYER_CHANGE
            self.direction = 'up'
        elif press[pygame.K_DOWN]:
            self.y_change = self.y_change + PLAYER_CHANGE
            self.direction = 'down'
    def update(self):
        
        self.movement()
        self.animation()
        
        
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        self.collition_with_block()
        self.collide_weapon()
        self.shoot()
        self.waitAfterShoot()
        self.collition_with_enemy()
        self.x_change = 0
        self.y_change  = 0
    def shoot(self):
        pressed = pygame.key.get_pressed()
        if self.shootstate == 'shoot':
            if self.eqip:
                if pressed[pygame.K_z]:
                    Bullet(self.game, self.rect.x, self.rect.y)
                    self.shootstate = 'wait'
    def damage(self, amount):
        self.health = self.health -  amount
        self.healthbar.damage()

        if self.health <= 0:
            self.kill()
            self.healthbar.kill()
                    

    def animation(self):
        downAnimation = [self.game.playerSpriteSheet.getImg(0,0,self.width,self.height),
                         self.game.playerSpriteSheet.getImg(32,0,self.width,self.height),
                         self.game.playerSpriteSheet.getImg(64,0,self.width,self.height)]
        upAnimation = [self.game.playerSpriteSheet.getImg(0,96,self.width,self.height),
                       self.game.playerSpriteSheet.getImg(32,96,self.width,self.height),
                       self.game.playerSpriteSheet.getImg(64,96,self.width,self.height)]
        leftAnimation = [self.game.playerSpriteSheet.getImg(0,32,self.width,self.height),
                         self.game.playerSpriteSheet.getImg(32,32,self.width,self.height),
                         self.game.playerSpriteSheet.getImg(64,32,self.width,self.height)]
        rightAnimation = [self.game.playerSpriteSheet.getImg(0,64,self.width,self.height),
                         self.game.playerSpriteSheet.getImg(32,64,self.width,self.height),
                         self.game.playerSpriteSheet.getImg(64,64,self.width,self.height)]
        
        if self.direction == 'down':
            if self.y_change == 0:
                self.image = self.game.playerSpriteSheet.getImg(32,0,self.width,self.height)
            else:
                self.image = downAnimation[math.floor(self.animationcounter)]
                self.animationcounter+=0.1
                if self.animationcounter >= 3:
                    self.animationcounter = 0
        if self.direction == 'left':
            if self.x_change == 0:
                self.image = self.game.playerSpriteSheet.getImg(32,32,self.width,self.height)
            else:
                self.image = leftAnimation[math.floor(self.animationcounter)]
                self.animationcounter+=0.1
                if self.animationcounter >= 3:
                    self.animationcounter = 0
        if self.direction == 'right':
            if self.x_change == 0:
                self.image = self.game.playerSpriteSheet.getImg(32,64,self.width,self.height)
            else:
                self.image = rightAnimation[math.floor(self.animationcounter)]
                self.animationcounter+=0.1
                if self.animationcounter >= 3:
                    self.animationcounter = 0
        
        if self.direction == 'up':
            if self.y_change == 0:
                self.image = self.game.playerSpriteSheet.getImg(32, 96,self.width,self.height)
            else:
                self.image = upAnimation[math.floor(self.animationcounter)]
                self.animationcounter+=0.1
                if self.animationcounter >= 3:
                    self.animationcounter = 0
    def collition_with_block(self):
        pressed = pygame.key.get_pressed()
        collideBlock = pygame.sprite.spritecollide(self, self.game.blocks, False , pygame.sprite.collide_rect_ratio(0.85))
        collideWater = pygame.sprite.spritecollide(self, self.game.water, False , pygame.sprite.collide_rect_ratio(0.90))

        if collideWater or collideBlock:
            self.game.Block_collide = True
            if pressed[pygame.K_LEFT]:
                self.rect.x += PLAYER_CHANGE
                
            elif pressed[pygame.K_RIGHT]:
                self.rect.x -= PLAYER_CHANGE
                    
            elif pressed[pygame.K_UP]:
                self.rect.y += PLAYER_CHANGE
                    
            elif pressed[pygame.K_DOWN]:
                self.rect.y -= PLAYER_CHANGE
        else:
            self.game.Block_collide = False
    def collide_weapon(self):
        collide=  pygame.sprite.spritecollide(self, self.game.weaponsshoot, True)
        if collide:
            self.eqip = True
   

    def waitAfterShoot(self):
        if self.shootstate == 'wait':
            self.counter+=1
            if self.counter >= self.waitTime:
                self.shootstate ='shoot'
                self.counter = 0
    def collition_with_enemy(self):
        pressed = pygame.key.get_pressed()
        collide = pygame.sprite.spritecollide(self, self.game.enemy, False , pygame.sprite.collide_rect_ratio(0.85))
        if collide:
            self.game.Enemy_collide = True
            if pressed[pygame.K_LEFT]:
                self.rect.x += PLAYER_CHANGE
                
            elif pressed[pygame.K_RIGHT]:
                self.rect.x -= PLAYER_CHANGE
                
                
            elif pressed[pygame.K_UP]:
                self.rect.y += PLAYER_CHANGE
                
                
            elif pressed[pygame.K_DOWN]:
                self.rect.y -= PLAYER_CHANGE  
        else:
            self.game.Enemy_collide = False          





class Enemy(pygame.sprite.Sprite):
    def __init__(self,game,x,y) :
        self.game = game
        self._layer = ENEMY_LAYER

        self.x =x*TIleSize
        self.y =y*TIleSize

        self.groups = self.game.all_sprite, self.game.enemy
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.healthbar = Enemy_Healthbar(game, self, x,y)

        self.width  = TIleSize
        self.height = TIleSize

        self.x_change = 0
        self.y_change = 0

        self.image= self.game.enemySpriteSheet.getImg(0,0,self.width,self.height)
        self.rect  = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y  = self.y
        self.direction = random.choice(['left','right','up','down'])
        self.numberofsteps = random.choice([30,40,50,60,70,80])
        self.stallsteps = self.numberofsteps * random.choice([1,2,3])
        self.state = 'moving'
        self.currentSteps = 0
        self.animationcounter = 0

        self.shootcounter = 0
        self.waitTime = random.choice([10,25, 20,30,45,50,60,70,80,90])
        self.shootstate = 'wait'

        self.health = ENEMY_HEALTH

    def shoot(self):
        if self.shootstate == 'wait':
            self.shootcounter +=1
            if self.shootcounter>=self.waitTime:
                self.shootstate ="shoot"
                self.shootcounter = 0
                self.waitTime = random.choice([10,25, 20,30,45,50,60,70,80,90])
        if self.shootstate == 'shoot':
            Enemy_Bullet(self.game, self.rect.x, self.rect.y)
            self.shootstate = 'wait'


    def movement(self):
        if self.state == 'moving':
            if self.direction == 'left':
                self.x_change = self.x_change - ENEMY_CHANGE
                self.currentSteps+=1
                
                
            if self.direction == 'right':
                self.x_change = self.x_change + ENEMY_CHANGE
                self.currentSteps+=1
                
            if self.direction == 'up':
                self.y_change = self.y_change - ENEMY_CHANGE
                self.currentSteps+=1
                
            if self.direction == 'down':
                self.y_change = self.y_change + ENEMY_CHANGE
                self.currentSteps+=1

            if self.currentSteps== self.numberofsteps:
                self.currentSteps = 0
                
                self.state = 'stalling'
                self.numberofsteps = random.choice([30,40,50,60,70,80])
                self.stallsteps = self.numberofsteps * random.choice([1,2,3])
                
                
        elif self.state == 'stalling':
            self.currentSteps +=1
            if self.currentSteps == self.stallsteps:
                self.state = 'moving'
                self.currentSteps = 0
                self.direction = random.choice(['left','right','up','down'])
    def collidePlayer(self):
        # collide = pygame.sprite.spritecollide(self, self.game.mainPlayer, True)
        # if collide:
        #     self.game.running = False
        pass
    def collition_with_block(self):
        
        collideBlock = pygame.sprite.spritecollide(self, self.game.blocks, False , pygame.sprite.collide_rect_ratio(0.85))
        collideWater = pygame.sprite.spritecollide(self, self.game.water, False , pygame.sprite.collide_rect_ratio(0.90))

        if collideBlock or collideWater:
            
            if self.direction   == 'left':
                self.rect.x += ENEMY_CHANGE
                self.direction   = 'right'
                
            elif self.direction   == 'right':
                self.rect.x -= ENEMY_CHANGE
                self.direction   = 'left'
                
            elif self.direction   == 'up':
                self.rect.y += ENEMY_CHANGE
                self.direction   = 'down'
                
            elif self.direction   == 'down':
                self.rect.y -= ENEMY_CHANGE
                self.direction   = 'up' 
        
            
    def update(self):
        self.movement()
        self.animation()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        self.collition_with_block()
        self.collidePlayer()
        self.x_change = 0
        self.y_change  = 0
        self.shoot()

    def damage(self, amount):
        self.health = self.health -  amount
        self.healthbar.damage(ENEMY_HEALTH, self.health)

        if self.health <= 0:
            self.kill()
            self.healthbar.kill()
    
    def animation(self):
        downAnimation = [self.game.enemySpriteSheet.getImg(0,0,self.width,self.height),
                         self.game.enemySpriteSheet.getImg(32,0,self.width,self.height),
                         self.game.enemySpriteSheet.getImg(64,0,self.width,self.height)]
        upAnimation = [self.game.enemySpriteSheet.getImg(0,96,self.width,self.height),
                       self.game.enemySpriteSheet.getImg(32,96,self.width,self.height),
                       self.game.enemySpriteSheet.getImg(64,96,self.width,self.height)]
        leftAnimation = [self.game.enemySpriteSheet.getImg(0,32,self.width,self.height),
                         self.game.enemySpriteSheet.getImg(32,32,self.width,self.height),
                         self.game.enemySpriteSheet.getImg(64,32,self.width,self.height)]
        rightAnimation = [self.game.enemySpriteSheet.getImg(0,64,self.width,self.height),
                         self.game.enemySpriteSheet.getImg(32,64,self.width,self.height),
                         self.game.enemySpriteSheet.getImg(64,64,self.width,self.height)]
        
        if self.direction == 'down':
            if self.y_change == 0:
                self.image = self.game.enemySpriteSheet.getImg(32,0,self.width,self.height)
            else:
                self.image = downAnimation[math.floor(self.animationcounter)]
                self.animationcounter+=0.1
                if self.animationcounter >= 3:
                    self.animationcounter = 0
        if self.direction == 'left':
            if self.x_change == 0:
                self.image = self.game.enemySpriteSheet.getImg(32,32,self.width,self.height)
            else:
                self.image = leftAnimation[math.floor(self.animationcounter)]
                self.animationcounter+=0.1
                if self.animationcounter >= 3:
                    self.animationcounter = 0
        if self.direction == 'right':
            if self.x_change == 0:
                self.image = self.game.enemySpriteSheet.getImg(32,64,self.width,self.height)
            else:
                self.image = rightAnimation[math.floor(self.animationcounter)]
                self.animationcounter+=0.1
                if self.animationcounter >= 3:
                    self.animationcounter = 0
        
        if self.direction == 'up':
            if self.y_change == 0:
                self.image = self.game.enemySpriteSheet.getImg(32, 96,self.width,self.height)
            else:
                self.image = upAnimation[math.floor(self.animationcounter)]
                self.animationcounter+=0.1
                if self.animationcounter >= 3:
                    self.animationcounter = 0
       
class Player_Healthbar(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self._layer = HEALTH_LAYER

        self.x =x*TIleSize
        self.y =y*TIleSize

        self.groups = self.game.all_sprite , self.game.healthbar
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.width  = 40
        self.height = 10

        self.image= pygame.Surface([self.width,self.height])
        self.image.fill(GREEN)
        self.rect  = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y  = self.y - TIleSize/2
    def move(self):
        self.rect.x = self.game.player.rect.x
        self.rect.y = self.game.player.rect.y - TIleSize/2
    def update(self):
        self.move()
    def damage(self ):
        self.image.fill(RED)
        width = self.rect.width * self.game.player.health/PLAYER_HEALTH
        pygame.draw.rect(self.image, GREEN, (0,0,width, self.height), 0)
    
    def kill_bar(self):
        self.kill()

    
    

class Enemy_Healthbar(pygame.sprite.Sprite):
    def __init__(self, game,enemy, x,y):
        self.game = game
        self._layer = HEALTH_LAYER
        self.enemy = enemy

        self.x =x*TIleSize
        self.y =y*TIleSize

        self.groups = self.game.all_sprite, self.game.healthbar
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.width  = 40
        self.height = 10

        self.image= pygame.Surface([self.width,self.height])
        self.image.fill(GREEN)
        self.rect  = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y  = self.y - TIleSize/2

        self.health = ENEMY_HEALTH

    def move(self):
        self.rect.x = self.enemy.rect.x
        self.rect.y = self.enemy.rect.y - TIleSize/2
    def damage(self , total_health, health):
        self.image.fill(RED)
        width = self.rect.width * health/total_health

        pygame.draw.rect(self.image, GREEN, (0,0,width, self.height), 0)
    def update(self):
        self.move()
    def kill_bar(self):
        self.kill()

class Particle(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self._layer = HEALTH_LAYER

        self.groups = self.game.all_sprite
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = pygame.Surface([4,4])
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
        self.lifetime = 6

    def move(self):
        w=0
        self.counter+=1
        w+=0.1
        self.rect.y +=math.floor(w)
        if self.counter >=6:
            self.kill()
            self.counter = 0
            w=0
    def update(self):
        self.move()