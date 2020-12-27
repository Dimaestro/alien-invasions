class GameStats():

    '''Отслеживание статистики за всю игру Alien Invasions '''
    
    def __init__(self, ai_settings):
        ''' Инициализирует статистику '''
        self.ai_settings = ai_settings
        self.reset_stats()
        # игра запускается в активном состоянии 
        self.game_active = True

    def reset_stats(self):
        ''' Инициализирует стаистику меняющуюсь в ходе игры '''
        self.ship_left = self.ai_settings.ship_limit