import pygame
from sprites import BackgroundLayer, CustomSpriteGroup, Player, Obstacle, Coin
from random import randint

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 600
FPS = 30
OBSTACLE_VELOCITY = 7
COIN_VELOCITY = 7
SCALE_FACTOR = 0.3
OBSTACLE_SCALE = 0.2
COIN_SCALE = 0.005
BG_MUSIC_VOLUME = 0.7

# Paths
ASSET_PATH = './assets/'
IMAGE_PATH = ASSET_PATH + 'images/'
RUNNER_PATH = ASSET_PATH + 'runner/'
MUSIC_PATH = ASSET_PATH + 'music/'

# Setup display and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

# Utility function to load and scale images
def load_image(path, scale=1):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))

# Background setup
backgrounds = CustomSpriteGroup()
for i in range(1, 6):
    bg_img = load_image(f'{IMAGE_PATH}Hills Layer 0{i}.png')
    backgrounds.add(BackgroundLayer(bg_img, i, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT))

bg_img_6_layer = BackgroundLayer(load_image(f'{IMAGE_PATH}Hills Layer 06.png'), 7, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)

# Background music
pygame.mixer.music.load(f'{MUSIC_PATH}bg_ring.mp3')
pygame.mixer.music.set_volume(BG_MUSIC_VOLUME)
pygame.mixer.music.play(-1)

# Player setup
runner_frames = [load_image(f'{RUNNER_PATH}skeleton-run_{i}.png', SCALE_FACTOR) for i in range(21)]
player = Player(runner_frames, x=100, y=SCREEN_HEIGHT - runner_frames[0].get_height() + 20, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, scale=0.5)

jump_sound = pygame.mixer.Sound(f'{MUSIC_PATH}jump.wav')

# Obstacle setup
cactus = load_image(f'{IMAGE_PATH}cactus.png', OBSTACLE_SCALE)
obstacles = pygame.sprite.Group()

# Coin setup
coin_img = load_image(f'{IMAGE_PATH}coin.jpg', COIN_SCALE)
coin_img.set_colorkey((255, 255, 255))
coins = pygame.sprite.Group()

# coin collect sound
coin_sound = pygame.mixer.Sound(f'{MUSIC_PATH}coin_collect.wav')

# Scoreboard setup
score_box_bg = load_image(f'{IMAGE_PATH}score_box.png', 0.5)
score_rect = score_box_bg.get_rect(topright=(SCREEN_WIDTH - 10, 10))
score_font = pygame.font.SysFont('Arial', 30)
score = 0


# Add obstacles function
def add_obstacles():
    positions = [SCREEN_WIDTH + randint(400, 500), SCREEN_WIDTH * 2, SCREEN_WIDTH * 2 + randint(400, 500)]
    for x in positions:
        obstacles.add(Obstacle(cactus, x=x, y=SCREEN_HEIGHT - cactus.get_height(), velocity=OBSTACLE_VELOCITY))

# Add coins function
def add_coins():
    x, y = SCREEN_WIDTH + randint(100, 200), SCREEN_HEIGHT - cactus.get_height() - coin_img.get_height() - 100
    positions = [x, x + randint(400, 500), x + randint(700, 1000)]
    for x in positions:
        coins.add(Coin(coin_img, x=x, y=y, velocity=COIN_VELOCITY))

# Initial setup
add_obstacles()
add_coins()

# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.jump()
            jump_sound.play()

    # Collision handling
    if any(pygame.sprite.collide_mask(player, obstacle) for obstacle in obstacles):
        running = False
    
    for coin in coins:
        if pygame.sprite.collide_mask(player, coin):
            coin.kill()
            coin_sound.play()
            score += 20
    
    if len(obstacles) < 3:
        add_obstacles()
        score += 10

    if len(coins) < 3:
        add_coins()


    # Update and draw sprites
    backgrounds.update()
    backgrounds.draw(screen)
    coins.update()
    coins.draw(screen)
    player.update()
    player.draw(screen)
    obstacles.update()
    obstacles.draw(screen)
    bg_img_6_layer.update()
    bg_img_6_layer.draw(screen)

    # Draw score
    screen.blit(score_box_bg, score_rect)
    score_text = score_font.render(f'score: {score}', True, (255, 255, 255))
    screen.blit(score_text, score_text.get_rect(center=score_rect.center))

    pygame.display.flip()

# Game Over screen
def show_game_over():
    game_over_bg = pygame.image.load(f'{IMAGE_PATH}trak2_faded1a.tga').convert_alpha()
    game_over_bg = pygame.transform.scale(game_over_bg, (300, 150))
    game_over_font = pygame.font.SysFont('Arial', 50)
    escape_font = pygame.font.SysFont('Arial', 20)
    game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
    escape_text = escape_font.render('Press ESC to exit', True, (0, 255, 0))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

        screen.blit(game_over_bg, game_over_bg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
        screen.blit(escape_text, escape_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))
        pygame.display.flip()

show_game_over()
pygame.quit()
