import pygame
from pygame.locals import *
import random


# Initializing pygame
pygame.init()

# Clock/Running Pace
clock = pygame.time.Clock()
fps = 60

# Screen Settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ARC SPACE")

# Define font
font = pygame.font.SysFont('fixedsys', 80)
white = (255,255,255)

# Define game variables
tile_size = 100
ground_scroll = 0 
scroll_speed = 3
flying = False
game_over = False
asteroid_frequency = 1300 # millisecons
last_asteroid = pygame.time.get_ticks()
score = 0
pass_asteroid = False
# Speed increase configuration
speed_increment = 1
max_scroll_speed = 12
next_speed_milestone = 10

# Load Images and Player
bg_img = pygame.image.load('Images/starfield.png')
character = pygame.image.load('Images/tiny_ship.png').convert_alpha()
character2 = pygame.transform.scale_by(character, 2)
rock = pygame.image.load('Images/asteroid.png').convert()
rock.set_colorkey((0,0,0)) # Transparency/convert_alpha as well
rock2 = pygame.transform.scale_by (rock, 0.4)
start_botton = pygame.image.load('Images/restart.png').convert_alpha()
restart_button = pygame.transform.scale_by(start_botton, 0.7)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def reset_game():
    asteroid_group.empty()
    ship.rect.x = 150
    ship.rect.y = HEIGHT/ 2
    # Reset dynamic game values
    global scroll_speed, next_speed_milestone, ground_scroll
    scroll_speed = 3
    next_speed_milestone = 10
    score = 0
    return score  

class Spaceship (pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = character2
        self.image = self.original_image
        self.index = 0
        self.counter = 0
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.clicked = False

    def update(self):
       
        # Gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            self.rect.y += int(self.vel)
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.vel = 0
            if self.rect.top < 0:
                self.rect.top = 0
                self.vel= 0  
                self.clicked = False
                return
                

        if not game_over and flying:
            
            # Jump
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not self.clicked:
                    self.clicked = True
                    self.vel = -10
            if not keys[pygame.K_SPACE]:
                self.clicked = False


            # Ship Rotation
            angle = -self.vel * 1.5
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)
        
        else:

            self.image = self.original_image
            self.rect = self.image.get_rect(center = self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)

class asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock2
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


        # Determinate position of the asteroids
        if position == 1:
            self.image = self.image
            self.rect.bottomleft = [x,y]
        if position == 1:
            self.image = self.image
            self.rect.bottomleft = [x,y]
        if position == -1:    
            self.rect.topleft = [x,y]
        if position == -1:    
            self.rect.topleft = [x,y]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

def mask_collision(s1, s2):
    return pygame.sprite.collide_mask(s1, s2)       

class button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) 

    def draw(self):

        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check if mouse is over the botton
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

Ship_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
ship = Spaceship(150, HEIGHT/2)
Ship_group.add(ship)
      
# Create restart button instance
Button = button( 200, 250 , restart_button)



# Game Loop
run = True
while run: 
        
    clock.tick(fps)

    # Check Score
    if len(asteroid_group) > 0:
        if not pass_asteroid  and asteroid_group.sprites()[0].rect.right < Ship_group.sprites()[0].rect.left:
            score += 1
            pass_asteroid = True

             # Increase screen scroll speed every 10 asteroids passed
            if score >= next_speed_milestone:
                 scroll_speed = min(scroll_speed + speed_increment, max_scroll_speed)
                 next_speed_milestone += 10

        if asteroid_group.sprites()[0].rect.right > Ship_group.sprites()[0].rect.left:
            pass_asteroid = False 

    # look for collision
    if pygame.sprite.groupcollide(Ship_group, asteroid_group, False, False, collided= pygame.sprite.collide_mask):
        game_over = True  
        flying = False

    # check if the ship has hit the ground
    if ship.rect.bottom == HEIGHT:
        game_over = True
        flying = False
    if ship.rect.top == 0:
        game_over = True
        flying = False

    if game_over == False and flying == True:
            
        # Generate new asteroids
        time_now = pygame.time.get_ticks()
        if time_now - last_asteroid > asteroid_frequency:
            asteroid_height = random.randint (100, 500)
            asteroid_options = [
            asteroid(WIDTH, ( asteroid_height), -1),
            asteroid(WIDTH, (asteroid_height), -1),
            asteroid(WIDTH, (asteroid_height), 1),
            asteroid(WIDTH, (asteroid_height), 1),
            asteroid(WIDTH, (asteroid_height), 1),
            asteroid(WIDTH, (asteroid_height), 1),
            asteroid(WIDTH, (asteroid_height), -1),
            asteroid(WIDTH, (asteroid_height), 1),
            ]
            chosen_asteroid = random.choice(asteroid_options)
            asteroid_group.add(chosen_asteroid )
            last_asteroid = time_now

    if not game_over:
        asteroid_group.update()
        

        screen.blit(bg_img, (ground_scroll,0))
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 950:
            ground_scroll = 0
            
    Ship_group.update()
    Ship_group.draw(screen)
    asteroid_group.draw(screen)
        
    draw_text(str(score), font, white, (WIDTH/2), 20)

    # Check for game over and reset
    if game_over == True:
        if Button.draw() == True:
            game_over = False
            score = reset_game()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False      
        if event.type == KEYDOWN and event.key == pygame.K_SPACE and flying == False and game_over == False:
            flying = True


    pygame.display.update()        

pygame.quit()

