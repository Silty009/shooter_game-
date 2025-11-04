#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as tm

window = display.set_mode((700, 500))
display.set_caption('Лабиринт')
background = transform.scale(image.load('backgr2.jpg'), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, w, h, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self): #управление игроком
        keys = key.get_pressed()
        
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(5, 10, 'bullet.png', self.rect.centerx, self.rect.top, -5)    
        bullets.add(bullet)
        
misses = 0
class Enemy(GameSprite):
    
    def update(self):
        global misses
        self.rect.y += self.speed
        if self.rect.y >= 500:

            self.rect.y = 0
            self.rect.x = randint(0, 655)
            misses += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 655)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroids(45, 35, 'asteroid.png', randint(0, 655), 0, randint(1, 2))
    asteroids.add(asteroid)
monsters = sprite.Group()
for i in range(5):
    enemy = Enemy(45, 35, 'spider.png.png', randint(0, 655), 0, randint(1, 3))
    monsters.add(enemy)





hero = Player(80, 80, 'hero.png1 (1).png', 290, 425, 5)




mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.3)
mixer.music.play()
fire_ = mixer.Sound('fire.ogg')



font.init()
font1 = font.SysFont('Arial', 70)
win = font1.render('YOU WIN!', True, (225, 215, 0))


lose = font1.render('YOU BIG LOOOOSER!>:)', True, (200, 215, 0))

font2 = font.SysFont('Arial', 25) #обязательно заменить класс font на SysFontfont2 = font.SysFont('Arial', 25) 

rel = font2.render('Ждите, перезарядка!', True, (255, 0, 0))

game = True
clock = time.Clock() #создаем игровой таймер

kills = 0

bullets = sprite.Group()

num_fire = 0
rel_time = False



finish = False

while game:

    
    
    
    for e in event.get():#для каждого события в списке событий совершаемый пользователем

        if e.type == QUIT:#если тип события равен нажатому крестику (выходу из игры)

            game = False#то тогда game = false
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and rel_time == False:
                    num_fire += 1
                    hero.fire()
                    fire_.play()  
                if num_fire > 5 and rel_time == False:
                    rel_time = True
                    start_rel = tm()



    if finish != True:
        window.blit(background, (0, 0))
        kills_count = font2.render('Убито:' + str(kills) , True, (200, 200, 200))
        window.blit(kills_count, (5, 5))
        misses_count = font2.render('Пропущено:' + str(misses), True, (200, 200, 200))
        window.blit(misses_count, (5, 25))
        hero.update()
        
        asteroids.update()
      
        hero.reset()
        monsters.update()
        bullets.update()
        bullets.draw(window)        
        monsters.draw(window)
        asteroids.draw(window)
        
        if rel_time == True:
            new_time = tm()
            if new_time - start_rel < 3:
                window.blit(rel, (250, 465))
            else:
                rel_time = False
                num_fire = 0

        if sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero, asteroids, False):
            finish = True
            window.blit(lose, (225, 225))
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprite_list:
            kills += 1
            enemy = Enemy(45, 35, 'spider.png.png', randint(0, 655), 0, randint(1, 3))
            monsters.add(enemy)
        if kills == 11:
            finish = True
            window.blit(win, (225, 225))
       

    
    
    display.update()
    clock.tick(60)

