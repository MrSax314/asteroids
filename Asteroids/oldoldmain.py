import pygame
import math

# Initialize pygame
pygame.init()

# Screen Creation / Caption and Icon
ScreenHeight = 600
ScreenWidth = 800
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
icon = pygame.image.load("ship.png")
pygame.display.set_caption("Asteroids")
pygame.display.set_icon(icon)

# Player data
playerImg = [pygame.image.load("ship-uuu.png"), pygame.image.load("ship-lll.png"), pygame.image.load("ship-ddd.png"),
             pygame.image.load("ship-rrr.png")]
playerX = 370
playerY = 300
player_speed = 0.2
playerX_change = 0
playerY_change = 0
player_direction = 0
score = 0

# Asteroid data
asteroidImg1 = pygame.image.load("asteroid1.png")
asteroidImg2 = pygame.image.load("asteroid3.png")
asteroidImg3 = pygame.image.load("asteroid5.png")
asteroidX = 370
asteroidY = 100
asteroidX_change = 0
asteroidY_change = 0

# Bullet data declaration
bulletImg = []
bulletX = []
bulletY = []
bullet_speed = []
bulletX_change = []
bulletY_change = []
bullet_state = []
num_of_bullets = 1

# Bullet data assignment
for i in range(num_of_bullets):
    bulletImg.append(pygame.image.load("pew.png"))
    bulletX.append(450)
    bulletY.append(700)
    bullet_speed.append(0.5)
    # bulletX_change.append(0)
    bulletY_change.append(0.5)
    bullet_state.append("ready")

# Score values
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 16)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y, direction):  # Direction 0 -> 28 (0 - 3)
    screen.blit(playerImg[direction], (x, y))


def asteroid(x, y):
    screen.blit(asteroidImg1, (x, y))


def fire_bullet(x, y, i):
    # global bullet_state
    bullet_state[i] = "fire"
    screen.blit(bulletImg[i], (x + 16, y + 10))


def isCollision(asteroidX, asteroidY, bulletX, bulletY):
    distance = math.sqrt((math.pow(asteroidX - bulletX, 2)) + (math.pow(asteroidY - bulletY, 2)))
    if distance < 15:
        return True
    else:
        return False

def iCollision(asteroidX, asteroidY, objectX, objectY, type):  # asteroid[j].get_px(), asteroid[j].get_py(), bullet[i].get_px(), bullet[i].get_py(), 'b'
    if type == 'b':  # Bullet dist check  TODO shorten code here! it is possoble (the nested ifs)
        distance = math.sqrt((math.pow(asteroidX + 16 - objectX, 2)) + (math.pow(asteroidY + 16 - objectY, 2)))
    if type == 'p':  # Player dist check
        distance = math.sqrt(
            (math.pow(asteroidX + 16 - (objectX + 16), 2)) + (math.pow(asteroidY + 16 - (objectY + 16), 2)))
    if distance < 15 and type == 'b':  # TODO conditional on size of asteroid
        return True
    elif distance < 21 and type == 'p':
        explosion_sound = mixer.Sound('boom.wav')
        explosion_sound.play()
        return True
    else:
        return False

# Game Loop
running = True
while running:

    # Screen layer
    screen.fill((0, 0, 0))  # RGB Tuple

    # Test for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key Tests
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerImg
                playerX_change = -player_speed
            if event.key == pygame.K_RIGHT:
                playerX_change = player_speed
            if event.key == pygame.K_UP:
                playerY_change = -player_speed
            if event.key == pygame.K_DOWN:
                playerY_change = player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state[0] == "ready":
                    bulletX[0] = playerX
                    fire_bullet(bulletX[0], bulletY[0], 0)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
            if event.key == pygame.K_SPACE:
                # bullet_state[0] = "ready"
                pass

    playerX += playerX_change
    playerY += playerY_change

    # Player layer
    player(playerX, playerY, direction)
    show_score(textX, textY)
    # Asteroids
    asteroid(asteroidX, asteroidY)

    # Bullet movement
    for i in range(num_of_bullets):
        if bulletY[i] <= 0:
            bulletY[i] = 480
            bullet_state[i] = "ready"

        if bullet_state[i] is "fire":
            fire_bullet(bulletX[i], bulletY[i], i)
            bulletY[i] = bulletY[i] - bulletY_change[i]

        # Collision
        collision = isCollision(asteroidX, asteroidY, bulletX[i], bulletY[i])
        if collision:
            bulletY[i] = 480
            bullet_state[i] = "ready"
            score_value += 1

    # Bounds check
    if playerX <= -7:
        playerX = -7
    elif playerX >= 774:
        playerX = 774
    if playerY <= 0:
        playerY = 0
    elif playerY >= 573:
        playerY = 573

    # Update
    pygame.display.update()