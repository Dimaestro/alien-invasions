import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    
    ''' Класс для управления пулями выпущиных короблем '''
    
    def __init__(self,ai_settings,screen,ship):
        ''' Создает обьект пули в текущей позиции коробля '''
        # Правильное наследование от класса Sprite
        super().__init__()
        # создание экрана
        self.screen = screen
        # загрузка изоображения и создания поверхности для него
        self.image = pygame.image.load('images/bullet.bmp')     
        self.rect = self.image.get_rect()                      
        self.screen_rect = screen.get_rect()
        # местоположение пули относительно коробля 
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        # скорость полета пули 
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        ''' Перемещает пулю вверх по экрану '''
        self.y -= self.speed_factor
        self.rect.y = self.y
    
    def blitme(self):
        ''' Вывод пули на экран '''
        self.screen.blit(self.image, self.rect)
