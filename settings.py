class Settings():
    
    ''' Класс для хранения всех настроек игры Alien_invasions'''

    def __init__(self):
        ''' Инициализирует настройки игры '''
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (45,46,58)
        # параметр коробля 
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # Параметры пули
        self.bullet_speed_factor = 3
        # разрешеное количество пуль на экране
        self.bullet_allowed = 3
        # настройки пришельцев 
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10              # снижение флота
        self.fleet_diraction = 1                # обозначает движение в право , а - 1 влево
        
    