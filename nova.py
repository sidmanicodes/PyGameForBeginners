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

blank_var = None

class GameFunctionality():
    def __init__(self):
        pass
    def draw_window(self, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
        WIN.blit(SPACE_BG, (0,0))
        pygame.draw.rect(WIN, BLACK, BORDER)
        
        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
        WIN.blit(RED_SPACESHIP, (red.x, red.y))

        red_health_text = HEALTH_FONT.render("Health:", 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health:", 1, WHITE)

        WIN.blit(red_health_text, (BORDER.x + BORDER.width + 30, 20))
        WIN.blit(yellow_health_text, (30, 20))

        for n in range(yellow_health):
            WIN.blit(HEART, ((yellow_health_text.get_width() + 22 + (55 * n)), 10))

        for n in range(red_health):
            WIN.blit(HEART, ((BORDER.x + BORDER.width + red_health_text.get_width() + 23 + (55 * n)), 10))

        for bullet in red_bullets:
            pygame.draw.rect(WIN, RED, bullet)

        for bullet in yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

        pygame.display.update()
    def yellow_handle_movement(self, keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and (yellow.x - VEL) > 0: # LEFT
            yellow.x -= VEL
        if keys_pressed[pygame.K_d] and (yellow.x + VEL + yellow.height) < BORDER.x: # RIGHT
            yellow.x += VEL
        if keys_pressed[pygame.K_w] and (yellow.y - VEL) > 0: # UP
            yellow.y -= VEL
        if keys_pressed[pygame.K_s] and (yellow.y + VEL + yellow.width) < HEIGHT: # DOWN
            yellow.y += VEL
    def red_handle_movement(self, keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and (red.x - VEL + (BORDER.width/2) - 10) > BORDER.x: # LEFT 
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and (red.x + VEL + (red.width - 30)) < WIDTH: # RIGHT
            red.x += VEL
        if keys_pressed[pygame.K_UP] and (red.y - VEL) > 0: # UP
            red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and (red.y + VEL + red.height + 10) < HEIGHT: # DOWN
            red.y += VEL
    def handle_bullets(self, yellow_bullets, red_bullets, yellow, red):
        for bullet in yellow_bullets:
            bullet.x += BULLET_VEL
            if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                yellow_bullets.remove(bullet)
            elif bullet.x > WIDTH:
                yellow_bullets.remove(bullet)
        for bullet in red_bullets:
            bullet.x -= BULLET_VEL
            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                red_bullets.remove(bullet)
            elif bullet.x < 0 - bullet.width:
                red_bullets.remove(bullet)


class GameState(GameFunctionality):
    def __init__(self, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
        self.state = "main_game"
        self.end_game = False
        self.red = red
        self.yellow = yellow
        self.red_bullets = red_bullets
        self.yellow_bullets = yellow_bullets
        self.red_health = red_health
        self.yellow_health = yellow_health
    def name_scrn(self):
        pass
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
            self.draw_window(self.red, self.yellow, self.red_bullets, self.yellow_bullets, self.red_health, self.yellow_health)
            self.end_scrn(winner_text)
            self.end_game = True

        # Creates key events for ship movement
        keys_pressed = pygame.key.get_pressed()

        # Calls the ships' movement handlers
        self.yellow_handle_movement(keys_pressed, self.yellow)
        self.red_handle_movement(keys_pressed, self.red)

        self.handle_bullets(self.yellow_bullets, self.red_bullets, self.yellow, self.red)

        self.draw_window(self.red, self.yellow, self.red_bullets, self.yellow_bullets, self.red_health, self.yellow_health)
    def end_scrn(self, text):
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text, 
            (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(5000)
    def state_manager(self):
        if self.state == "main_game":
            self.main_game()


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 5
    yellow_health = 5

    clock = pygame.time.Clock()
    run = True

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