import math
import time
import pygame
import random
import os
from pygame import mixer
from objects import obj

# Initialize pygame
pygame.init()

# Screen Creation / Caption and Icon
ScreenHeight = 600
ScreenWidth = 800

screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
current_path = os.path.dirname('F:/4 Scripts/asteroids/Asteroids/') # Where your .py file is located
print(current_path)
resource_path = os.path.join(current_path, 'resources') # The resource folder path
icon = pygame.image.load(os.path.join(resource_path,"ship.png"))
pygame.display.set_caption("Asteroids")
pygame.display.set_icon(icon)

# Level data
game_level = 0

# Player data # TODO less code here plz thx
# Rotation variables
turning_speed = 100  # Larger = Slower
count_l = 0
count_r = 0

# Player sprites for each direction 0(TDC)-24(TDC+15 degrees)
'''
playerImg = [pygame.image.load("ship-uuu.png"), pygame.image.load("ship-1.png"), pygame.image.load("ship-uuu.png"),
             pygame.image.load("ship-uuu.png"), pygame.image.load("ship-lll.png"), pygame.image.load("ship-lll.png"),
             pygame.image.load("ship-lll.png"), pygame.image.load("ship-lll.png"), pygame.image.load("ship-lll.png"),
             pygame.image.load("ship-ddd.png"), pygame.image.load("ship-ddd.png"), pygame.image.load("ship-ddd.png"),
             pygame.image.load("ship-ddd.png"), pygame.image.load("ship-ddd.png"), pygame.image.load("ship-ddd.png"),
             pygame.image.load("ship-ddd.png"), pygame.image.load("ship-rrr.png"), pygame.image.load("ship-rrr.png"),
             pygame.image.load("ship-rrr.png"), pygame.image.load("ship-rrr.png"), pygame.image.load("ship-rrr.png"),
             pygame.image.load("ship-uuu.png"), pygame.image.load("ship-uuu.png"), pygame.image.load("ship-uuu.png"), ]
'''
playerImg = [pygame.image.load(os.path.join(resource_path,"ship-0.png")), pygame.image.load(os.path.join(resource_path,"ship-1.png")), pygame.image.load(os.path.join(resource_path,"ship-2.png")),
             pygame.image.load(os.path.join(resource_path,"ship-3.png")), pygame.image.load(os.path.join(resource_path,"ship-4.png")), pygame.image.load(os.path.join(resource_path,"ship-5.png")),
             pygame.image.load(os.path.join(resource_path,"ship-6.png")), pygame.image.load(os.path.join(resource_path,"ship-7.png")), pygame.image.load(os.path.join(resource_path,"ship-8.png")),
             pygame.image.load(os.path.join(resource_path,"ship-9.png")), pygame.image.load(os.path.join(resource_path,"ship-10.png")), pygame.image.load(os.path.join(resource_path,"ship-11.png")),
             pygame.image.load(os.path.join(resource_path,"ship-12.png")), pygame.image.load(os.path.join(resource_path,"ship-13.png")), pygame.image.load(os.path.join(resource_path,"ship-14.png")),
             pygame.image.load(os.path.join(resource_path,"ship-15.png")), pygame.image.load(os.path.join(resource_path,"ship-16.png")), pygame.image.load(os.path.join(resource_path,"ship-17.png")),
             pygame.image.load(os.path.join(resource_path,"ship-18.png")), pygame.image.load(os.path.join(resource_path,"ship-19.png")), pygame.image.load(os.path.join(resource_path,"ship-20.png")),
             pygame.image.load(os.path.join(resource_path,"ship-21.png")), pygame.image.load(os.path.join(resource_path,"ship-22.png")), pygame.image.load(os.path.join(resource_path,"ship-23.png"))]

# playerImg = [pygame.image.load("ship-uuu.png"), pygame.image.load("ship-lll.png"), pygame.image.load("ship-ddd.png"),
# pygame.image.load("ship-rrr.png")]
player = obj(370, 300, vx=0, vy=0)
friction = 0.00001
speed_limit = 1
acc = 0.0005
score = 0

# Asteroid data
asteroid = []
num_of_asteroids = 3
num_of_asteroids_added = 0
asteroid_speed_max = 0.1
asteroid_speed_min = 0.02
asteroidImg = [0, [pygame.image.load(os.path.join(resource_path,"asteroid6.png")), pygame.image.load(os.path.join(resource_path,"asteroid5.png"))],
               [pygame.image.load(os.path.join(resource_path,"asteroid4.png")), pygame.image.load(os.path.join(resource_path,"asteroid3.png"))],
               [pygame.image.load(os.path.join(resource_path,"asteroid2.png")), pygame.image.load(os.path.join(resource_path,"asteroid1.png"))]]

# Asteroid creation
for i in range(num_of_asteroids):
    # asteroid.append(obj(370, 100, 0, 0))   # TODO be sure that asteroids don't spawn on player at spawn
    # or obj(random.randint(0, 768), random.randint(0, 668), random.uniform(asteroid_speed_min, asteroid_speed_max),
    # random.uniform(asteroid_speed_min, asteroid_speed_max)))
    asteroid.append(
        obj(random.randint(0, 768), random.randint(0, 568), random.uniform(asteroid_speed_min, asteroid_speed_max),
            random.uniform(asteroid_speed_min, asteroid_speed_max)))
    if asteroid[i].get_px() > 200 and asteroid[i].get_px() < 600 and asteroid[i].get_py() > 100 and asteroid[
        i].get_py() < 400:  # 300 500 200 400
        asteroid[i].set_pos(random.randint(1, 300), random.randint(1, 200))
    asteroid[i].set_state(3)  # random.randint(1, 3)

# Bullet data declaration
bullet = []
bulletImg = pygame.image.load(os.path.join(resource_path,"pew.png"))
num_of_bullets = 9
bullet_speed = 0.5

# Bullet data assignment
for i in range(num_of_bullets):
    bullet.append(obj(450, 700, 0, 0))

# Bullet velocity/initial position decoder dict - because you cant rotate sprites with pygame :(
num_of_sprites = 28
decoder = {  # TODO make this dict a function!
    0: {'px': 16, 'py': 0, 'vx': math.cos(math.pi / 2), 'vy': math.sin(math.pi / 2)},

    1: {'px': 13, 'py': 3, 'vx': math.cos(math.pi * 7 / 12), 'vy': math.sin(math.pi * 7 / 12)},
    2: {'px': 11, 'py': 5, 'vx': math.cos(math.pi * 8 / 12), 'vy': math.sin(math.pi * 8 / 12)},
    3: {'px': 8, 'py': 8, 'vx': math.cos(math.pi * 9 / 12), 'vy': math.sin(math.pi * 9 / 12)},
    4: {'px': 5, 'py': 11, 'vx': math.cos(math.pi * 10 / 12), 'vy': math.sin(math.pi * 10 / 12)},
    5: {'px': 3, 'py': 13, 'vx': math.cos(math.pi * 11 / 12), 'vy': math.sin(math.pi * 11 / 12)},

    6: {'px': 0, 'py': 16, 'vx': math.cos(math.pi), 'vy': math.sin(math.pi)},

    7: {'px': 3, 'py': 19, 'vx': math.cos(math.pi * 13 / 12), 'vy': math.sin(math.pi * 13 / 12)},
    8: {'px': 5, 'py': 21, 'vx': math.cos(math.pi * 14 / 12), 'vy': math.sin(math.pi * 14 / 12)},
    9: {'px': 8, 'py': 24, 'vx': math.cos(math.pi * 15 / 12), 'vy': math.sin(math.pi * 15 / 12)},
    10: {'px': 11, 'py': 27, 'vx': math.cos(math.pi * 16 / 12), 'vy': math.sin(math.pi * 16 / 12)},
    11: {'px': 13, 'py': 29, 'vx': math.cos(math.pi * 17 / 12), 'vy': math.sin(math.pi * 17 / 12)},

    12: {'px': 16, 'py': 32, 'vx': math.cos(math.pi * 18 / 12), 'vy': math.sin(math.pi * 18 / 12)},

    13: {'px': 19, 'py': 29, 'vx': math.cos(math.pi * 19 / 12), 'vy': math.sin(math.pi * 19 / 12)},
    14: {'px': 21, 'py': 27, 'vx': math.cos(math.pi * 20 / 12), 'vy': math.sin(math.pi * 20 / 12)},
    15: {'px': 24, 'py': 24, 'vx': math.cos(math.pi * 21 / 12), 'vy': math.sin(math.pi * 21 / 12)},
    16: {'px': 27, 'py': 21, 'vx': math.cos(math.pi * 22 / 12), 'vy': math.sin(math.pi * 22 / 12)},
    17: {'px': 29, 'py': 19, 'vx': math.cos(math.pi * 23 / 12), 'vy': math.sin(math.pi * 23 / 12)},

    18: {'px': 32, 'py': 16, 'vx': math.cos(math.pi * 2), 'vy': math.sin(math.pi * 2)},

    19: {'px': 29, 'py': 13, 'vx': math.cos(math.pi * 1 / 12), 'vy': math.sin(math.pi * 1 / 12)},
    20: {'px': 27, 'py': 11, 'vx': math.cos(math.pi * 2 / 12), 'vy': math.sin(math.pi * 2 / 12)},
    21: {'px': 24, 'py': 8, 'vx': math.cos(math.pi * 3 / 12), 'vy': math.sin(math.pi * 3 / 12)},
    22: {'px': 21, 'py': 5, 'vx': math.cos(math.pi * 4 / 12), 'vy': math.sin(math.pi * 4 / 12)},
    23: {'px': 19, 'py': 3, 'vx': math.cos(math.pi * 5 / 12), 'vy': math.sin(math.pi * 5 / 12)}}

# Score values / text
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 16)
textX = 10
textY = 10

# Game text font
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
game_start_font = pygame.font.Font('freesansbold.ttf', 32)


# TODO Start level lives, game_pause function
def game_over():
    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))
    player.set_state(1)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def blit_player(x, y, direction):  # Direction 0 -> 23
    screen.blit(playerImg[direction], (x, y))  # playerImg[0]


def blit_asteroid(x, y, state):  # Only receives  1<= states <=3
    screen.blit(asteroidImg[state][0], (x, y))


def blit_bullet(x, y, i):
    # global bullet_state
    bullet[i].set_state(1)  # 1=fire
    screen.blit(bulletImg, (x, y))  # screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(obj1, obj2, type):  # obj1 = asteroid  obj2 = player or bullet
    if type == 'b':  # Bullet dist check
        distance = math.sqrt(
            (math.pow(obj1.get_px() + 16 - obj2.get_px(), 2)) + (math.pow(obj1.get_py() + 16 - obj2.get_py(), 2)))
        if distance > 15 and obj1.get_state() == 3:  # TODO conditional on size of asteroid
            return False
        elif distance > 11 and obj1.get_state() == 2:
            return False
        elif distance > 7 and obj1.get_state() == 1:
            return False
        else:
            return True
    if type == 'p':  # Player dist check
        # print(asteroid[1].get_px())
        a = asteroid[1].get_px()
        b = obj2.get_px()
        c = obj1.get_py()
        d = obj2.get_py()
        z = a + 16
        x = (z) - (b + 16)
        y = (c + 16) - (d + 16)
        distance = math.sqrt(
            math.pow((x), 2) +
            math.pow((y), 2))
        if distance < 23:
            explosion_sound = mixer.Sound('boom.wav')
            explosion_sound.play()
            return True
        else:
            return False


def iCollision(asteroidX, asteroidY, objectX, objectY, type,
               i):  # asteroid[j].get_px(), asteroid[j].get_py(), bullet[i].get_px(), bullet[i].get_py(), 'b'
    if type == 'b':  # Bullet dist check  TODO shorten code here! it is possoble (the nested ifs)
        distance = math.sqrt((math.pow(asteroidX + 16 - objectX, 2)) + (math.pow(asteroidY + 16 - objectY, 2)))
        if distance > 15 and asteroid[i].get_state() == 3:  # TODO conditional on size of asteroid
            return False
        elif distance > 11 and asteroid[i].get_state() == 2:
            return False
        elif distance > 7 and asteroid[i].get_state() == 1:
            return False
        else:
            return True
    if type == 'p':  # Player dist check
        distance = math.sqrt(
            (math.pow(asteroidX + 16 - (objectX + 16), 2)) + (math.pow(asteroidY + 16 - (objectY + 16), 2)))

        if distance < 21 and type == 'p':
            explosion_sound = mixer.Sound('boom.wav')
            explosion_sound.play()
            return True
        else:
            return False


def decode():
    pass


def split_asteroid(i, total_asteroids):
    asteroid.append(  # @ index 1 + num_of_asteroids
        obj(asteroid[i].get_px, asteroid[i].get_py, random.uniform(asteroid_speed_min, asteroid_speed_max),
            random.uniform(asteroid_speed_min, asteroid_speed_max)))
    '''
    asteroid.append(  # @ index 1 + num_of_asteroids
        obj(asteroid[i].get_px, asteroid[i].get_py, random.uniform(asteroid_speed_min, asteroid_speed_max),
            random.uniform(asteroid_speed_min, asteroid_speed_max)))
    '''
    asteroid[-1].set_state(asteroid[i].get_state() - 1)
    asteroid[i].set_state(0)  # random.randint(1, 3)
    total_asteroids += 1  # if asteroid[i] =        num_of_asteroids = 3
    return total_asteroids


def next_level():  # base off level (num of asteroids and size)- re set asteroid states and randomize vel and pos
    if game_level == 2:
        asteroid.append(
            obj(random.randint(0, 768), random.randint(0, 568), random.uniform(asteroid_speed_min, asteroid_speed_max),
                random.uniform(asteroid_speed_min, asteroid_speed_max)))
        for i in range(num_of_asteroids):
            # asteroid.append(obj(370, 100, 0, 0))   # TODO be sure that asteroids don't spawn on player at spawn
            asteroid[i].set_pos(random.randint(0, 768), random.randint(0, 568))
            asteroid[i].set_vel(random.uniform(asteroid_speed_min, asteroid_speed_max),
                                random.uniform(asteroid_speed_min, asteroid_speed_max))
            if asteroid[i].get_px() > 300 or asteroid[i].get_px() < 500 and asteroid[i].get_py() > 200 or asteroid[
                i].get_py() < 400:
                asteroid[i].set_pos(asteroid[i].get_px() + 200, asteroid[i].get_py() + 200)
            asteroid[i].set_state(3)  # random.randint(1, 3)
    if game_level == 3:
        asteroid.append(
            obj(random.randint(0, 768), random.randint(0, 568), random.uniform(asteroid_speed_min, asteroid_speed_max),
                random.uniform(asteroid_speed_min, asteroid_speed_max)))
        asteroid.append(
            obj(random.randint(0, 768), random.randint(0, 568), random.uniform(asteroid_speed_min, asteroid_speed_max),
                random.uniform(asteroid_speed_min, asteroid_speed_max)))
        for i in range(num_of_asteroids):
            # asteroid.append(obj(370, 100, 0, 0))   # TODO be sure that asteroids don't spawn on player at spawn
            asteroid[i].set_pos(random.randint(0, 768), random.randint(0, 668))
            asteroid[i].set_vel(random.uniform(asteroid_speed_min, asteroid_speed_max),
                                random.uniform(asteroid_speed_min, asteroid_speed_max))
            if asteroid[i].get_px() > 300 or asteroid[i].get_px() < 500 and asteroid[i].get_py() > 200 or asteroid[
                i].get_py() < 400:
                asteroid[i].set_pos(asteroid[i].get_px() + 200, asteroid[i].get_py() + 200)
            asteroid[i].set_state(3)  # random.randint(1, 3)
    if game_level == 4:
        win()


running = True


def win():
    running = False
    game_level = -1
    print("winner winner chicken dinner")
    time.sleep(5)
    pygame.quit()


# Key constant on
udown = "False"
ldown = "False"
ddown = "False"
rdown = "False"
ct = 0

# Start screen loop
while game_level == 0:
    # Screen layer
    screen.fill((0, 0, 0))  # RGB Tuple
    game_start_text = game_over_font.render("Press any button to start!", True, (255, 255, 255))
    screen.blit(game_start_text, (0, 250))
    game_start_text2 = game_start_font.render("Arrow keys to move, Space bar to shoot!", True, (255, 255, 255))
    screen.blit(game_start_text2, (100, 350))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            game_level = -1
        if event.type == pygame.KEYDOWN:  # Add velocity vector components to player velocity
            game_level = 1
    pygame.display.update()

# Game Loop
running = True
while running and game_level > 0:
    print(game_level)
    # Screen layer
    screen.fill((0, 0, 0))  # RGB Tuple

    # Test for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key down test
        if event.type == pygame.KEYDOWN:  # Add velocity vector components to player velocity
            if event.key == pygame.K_UP:
                udown = "True"
                if player.get_direction() == 0:
                    player.set_vel(player.get_vx() + (acc * decoder[0]['vx']),
                                   player.get_vy() + (acc * decoder[0]['vy']))
                if player.get_direction() == 1:
                    player.set_vel(player.get_vx() + (acc * decoder[1]['vx']),
                                   player.get_vy() + (acc * decoder[1]['vy']))
                if player.get_direction() == 2:
                    player.set_vel(player.get_vx() + (acc * decoder[2]['vx']),
                                   player.get_vy() + (acc * decoder[2]['vy']))
                if player.get_direction() == 3:
                    player.set_vel(player.get_vx() + (acc * decoder[3]['vx']),
                                   player.get_vy() + (acc * decoder[3]['vy']))
                if player.get_direction() == 4:
                    player.set_vel(player.get_vx() + (acc * decoder[4]['vx']),
                                   player.get_vy() + (acc * decoder[4]['vy']))
                if player.get_direction() == 5:
                    player.set_vel(player.get_vx() + (acc * decoder[5]['vx']),
                                   player.get_vy() + (acc * decoder[5]['vy']))
                if player.get_direction() == 6:
                    player.set_vel(player.get_vx() + (acc * decoder[6]['vx']),
                                   player.get_vy() + (acc * decoder[6]['vy']))
                if player.get_direction() == 7:
                    player.set_vel(player.get_vx() + (acc * decoder[7]['vx']),
                                   player.get_vy() + (acc * decoder[7]['vy']))
                if player.get_direction() == 8:
                    player.set_vel(player.get_vx() + (acc * decoder[8]['vx']),
                                   player.get_vy() + (acc * decoder[8]['vy']))
                if player.get_direction() == 9:
                    player.set_vel(player.get_vx() + (acc * decoder[9]['vx']),
                                   player.get_vy() + (acc * decoder[9]['vy']))
                if player.get_direction() == 10:
                    player.set_vel(player.get_vx() + (acc * decoder[10]['vx']),
                                   player.get_vy() + (acc * decoder[10]['vy']))
                if player.get_direction() == 11:
                    player.set_vel(player.get_vx() + (acc * decoder[11]['vx']),
                                   player.get_vy() + (acc * decoder[11]['vy']))

                if player.get_direction() == 12:
                    player.set_vel(player.get_vx() + (acc * decoder[12]['vx']),
                                   player.get_vy() + (acc * decoder[12]['vy']))

                if player.get_direction() == 13:
                    player.set_vel(player.get_vx() + (acc * decoder[13]['vx']),
                                   player.get_vy() + (acc * decoder[13]['vy']))
                if player.get_direction() == 14:
                    player.set_vel(player.get_vx() + (acc * decoder[14]['vx']),
                                   player.get_vy() + (acc * decoder[14]['vy']))
                if player.get_direction() == 15:
                    player.set_vel(player.get_vx() + (acc * decoder[15]['vx']),
                                   player.get_vy() + (acc * decoder[15]['vy']))
                if player.get_direction() == 16:
                    player.set_vel(player.get_vx() + (acc * decoder[16]['vx']),
                                   player.get_vy() + (acc * decoder[16]['vy']))
                if player.get_direction() == 17:
                    player.set_vel(player.get_vx() + (acc * decoder[17]['vx']),
                                   player.get_vy() + (acc * decoder[17]['vy']))

                if player.get_direction() == 18:
                    player.set_vel(player.get_vx() + (acc * decoder[18]['vx']),
                                   player.get_vy() + (acc * decoder[18]['vy']))

                if player.get_direction() == 19:
                    player.set_vel(player.get_vx() + (acc * decoder[19]['vx']),
                                   player.get_vy() + (acc * decoder[19]['vy']))
                if player.get_direction() == 20:
                    player.set_vel(player.get_vx() + (acc * decoder[20]['vx']),
                                   player.get_vy() + (acc * decoder[20]['vy']))
                if player.get_direction() == 21:
                    player.set_vel(player.get_vx() + (acc * decoder[21]['vx']),
                                   player.get_vy() + (acc * decoder[21]['vy']))
                if player.get_direction() == 22:
                    player.set_vel(player.get_vx() + (acc * decoder[22]['vx']),
                                   player.get_vy() + (acc * decoder[22]['vy']))
                if player.get_direction() == 23:
                    player.set_vel(player.get_vx() + (acc * decoder[23]['vx']),
                                   player.get_vy() + (acc * decoder[23]['vy']))

            if event.key == pygame.K_LEFT:
                ldown = "True"
                player.set_direction(player.get_direction() + 1)
                if player.get_direction() >= 24:
                    player.set_direction(0)

            if event.key == pygame.K_RIGHT:
                rdown = "True"
                player.set_direction(player.get_direction() - 1)
                if player.get_direction() <= -1:
                    player.set_direction(23)

            if event.key == pygame.K_SPACE:
                for i in range(num_of_bullets):  # best bullet velocty, set initial position
                    if bullet[i].get_state() == 0:
                        bullet_sound = mixer.Sound(os.path.join(resource_path,'pew.wav'))
                        bullet_sound.play()
                        bullet[i].set_px(player.get_px() + (decoder[player.get_direction()]['px']))
                        bullet[i].set_py(player.get_py() + (decoder[player.get_direction()]['py']))
                        bullet[i].set_vx((decoder[player.get_direction()]['vx'] * bullet_speed))
                        bullet[i].set_vy((decoder[player.get_direction()]['vy'] * bullet_speed))
                        blit_bullet(bullet[i].get_px(), bullet[i].get_py(), i)
                        break

            # Key tests up
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:
                udown = "False"
            if event.key == pygame.K_LEFT:
                ldown = "False"
            if event.key == pygame.K_RIGHT:
                rdown = "False"

    # Button held down test
    if udown == "True":
        if player.get_direction() == 0:
            player.set_vel(player.get_vx() + (acc * decoder[0]['vx']), player.get_vy() + (acc * decoder[0]['vy']))
        if player.get_direction() == 1:
            player.set_vel(player.get_vx() + (acc * decoder[1]['vx']), player.get_vy() + (acc * decoder[1]['vy']))
        if player.get_direction() == 2:
            player.set_vel(player.get_vx() + (acc * decoder[2]['vx']), player.get_vy() + (acc * decoder[2]['vy']))
        if player.get_direction() == 3:
            player.set_vel(player.get_vx() + (acc * decoder[3]['vx']), player.get_vy() + (acc * decoder[3]['vy']))
        if player.get_direction() == 4:
            player.set_vel(player.get_vx() + (acc * decoder[4]['vx']), player.get_vy() + (acc * decoder[4]['vy']))
        if player.get_direction() == 5:
            player.set_vel(player.get_vx() + (acc * decoder[5]['vx']), player.get_vy() + (acc * decoder[5]['vy']))
        if player.get_direction() == 6:
            player.set_vel(player.get_vx() + (acc * decoder[6]['vx']), player.get_vy() + (acc * decoder[6]['vy']))
        if player.get_direction() == 7:
            player.set_vel(player.get_vx() + (acc * decoder[7]['vx']), player.get_vy() + (acc * decoder[7]['vy']))
        if player.get_direction() == 8:
            player.set_vel(player.get_vx() + (acc * decoder[8]['vx']), player.get_vy() + (acc * decoder[8]['vy']))
        if player.get_direction() == 9:
            player.set_vel(player.get_vx() + (acc * decoder[9]['vx']), player.get_vy() + (acc * decoder[9]['vy']))
        if player.get_direction() == 10:
            player.set_vel(player.get_vx() + (acc * decoder[10]['vx']), player.get_vy() + (acc * decoder[10]['vy']))
        if player.get_direction() == 11:
            player.set_vel(player.get_vx() + (acc * decoder[11]['vx']), player.get_vy() + (acc * decoder[11]['vy']))

        if player.get_direction() == 12:
            player.set_vel(player.get_vx() + (acc * decoder[12]['vx']), player.get_vy() + (acc * decoder[12]['vy']))

        if player.get_direction() == 13:
            player.set_vel(player.get_vx() + (acc * decoder[13]['vx']), player.get_vy() + (acc * decoder[13]['vy']))
        if player.get_direction() == 14:
            player.set_vel(player.get_vx() + (acc * decoder[14]['vx']), player.get_vy() + (acc * decoder[14]['vy']))
        if player.get_direction() == 15:
            player.set_vel(player.get_vx() + (acc * decoder[15]['vx']), player.get_vy() + (acc * decoder[15]['vy']))
        if player.get_direction() == 16:
            player.set_vel(player.get_vx() + (acc * decoder[16]['vx']), player.get_vy() + (acc * decoder[16]['vy']))
        if player.get_direction() == 17:
            player.set_vel(player.get_vx() + (acc * decoder[17]['vx']), player.get_vy() + (acc * decoder[17]['vy']))

        if player.get_direction() == 18:
            player.set_vel(player.get_vx() + (acc * decoder[18]['vx']), player.get_vy() + (acc * decoder[18]['vy']))

        if player.get_direction() == 19:
            player.set_vel(player.get_vx() + (acc * decoder[19]['vx']), player.get_vy() + (acc * decoder[19]['vy']))
        if player.get_direction() == 20:
            player.set_vel(player.get_vx() + (acc * decoder[20]['vx']), player.get_vy() + (acc * decoder[20]['vy']))
        if player.get_direction() == 21:
            player.set_vel(player.get_vx() + (acc * decoder[21]['vx']), player.get_vy() + (acc * decoder[21]['vy']))
        if player.get_direction() == 22:
            player.set_vel(player.get_vx() + (acc * decoder[22]['vx']), player.get_vy() + (acc * decoder[22]['vy']))
        if player.get_direction() == 23:
            player.set_vel(player.get_vx() + (acc * decoder[23]['vx']), player.get_vy() + (acc * decoder[23]['vy']))
    # '''
    # TODO remove when more sprite angles are added

    if ldown == "True":
        count_l += 1
        if count_l > turning_speed:
            count_l = 0
            player.set_direction(player.get_direction() + 1)
            if player.get_direction() >= 24:
                player.set_direction(0)

    if rdown == "True":
        count_r += 1
        if count_r > turning_speed:
            count_r = 0
            player.set_direction(player.get_direction() - 1)
            if player.get_direction() <= -1:
                player.set_direction(23)
    # '''

    # Player state check
    if player.get_state() == 1:
        game_over()
    elif player.get_state() == 0:
        # Player speed limit
        if player.get_vx() > speed_limit:
            player.set_vx()  # put speed limit : replace 1
        if player.get_vy() > speed_limit:
            player.set_vy(1)
        if player.get_vx() < -speed_limit:
            player.set_vx(-1)
        if player.get_vy() < -speed_limit:
            player.set_vy(-1)

        # Player friction
        if player.get_vx() < 0:
            player.set_vx(player.get_vx() + friction)
        if player.get_vx() > 0:
            player.set_vx(player.get_vx() - friction)
        if player.get_vy() < 0:
            player.set_vy(player.get_vy() + friction)
        if player.get_vy() > 0:
            player.set_vy(player.get_vy() - friction)

        # Player collision check --> End credit
        for i in range(num_of_asteroids):
            if asteroid[i].get_state() >= 1:
                collision = iCollision(asteroid[i].get_px(), asteroid[i].get_py(), player.get_px(), player.get_py(),
                                       'p', i)  # nope
                # collision = isCollision(asteroid[i], player, 'p') #TODO integrate object type (player or asteroid)(child classes?)
                if collision:
                    game_over()

        # Player movement physics based on x,y velocity
        player.set_px(player.get_px() + player.get_vx())
        player.set_py(player.get_py() - player.get_vy())

        # Player bounds check round table
        if player.get_px() <= -29:
            player.set_px(795)
        elif player.get_px() >= 796:
            player.set_px(-28)
        if player.get_py() <= -22:
            player.set_py(594)
        elif player.get_py() >= 595:
            player.set_py(-21)

        # Player layer (blit)
        blit_player(player.get_px(), player.get_py(), player.get_direction())
        show_score(textX, textY)
        # player.debug()
        # print("      ", decoder[player.get_direction()]['vx'])

    # Asteroid movement physics
    for i in range(num_of_asteroids):
        if asteroid[i].get_state() >= 1:
            # Asteroid movement
            asteroid[i].set_px(asteroid[i].get_px() + asteroid[i].get_vx())
            asteroid[i].set_py(asteroid[i].get_py() - asteroid[i].get_vy())

            # Asteroid round table
            if asteroid[i].get_px() <= -29:
                asteroid[i].set_px(795)
            elif asteroid[i].get_px() >= 796:
                asteroid[i].set_px(-28)
            if asteroid[i].get_py() <= -22:
                asteroid[i].set_py(594)
            elif asteroid[i].get_py() >= 595:
                asteroid[i].set_py(-21)

            # Asteroids layer (blit)
            blit_asteroid(asteroid[i].get_px(), asteroid[i].get_py(), asteroid[i].get_state())
            # asteroid[1].debug1()
        if asteroid[i].get_state() == 0:
            ct += 1
            if ct == num_of_asteroids:
                game_level += 1
                num_of_asteroids += 1
                next_level()
    ct = 0

    # Bullet bounds check
    for i in range(num_of_bullets):

        # Bullet bounds bullet reset
        if bullet[i].get_py() <= 0 or bullet[i].get_py() >= 600 or bullet[i].get_px() <= 0 or bullet[i].get_px() >= 800:
            bullet[i].set_state(0)
            # break? nope tested once didn't work

        # Bullet trajectory / blit
        if bullet[i].get_state() == 1:
            blit_bullet(bullet[i].get_px(), bullet[i].get_py(), i)
            bullet[i].set_px(bullet[i].get_px() + bullet[i].get_vx())
            bullet[i].set_py(bullet[i].get_py() - bullet[i].get_vy())

        # Bullet collision check
        for i in range(num_of_bullets):  # Added for loop
            for j in range(num_of_asteroids):
                if bullet[i].get_state() == 1 and asteroid[j].get_state() > 0:

                    # collision = isCollision(asteroid[j], bullet[i], 'b')
                    collision = iCollision(asteroid[j].get_px(), asteroid[j].get_py(), bullet[i].get_px(),
                                           bullet[i].get_py(), 'b', j)
                    if collision:
                        explosion_sound = mixer.Sound(os.path.join(resource_path,'boom.wav'))
                        explosion_sound.play()
                        # bullet[i].set_py(480)
                        bullet[i].set_state(0)
                        asteroid[j].set_state(0)
                        score_value += 1
                        if asteroid[j].get_state() > 2:
                            pass
                            # num_of_asteroids = split_asteroid(j, num_of_asteroids) # TODO implement split

    # time.sleep(.5)
    # Update
    pygame.display.update()
