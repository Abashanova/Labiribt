from pygame import*
#Шрифт
font.init()
font = font.SysFont('Times New Roman',50)
win = font.render('YOU WIN!',True, (237, 0, 8))
lose = font.render('YOU LOSE!',True, (237, 0, 8))
#Картинки
img_back = 'space.jpg'
img_hero =  'hero.png'
img_enemy =  'enemy.png'
img_end = 'end.png'
img_bullet = 'bullet.png'
#Музыка
mixer.init() #Подключаем музыку к игре
mixer.music.load('music.ogg') #Загружаем файл
mixer.music.play()
fire = mixer.Sound('sound1.ogg')
#boom = mixer.Sound('')



#Классы
class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        sprite.Sprite.__init__(self)
        #Каждый спрайт должен хранить свойство - изображение
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        #Каждый спрайт должен хранить свое свойство - прямоугольник
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self): #Метод отрисовки героя
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite): #Унаследовал все у класса родителя ЭТО УЖЕ САМ СПРАЙТ
    def update(self): #управление
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5: #Ограничение в движении
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self): #Метод оружия , используем место игрока, чтоб на его месте создать оружие
          bullet = Bullet(img_bullet, self.rect.right, self.rect.centery, 24, 25, 10)
          bullets.add(bullet)
class Enemy(GameSprite): #Класс врага, который будет двигаться вправо влево
    side = 'left'
    def update(self):
        if self.rect.x <= 470:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Enemy2(GameSprite): #Класс врага, который будет двигаться вверх вниз
    side = 'up'
    def update(self):
        if self.rect.y <= 130:
            self.side = 'up'
        if self.rect.y >= win_height - 270:
            self.side = 'down'
        if self.side == 'down':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        



class Wall(sprite.Sprite):
    def __init__(self, red, green, blue, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.red = red
        self.green = green 
        self.blue = blue
        self.w = wall_width
        self.h = wall_height
        #Каждый спрайт должен хранить свое свойство - image
        self.image = Surface((self.w, self.h))
        self.image.fill((red, green, blue)) #Стена
        #Каждый спрайт должен хранить свое свойство rect
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width+10:
            self.kill() #Убираем пулю вообще
#Окно игры
win_width = 700
win_height= 700
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load(img_back),(win_width, win_height))
#Персонажи
hero = Player(img_hero, 5, win_height - 60, 60, 70, 10) 
enemy = Enemy(img_enemy, win_width - 80, 280, 65, 65, 10)
enemy2 = Enemy2(img_enemy, 70, 200, 65, 65, 10)
final = GameSprite(img_end, win_width - 150, win_height - 100, 100, 65, 0)

#Стены
w1 = Wall (255, 255, 255, 100, 20, 450, 10)
w2 = Wall (255, 255, 255, 100, 480, 350, 10)
w3 = Wall (255, 255, 255, 100, 20, 10, 380)
w4 = Wall (255, 255, 255, 200, 130, 10, 200)
w5 = Wall (255, 255, 255, 450, 130, 10, 360)
w6 = Wall (255, 255, 255, 300, 20, 10, 30)
w7 = Wall (255, 255, 255, 390, 120, 130, 10)
w8 = Wall (255, 255, 255, 300, 130, 10, 200)
w9 = Wall (255, 255, 255, 200, 280, 10, 200)


#Группы спрайтов 
enemies = sprite.Group()
walls = sprite.Group()
bullets = sprite.Group()

walls.add(w1, w1, w3, w4, w5, w6, w7, w8, w9)
enemies.add(enemy, enemy2)

points = 0
#Игровой цикл
game = True
finish = False
clock = time.Clock()
FPS = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire() #Применяем метод fire
                fire.play()
    if finish != True:
            window.blit(back, (0,0))
            walls.draw(window)
            hero.reset()
            hero.update()
            enemies.update()
            enemies.draw(window)
            final.reset()
            bullets.draw(window)
            bullets.update()
            sprite.groupcollide(bullets, enemies, True, True)
            if sprite.groupcollide(bullets, enemies, True, True):
                points += 1
            x = font.render(str(points), True, (255, 255, 255))
            window.blit(x, (20, 20)) #Отображаем очки на экране
            
            
            #Проигрыш
            if sprite.spritecollide(hero, walls, False):
                finish = True
                window.blit(lose, (200, 200))

            if sprite.spritecollide(hero, enemies, False):
                finish = True
                window.blit(lose, (200, 200))
                
            #Победа
            if sprite.collide_rect(hero, final):
                finish = True
                window.blit(win, (200,200))

        
    display.update()
    clock.tick(FPS)
