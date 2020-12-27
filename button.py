import pygame.font

class Button():

    ''' класс создания кнопки '''

    def __init__(self, ai_settings, screen, msg):
        ''' инициализирует атрибуты кнопки '''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # назначение размеров и свойств кнопок
        self.width, self.height = 200 , 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # построение обьекта рект кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # сообщение кнопки создается только один раз
        self.prep_msg(msg)