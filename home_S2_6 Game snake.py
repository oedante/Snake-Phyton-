#Learning group: группа Pytн-КБд-242304-25
#Autor: Ермишин Олег
#Курс 2
#Домашнее задание 6

import datetime
import os
import pygame
import random
import time

global eat_count
eat_count = 0

#получаем текущий час и выбираем приветствее
current_hour = datetime.datetime.now().time().hour                                                    

if current_hour < 5 or current_hour > 22:
    greeting = 'Доброй ночи'
elif current_hour < 10:
    greeting = 'Доброе утро'
elif current_hour < 19:
    greeting = 'Добрый день'
elif current_hour < 23:
    greeting = 'Добрый вечер'
else: 
    greeting = 'Доброго апокалипсиса'

#выводим приветствие
print(f'{greeting}, {os.getlogin()}.\n')
#Получаем текущую деррикторию скрипта
curr_dir = os.path.dirname(os.path.abspath(__file__))

#---------------------------------------------------------------------------------------------------------
#Свойства окна и FPS
win_width = 800
win_height = 800
fps = 5
title = 20
speed_x = 20
speed_y = 0

#Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((win_width, win_height), 0, 32 )

pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

#Объекты змеи
snake_length = []

#Класс змеи
class snake_head(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((title, title))
        self.image.fill((150,150,150))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xx = x
        self.yy = y

    def update(self):
        #Запоминаем текущую позиция
        self.xx = self.rect.x
        self.yy = self.rect.y
        #Двигаемся
        self.rect.x += speed_x
        self.rect.y += speed_y

    def upgrade(self):
        #Создаем еще один элемент хвоста
        snake_length.append(snake_tail(snake_length[-1].rect.x , snake_length[-1].rect.y))
        all_sprites.add(snake_length[-1])

#Класс хвоста змеи
class snake_tail(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((title, title))
        self.image.fill((210,210,210))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xx = x
        self.yy = y

    def update(self):
        global eat_count
        #Запоминаем текущую позиция
        self.xx = self.rect.x
        self.yy = self.rect.y
        #Двигаемся, получая предыдущие координаты предыдущего блока
        self.rect.x = snake_length[snake_length.index(self) - 1].xx
        self.rect.y = snake_length[snake_length.index(self) - 1].yy

        #Столкнулись сами с собой и съедаем себя
        if self.rect.colliderect(snake.rect):
            for item in snake_length[-1:len(snake_length) - snake_length.index(self)-1:-1]:
                item.kill()
                snake_length.pop()
                eat_count -=1
    
#Класс еды
class eat(pygame.sprite.Sprite):
    #Сколько еды на экране
    instances_count = 0

    def __init__(self, x, y):
        eat.instances_count += 1
        pygame.sprite.Sprite.__init__(self)
        self.image =  pygame.transform.scale(pygame.image.load( "{0}.png".format(curr_dir + '\\img\\apple')).convert_alpha(),(title,title))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        #Сколько съели
        global eat_count
        #Коллизия со змеей, съели яблоко
        if self.rect.colliderect(snake.rect):
            self.kill()
            eat.instances_count -= 1
            eat_count +=1
            snake.upgrade()

# Создаем пользовательское событие проверки количества еды
ADD_EAT= pygame.USEREVENT + 1
# Устанавливаем таймер на 0,5 секунд
pygame.time.set_timer(ADD_EAT, 500)

#Вывод счетчика
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (200,200,200))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Цикл игры------------------------------------------------------------------------------------
all_sprites = pygame.sprite.Group()
snake = snake_head(random.randrange((title * 5), win_width - (title * 5), title),random.randrange((title * 5), win_height - (title * 5), title))
all_sprites.add(snake)
snake_length.append(snake)


running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(fps)

    # Обновление
    all_sprites.update()
    # Рендеринг
    screen.fill(( 0, 0, 0 ))
    draw_text(screen, f'Вы съели яблок: {eat_count}', 18, win_width / 2 + 300, 10)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
    # Обрабатываем события 
    for event in pygame.event.get(): 
        #Если событие закрытия окна, то выходим из цикла 
        if event.type == pygame.QUIT:
            running = False 

        #Двигаем змею
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and speed_y == 0:
                speed_x = 0
                speed_y = -title
            if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and speed_y == 0:
                speed_x = 0
                speed_y = title
            if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and speed_x == 0:
                speed_x = -title
                speed_y = 0
            if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and speed_x == 0:
                speed_x = title
                speed_y = 0

        #Проверяем количество еды на экране
        if event.type == ADD_EAT: 
            #Добавляем яблоки
            if eat.instances_count < 6:
                all_sprites.add(eat(random.randrange(title, win_width - title, title),random.randrange(title, win_height - title, title)))
                #Устанавливаем рандомное время появления следующего яблока
                pygame.time.set_timer(ADD_EAT, random.randint(100, 1500)) 

        #Проверяем столкновение с границей экрана
        if snake.rect.x >= win_width or snake.rect.x < 0 or snake.rect.y >= win_height or snake.rect.y < 0:
            draw_text(screen, f'Вы столкнулись с экраном(', 18, win_width / 2 + 300, 10)
            print('Вы столкнулись с экраном(')
            time.sleep(2)
            pygame.quit()

pygame.quit()

#тормозим терминал
#input("\nНажмите любую клавишу для завершения...")