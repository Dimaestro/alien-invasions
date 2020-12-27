import pygame

class Ship():
    
    ''' class Ship '''
    
    def __init__(self,ai_settings,screen):
        ''' Инициализирует корабль и задает его начальную позицию '''
        self.screen = screen
        self.ai_settings = ai_settings
        # загрузка картинки и создания поверхнисти в виде прямоугольника 
        self.image = pygame.image.load('images/ship.bmp')     
        self.rect = self.image.get_rect()                      
        self.screen_rect = screen.get_rect()
        # Обьект находится внизу экрна
        self.rect.centerx = self.screen_rect.centerx           
        self.rect.bottom = self.screen_rect.bottom
        # сохранение вещественной координаты коробля
        self.center = float(self.rect.centerx)
        # Флаг перемещения 
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        ''' Рисует корабль в текущей позиции '''
        self.screen.blit(self.image, self.rect)

    def update(self):
        ''' Обновляет позицию коробля с учетом флага '''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        # обновляет значение координат
        self.rect.centerx = self.center

    def center_ship(self):
        ''' размещает корабль в центре '''
        self.center = self.screen_rect.centerx
