# РЕФАКТОРИНГ
import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    ''' Отслеживание нажатия клавиш '''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    ''' Отслеживание отпускания клавиш '''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ship,bullets,ai_settings,screen):
    '''Отслеживание событий клавиатуры и мыши'''
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event,ai_settings,screen,ship,bullets)                 
            elif event.type == pygame.KEYUP:
                check_keyup_events(event,ship)
            
def update_screen(ai_settings,screen,ship,aliens,bullets):
    ''' Обновляет изоображение на экране и отображает новый экран '''
    # цвет экрана
    screen.fill(ai_settings.bg_color)
    # отрисовка пуль находящихся в группе
    for bullet in bullets.sprites():
        bullet.blitme()
    # Отрисовка коробля
    ship.blitme()
    # на экран русуются все пришельцы находящиеся в группе в текущей позиции
    aliens.draw(screen)
    # «Отображение последнего прорисованного экрана.»  
    pygame.display.flip()

def update_bullets(ai_settings, screen , ship, aliens, bullets):
    ''' Обновляет позиции пуль и удаляет старые пули '''
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # проверка попаданий в пришельцев
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    ''' Обнуружение колизий пуль с пришельцами '''
    # при обноружение удаляет пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # уничтожение оставшихся пуль и создание нового флота
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
    
def fire_bullet(ai_settings,screen,ship,bullets):
    ''' Выстрел пули если максимум еще не достигнут '''
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
        
def get_number_aliens_x(ai_settings,alien_width):
    ''' Получение количества пришельцев в ряду '''
    # вычисление пришельцев в ряду 
    # интервал между пришельцами равен ширене одного пришельца
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    ''' Получение количества рядов помещающихся на экран '''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien (ai_settings,screen,aliens,alien_number,row_number):
    ''' Создание пришельца ,  размещение и добавление в группу '''
    # создание пришельца и размещения его в ряду 
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    ''' Создает флот пришельцев '''
    # создание пришельца и вычесления количества в ряду
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        # создание первого ряда пришельцев
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    ''' Обрабытывает столкновения коробля с пришельцами '''
    if stats.ship_left > 0 :
        # уменьшение ship_left
        stats.ship_left -= 1
        # очиста списка пришельцев и пуль
        aliens.empty()
        bullets.empty()
        # создание нового флота и размещение коробля в центре 
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # пауза
        sleep(0.5)
    else :
        stats.game_active = False

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets): 
    """Проверяет, добрались ли пришельцы до нижнего края экрана.""" 
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что при столкновении с кораблем.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    ''' Проверяет достиг ли флот экрана , обновляет позиции всех пришельцев во флоте '''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # проверяет колизии пришелец - корабль
    if pygame.sprite.spritecollide(ship, aliens, None):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    ''' Реагирует на достижения пришельца края экрана '''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_diraction(ai_settings,aliens)
            break

def change_fleet_diraction(ai_settings, aliens):
    ''' Опускает весь флот и меняет направление '''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_diraction *= -1





    