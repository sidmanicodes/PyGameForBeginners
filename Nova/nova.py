import pygame
import os
pygame.font.init()
pygame.mixer.init()

# Constants

# Basic setup
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SPACE_BG_IMG = pygame.image.load(
    os.path.join("Assets", "space.png"))
SPACE_BG = pygame.transform.scale(SPACE_BG_IMG, (WIDTH, HEIGHT))
pygame.display.set_caption("New Game!")

# Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Middle-of-screen border
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "Grenade+1.mp3")
)
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "Gun+Silencer.mp3")
)
BG_MUSIC = pygame.mixer.Sound(
    os.path.join("Assets", "background_music.mp3")
)

# Fonts
HEALTH_FONT = pygame.font.Font(
    os.path.join("Assets", "mario_font.ttf"), 50
)
WINNER_FONT = pygame.font.Font(
    os.path.join("Assets", "mario_font.ttf"), 130
)

# Rates
VEL = 5
BULLET_VEL = 7
FPS = 60

# Maximum bullet capacity
MAX_BULLETS = 5

# User events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


# Images
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMG = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
    )
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90
    )
RED_SPACESHIP_IMG = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png")
    )
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270
    )

HEART_WIDTH, HEART_HEIGHT = 78, 78

HEART_IMG = pygame.image.load(
    os.path.join("Assets", "heart.png")
)
HEART = pygame.transform.scale(HEART_IMG, (HEART_WIDTH, HEART_HEIGHT))

class GameFunctionality():
    def __init__(self, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
        self.red = red
        self.yellow = yellow
        self.red_bullets = red_bullets
        self.yellow_bullets = yellow_bullets
        self.red_health = red_health
        self.yellow_health = yellow_health
    def draw_intro(self):
        pass
    def draw_game(self):
        WIN.blit(SPACE_BG, (0,0))
        pygame.draw.rect(WIN, BLACK, BORDER)
        
        WIN.blit(YELLOW_SPACESHIP, (self.yellow.x, self.yellow.y))
        WIN.blit(RED_SPACESHIP, (self.red.x, self.red.y))

        self.red_health_text = HEALTH_FONT.render("Health:", 1, WHITE)
        self.yellow_health_text = HEALTH_FONT.render("Health:", 1, WHITE)

        WIN.blit(self.red_health_text, (BORDER.x + BORDER.width + 30, 20))
        WIN.blit(self.yellow_health_text, (30, 20))

        for n in range(self.yellow_health):
            WIN.blit(HEART, ((self.yellow_health_text.get_width() + 22 + (55 * n)), 10))

        for n in range(self.red_health):
            WIN.blit(HEART, ((BORDER.x + BORDER.width + self.red_health_text.get_width() + 23 + (55 * n)), 10))

        for bullet in self.red_bullets:
            pygame.draw.rect(WIN, RED, bullet)

        for bullet in self.yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

        pygame.display.update()
    def yellow_handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and (self.yellow.x - VEL) > 0: # LEFT
            self.yellow.x -= VEL
        if keys_pressed[pygame.K_d] and (self.yellow.x + VEL + self.yellow.height) < BORDER.x: # RIGHT
            self.yellow.x += VEL
        if keys_pressed[pygame.K_w] and (self.yellow.y - VEL) > 0: # UP
            self.yellow.y -= VEL
        if keys_pressed[pygame.K_s] and (self.yellow.y + VEL + self.yellow.width) < HEIGHT: # DOWN
            self.yellow.y += VEL
    def red_handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and (self.red.x - VEL + (BORDER.width/2) - 10) > BORDER.x: # LEFT 
            self.red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and (self.red.x + VEL + (self.red.width - 30)) < WIDTH: # RIGHT
            self.red.x += VEL
        if keys_pressed[pygame.K_UP] and (self.red.y - VEL) > 0: # UP
            self.red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and (self.red.y + VEL + self.red.height + 10) < HEIGHT: # DOWN
            self.red.y += VEL
    def handle_bullets(self):
        for bullet in self.yellow_bullets:
            bullet.x += BULLET_VEL
            if self.red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                self.yellow_bullets.remove(bullet)
            elif bullet.x > WIDTH:
                self.yellow_bullets.remove(bullet)
        for bullet in self.red_bullets:
            bullet.x -= BULLET_VEL
            if self.yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                self.red_bullets.remove(bullet)
            elif bullet.x < 0 - bullet.width:
                self.red_bullets.remove(bullet)


class GameState(GameFunctionality):
    def __init__(self, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
        self.state = "name_scrn"
        self.end_game = False
        self.red = red
        self.yellow = yellow
        self.red_bullets = red_bullets
        self.yellow_bullets = yellow_bullets
        self.red_health = red_health
        self.yellow_health = yellow_health
    def name_scrn(self):
        
    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # Creates bullets for yellow ship and adds to list of yellow bullets
                if event.key == pygame.K_LCTRL and len(self.yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        self.yellow.x + self.yellow.width, self.yellow.y + (self.yellow.height//2 - 2), 10, 5)
                    self.yellow_bullets.append(bullet)
                    pygame.mixer.Sound.set_volume(BULLET_FIRE_SOUND, 0.3)
                    pygame.mixer.Channel(3).play(BULLET_FIRE_SOUND)

                # Creates bullets for red ship and adds to list of red bullets
                if event.key == pygame.K_RCTRL and len(self.red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        self.red.x, self.red.y + (self.red.height//2 - 2), 10, 5)
                    self.red_bullets.append(bullet)
                    pygame.mixer.Sound.set_volume(BULLET_FIRE_SOUND, 0.3)
                    pygame.mixer.Channel(2).play(BULLET_FIRE_SOUND)

            # Defines what should happen in case either ship is hit
            if event.type == RED_HIT:
                self.red_health -= 1
                pygame.mixer.Sound.set_volume(BULLET_HIT_SOUND, 0.3)
                pygame.mixer.Channel(1).play(BULLET_HIT_SOUND)
            
            if event.type == YELLOW_HIT:
                self.yellow_health -= 1
                pygame.mixer.Sound.set_volume(BULLET_HIT_SOUND, 0.3)
                pygame.mixer.Channel(0).play(BULLET_HIT_SOUND)

        # # Creates winning text
        winner_text = ""
        if self.red_health <= 0:
            winner_text = "Yellow wins!"
        
        if self.yellow_health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            self.draw_game()
            self.end_scrn(winner_text)
            self.end_game = True

        # Creates key events for ship movement
        keys_pressed = pygame.key.get_pressed()

        # Calls the ships' movement handlers
        self.yellow_handle_movement(keys_pressed)
        self.red_handle_movement(keys_pressed)

        self.handle_bullets()

        self.draw_game()
    def end_scrn(self, text):
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text, 
            (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(5000)
    def state_manager(self):
        if self.state == "name_scrn":
            self.name_scrn()

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 5
    yellow_health = 5

    clock = pygame.time.Clock()
    run = True

    game_functionality = GameFunctionality(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    game_state = GameState(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    pygame.mixer.Sound.set_volume(BG_MUSIC, 0.1)
    pygame.mixer.Channel(4).play(BG_MUSIC)

    while run:
        clock.tick(FPS)
        game_state.state_manager()

        if game_state.end_game:
            break
    
    main()

if __name__ == '__main__':
    main()