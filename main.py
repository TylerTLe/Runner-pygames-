import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score:{current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:screen.blit(snail_surface,obstacle_rect)
            else: screen.blit(fly_surface,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list 
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

pygame.init() 
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0

sky = pygame.image.load('graphics/Sky.png').convert()
ground = pygame.image.load('graphics/Ground.png').convert()

# score_surface = test_font.render('Score:', False, (64,64,64))
# score_rect = score_surface.get_rect(center = (400,50))

# Obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()

obstacle_rect_list = []


player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_hitbox = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Runner',False, (111,196,169))
game_rect = game_name.get_rect(center = (400,75))
game_start = test_font.render('Press space to run',False, (111,196,169))
game_start_rect = game_start.get_rect(center = (400,335))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_hitbox.bottom >=300:
                    if player_hitbox.collidepoint(event.pos):
                        player_gravity = -20
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_hitbox.bottom >=300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900,1100),210)))
            

# Game screen and mechanics
    if game_active:
        # Background
        screen.blit(sky,(0,0))
        screen.blit(ground,(0,300))
        score = display_score()

        # Snail
        # snail_hitbox.x -= 4
        # if snail_hitbox.right <= 0: snail_hitbox.left = 800
        # screen.blit(snail_surface,snail_hitbox)

        # Player
        player_gravity += 1
        player_hitbox.y += player_gravity
        if player_hitbox.bottom >= 300: player_hitbox.bottom = 300
        screen.blit(player_surface,player_hitbox)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_hitbox,obstacle_rect_list)

# Start screen
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_hitbox.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))

        screen.blit(game_name,game_rect)

        if score == 0: screen.blit(game_start,game_start_rect)
        else: screen.blit(score_message,score_message_rect)
 
    pygame.display.update()
    clock.tick(60)

