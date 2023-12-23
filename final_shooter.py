from random import randint
from pygame import *


window = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

win = 0
lost = 0

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.3)
mixer.music.play()

font.init()
font2 = font.Font(None, 36)

font1 = font.Font(None, 80)

game_over_lose = font1.render('YOU LOSE', True, (255,0,0))

game_over_win = font1.render('YOU WIN', True, (0,255,0))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + 30, self.rect.y, 25, 30, 25)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(10, 600)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


ship = Player('rocket.png', 5, 400, 80 ,100, 10)
monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(10, 600), 0, 65, 50, randint(1,3))
    monsters.add(enemy)

bullets = sprite.Group()
run = True
clock = time.Clock()
FPS = 60
finished = False
while run:
    window.blit(background, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()

    if not finished:
        ship.reset()
        ship.update()
        
        text = font2.render('Score:' + str(win), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Missed:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            win += 1
            enemy = Enemy('ufo.png', randint(10, 600), 0, 65, 50, randint(1,10))
            monsters.add(enemy)

    else:
        finished = False
        win = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(1000)
        for i in range(5):
            enemy = Enemy('ufo.png', randint(10, 600), 0, 65, 50, randint(1,3))
            monsters.add(enemy)


    if sprite.spritecollide(ship, monsters, False) or lost >= 5:
        finished = True
        window.blit(game_over_lose, (200, 200))

    if win >= 10:
        finished = True
        window.blit(game_over_win, (200, 200))


    clock.tick(FPS)
    display.update()
