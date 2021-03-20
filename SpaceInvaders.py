import math
import random

import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()



pygame.display.set_caption('space invaders')

background = pygame.image.load('background.png')

score = 0
previous_score = 0
score_font = pygame.font.Font('arcade_weknow/ARCADE.otf', 32)
textX = 10
testY = 10

# intro
intro = True
intro_text = "SpaceInvaders"
intro_font = pygame.font.Font('arcade_weknow/ARCADE.otf', 64)
intro_font2 = pygame.font.Font('arcade_weknow/ARCADE.otf', 64)

# PlayButton
play_button = pygame.image.load('play-button.png')
play_button_X = (SCREEN_WIDTH / 2) - play_button.get_width()
play_button_Y = (SCREEN_HEIGHT / (4 / 3)) - play_button.get_height()

# GameOver
gameover = False
gameover_text = "Game Over"
replay_button = pygame.image.load('replay.png')

# player
player_image = pygame.image.load('spaceship.png')
player_X = 370
player_Y = 480
player_movement = 0

# bullet
bullet_image = pygame.image.load('hot.png')
bullet_X = []
bullet_Y = []
bullet_movement = 0.7
bullet_fired = []
num_bullet = 1
for i in range(num_bullet):
    bullet_X.append(0)
    bullet_Y.append(player_Y)
    bullet_fired.append(False)

# enemy
enemy_image = pygame.image.load('ufo.png')
enemy_X = []
enemy_Y = []
enemy_X_movement = []
enemy_Y_movement = 40
num_enemies = 2

# gamespeedincrement
gamespeed = 0
gamespeed_increment = 0.05

for i in range(num_enemies):
    enemy_X.append(random.randint(0, 736))
    enemy_Y.append(random.randint(50, 150))
    enemy_X_movement.append(0.2)


def player(x, y):
    screen.blit(player_image, (x, y))


def fire_bullet(x, y, n):
    global bullet_fired
    bullet_fired[n] = True
    screen.blit(bullet_image, (x + 16, y + 10))


def add_bullet():
    global num_bullet
    num_bullet += 1
    bullet_X.append(0)
    bullet_Y.append(player_Y)
    bullet_fired.append(False)


def spawn_enemy(x, y):
    screen.blit(enemy_image, (x, y))


def add_enemy():
    global num_enemies
    enemy_X.append(random.randint(0, 736))
    enemy_Y.append(random.randint(50, 150))
    enemy_X_movement.append(0.2)
    num_enemies += 1


def reset_enemy(index):
    enemy_X[index] = random.randint(0, 736)
    enemy_Y[index] = random.randint(50, 150)
    enemy_X_movement[index] = 0.2


def reset_bullet(n):
    global bullet_fired, bullet_Y
    bullet_fired[n] = False
    bullet_Y[n] = player_Y


def isCollion(eX, eY, bX, bY):
    distance = math.sqrt(math.pow(eX - bX, 2) + (math.pow(eY - bY, 2)))
    if distance < 27:
        return True
    else:
        return False


def show_score():
    text = score_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (textX, testY))


def show_intro():
    show_big_text(intro_text)
    show_play_button()


def show_big_text(s):
    text = intro_font.render(s, True, (89, 203, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
    text2 = intro_font2.render(s, True, (250, 50, 183))
    text_rect2 = text.get_rect(center=((SCREEN_WIDTH / 2) + 3, (SCREEN_HEIGHT / 2) + 3))
    screen.blit(text2, text_rect2)


def show_play_button():
    screen.blit(play_button, (play_button_X, play_button_Y))


def show_replay_button():
    screen.blit(replay_button, (play_button_X, play_button_Y))


def play_button_clicked():
    click = pygame.mouse.get_pressed()
    if click[0] == 1:
        pos = pygame.mouse.get_pos()
        if play_button_X < pos[0] < play_button_X + play_button.get_width():
            if play_button_Y < pos[1] < play_button_Y + play_button.get_height():
                return True
    return False


def game_over_screen():
    show_big_text(gameover_text)
    show_score()
    show_replay_button()


def reset():
    global num_enemies, enemy_X, enemy_Y, player_X, player_Y, score, bullet_fired, gamespeed, num_bullet, bullet_X, bullet_Y
    num_enemies = 2
    enemy_X = []
    enemy_Y = []
    for i in range(num_enemies):
        enemy_X.append(random.randint(0, 736))
        enemy_Y.append(random.randint(50, 150))
        enemy_X_movement.append(2)
    player_X = 370
    player_Y = 480
    score = 0
    bullet_fired = []
    bullet_fired.append(False)
    gamespeed = 0
    num_bullet = 1
    bullet_X = []
    bullet_X.append(0)
    bullet_Y = []
    bullet_Y.append(player_Y)


running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    dt = clock.tick(60)

    while intro:
        show_intro()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if play_button_clicked():
            intro = False

        pygame.display.update()

    while gameover:
        game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if play_button_clicked():
            reset()
            gameover = False

        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_movement = -0.2 - gamespeed
            if event.key == pygame.K_RIGHT:
                player_movement = 0.2 + gamespeed
            if event.key == pygame.K_SPACE:
                for i in range(num_bullet):
                    if not bullet_fired[i]:
                        bullet_X[i] = player_X
                        fire_bullet(bullet_X[i], bullet_Y[i], i)
                        break
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_movement = 0

    # playermovement
    player_X += player_movement * dt
    if player_X <= 1:
        player_X = 1
    elif player_X >= 735:
        player_X = 735

    # bulletmovement
    for i in range(num_bullet):
        if bullet_Y[i] <= 1:
            reset_bullet(i)
        if bullet_fired[i]:
            bullet_Y[i] -= bullet_movement * dt
            fire_bullet(bullet_X[i], bullet_Y[i], i)

    # enemy_movement
    for i in range(num_enemies):
        if enemy_Y[i] >= 440:
            gameover = True

        for j in range(num_bullet):
            if bullet_fired[j]:
                collision = isCollion(enemy_X[i], enemy_Y[i], bullet_X[j], bullet_Y[j])
                if collision:
                    reset_enemy(i)
                    reset_bullet(j)
                    score += 1

        if score != 0 and previous_score != score:
            if score % 3 == 0:
                add_enemy()
                print("added enemy")
            if score % 10 == 0:
                gamespeed += gamespeed_increment
                print("increased gamespeed")
            if score % 20 == 0:
                add_bullet()
                print("added bullet")
            previous_score = score

        if enemy_X_movement[i] < 0:
            enemy_X[i] += (enemy_X_movement[i] - gamespeed) * dt
        else:
            enemy_X[i] += (enemy_X_movement[i] + gamespeed) * dt
        if enemy_X[i] <= 1:
            enemy_X[i] = 2
            enemy_X_movement[i] = -enemy_X_movement[i]
            enemy_Y[i] += (enemy_Y_movement + gamespeed)
        elif enemy_X[i] >= 735:
            enemy_X[i] = 734
            enemy_X_movement[i] = -enemy_X_movement[i]
            enemy_Y[i] += (enemy_Y_movement + gamespeed)

        spawn_enemy(enemy_X[i], enemy_Y[i])

    player(player_X, player_Y)
    show_score()
    pygame.display.update()
