"""
Goals
Clean up code, fix no stop movement, limit star and player speed, add star spawner,
set player back at border if they move to far

Strech Goals
Add dynamic player stats, add star difficulty increase, player xp and pick 3 system, add health, homescreen

"""
import pygame as py
import random
import time

py.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("Star Fall")

game_speed = .05
game_clock = time.time()

game_time = time.time()

BLK = (0, 0, 0)
RED = (255, 0, 0)

background_color = (47, 15, 140)

class Mouse():

    def __init__(self):
        self.hitbox = py.rect.Rect(0, 0, 80, 4)
        self.hitbox.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 96)
        self.color = RED
        self.speed = 0
        self.speed_multiplier = 5
        self.score = 0
        self.lives = 3

    def draw(self):
        screen.blit(mouse_sprite, (self.hitbox.x - 24, self.hitbox.y - 32))

    def direction(self):

        if event.key == py.K_a:
            self.speed = -1
        if event.key == py.K_d:
            self.speed = 1
    
    def move(self):
        if self.hitbox.left < SCREEN_WIDTH - self.hitbox.width and self.speed == abs(self.speed):
            self.hitbox.centerx += self.speed * self.speed_multiplier
        elif self.hitbox.left > 0 and self.speed != abs(self.speed):
            self.hitbox.centerx += self.speed * self.speed_multiplier
            
class Star():

    def __init__(self, y):
        self.hitbox = py.rect.Rect(SCREEN_WIDTH // 2, y, 32, 32)
        self.hitbox.x = random.randint(self.hitbox.width, SCREEN_WIDTH - self.hitbox.width)
        self.caught = False
        self.fallen = False
        self.speed = 10

    def draw(self):
        screen.blit(star_sprite, self.hitbox)

    def move(self):
        self.hitbox.y += self.speed
        if self.hitbox.colliderect(player.hitbox):
            self.caught = True
        if self.hitbox.bottom > SCREEN_HEIGHT:
            self.fallen = True

def draw_screen():
    screen.blit(background, (0, 0))

def make_img(link):
    img = py.image.load(link).convert()
    img.set_colorkey((0,0,0))
    return img

def make_text(text, font_size, x, y, color = BLK, font = "./slkscr.ttf"):
    text_info = []

    text_font = py.font.Font(font, font_size)
    text_rend = text_font.render(text, True, color)
    text_rect = text_rend.get_rect(center = (x, y))
    text_info = [text_rend, text_rect]

    return text_info


player = Mouse()
stars = [Star(-32), Star(-128), Star(-198)]

background = py.transform.scale(make_img("./background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
mouse_sprite = py.transform.scale(make_img("./moose.png"), (128, 128))
star_sprite = py.transform.scale(make_img("./straw.png"), (32, 32))

py.key.set_repeat()

game_active = True
running = True

while running:

    while game_active:
        if time.time() - game_clock > game_speed:
            game_clock = time.time()

            draw_screen()
            score = make_text(f"Score: {player.score}", 30, 80, 20)
            screen.blit(score[0], score[1])

            for star in stars:
                star.draw()
                star.speed = 10 + int((time.time() - game_time) // 7)
                if star.caught:
                    star.caught = False
                    star.hitbox.y = -100
                    star.hitbox.x = random.randint(star.hitbox.width, SCREEN_WIDTH - star.hitbox.width)
                    player.score += 1
                if star.fallen:
                    star.fallen = False
                    star.hitbox.y = -100
                    star.hitbox.x = random.randint(star.hitbox.width, SCREEN_WIDTH - star.hitbox.width)
                    player.lives -= 1
            player.draw()


            for event in py.event.get():
                if event.type == py.QUIT:
                    game_active = False
                    running = False

                if event.type == py.KEYDOWN:
                    player.direction()
            
            player.move()
            player.speed_multiplier = 5 + player.score / 3
            
            for star in stars:
                star.move()

            py.display.update()




py.quit()
