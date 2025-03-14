import pygame
from sprites import BackgroundLayer, CustomSpriteGroup, Player, Obstacle
from random import randint


pygame.init()
pygame.mixer.init()
pygame.font.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Runner")
running = True


# Backgrounds
bg_img_1 = pygame.image.load('./assets/images/Hills Layer 01.png').convert_alpha()
bg_img_1_layer = BackgroundLayer(bg_img_1, 1, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)

bg_img_2 = pygame.image.load('./assets/images/Hills Layer 02.png').convert_alpha()
bg_img_2_layer = BackgroundLayer(bg_img_2, 2, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)

bg_img_3 = pygame.image.load('./assets/images/Hills Layer 03.png').convert_alpha()
bg_img_3_layer = BackgroundLayer(bg_img_3, 3, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)

bg_img_4 = pygame.image.load('./assets/images/Hills Layer 04.png').convert_alpha()
bg_img_4_layer = BackgroundLayer(bg_img_4, 4, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)

bg_img_5 = pygame.image.load('./assets/images/Hills Layer 05.png').convert_alpha()
bg_img_5_layer = BackgroundLayer(bg_img_5, 5, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)

bg_img_6 = pygame.image.load('./assets/images/Hills Layer 06.png').convert_alpha()
bg_img_6_layer = BackgroundLayer(bg_img_6, 7, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)


backgrounds = CustomSpriteGroup()
backgrounds.add(bg_img_1_layer, bg_img_2_layer, bg_img_3_layer, bg_img_4_layer, bg_img_5_layer)


# background music
pygame.mixer.music.load('./assets/music/bg_ring.mp3')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)


# runner or Player
runner_frames = [ pygame.image.load(f'./assets/runner/skeleton-run_{i}.png').convert_alpha()  for i in range(21)]
scale_factor = 0.3
runner_frames_scaled_down = [ pygame.transform.scale(frame, (frame.get_width() * scale_factor, frame.get_height() * scale_factor)) for frame in runner_frames]
player = Player(runner_frames_scaled_down, x=100, y=SCREEN_HEIGHT - runner_frames_scaled_down[0].get_height()+20, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, scale=0.5)


# player jump sound
jump_sound = pygame.mixer.Sound('./assets/music/jump.wav')
# jump_sound.set_volume(0.5)



# obstacle
cactus = pygame.image.load('./assets/images/cactus.png').convert_alpha()
obstacle_sf = 0.2
cactus = pygame.transform.scale(cactus, (cactus.get_width() * obstacle_sf, cactus.get_height() * obstacle_sf))
obstacles = pygame.sprite.Group()
def add_obstacles():
    obs1 = Obstacle(cactus, x=SCREEN_WIDTH, y=SCREEN_HEIGHT - cactus.get_height(), velocity=7)
    obs2 = Obstacle(cactus, x=obs1.rect.x+randint(400, 500), y=SCREEN_HEIGHT - cactus.get_height(), velocity=7)
    obs3 = Obstacle(cactus, x=obs2.rect.x+randint(400, 500), y=SCREEN_HEIGHT - cactus.get_height(), velocity=7)
    obs4 = Obstacle(cactus, x=SCREEN_WIDTH*2, y=SCREEN_HEIGHT - cactus.get_height(), velocity=7)
    obstacles.add(obs1, obs2, obs3, obs4)



# Score Board
score_box_bg = pygame.image.load('./assets/images/score_box.png').convert_alpha()
score_box_bg_sf = 0.5
score_box_bg = pygame.transform.scale(score_box_bg, (score_box_bg.get_width()*score_box_bg_sf, score_box_bg.get_height()*score_box_bg_sf))
score_rect = score_box_bg.get_rect()
score_rect.x = SCREEN_WIDTH-score_rect.width-10
score_rect.y = 10
score_rect_shadow = pygame.rect.Rect(score_rect.x+4, score_rect.y, score_rect.width-8, score_rect.height+4)
score_font = pygame.font.SysFont('Arial', 30)
score = 0
score_text = score_font.render(f'score: {score}', True, (255, 255, 255))
score_text_rect = score_text.get_rect()
score_text_rect.center = (score_rect.x + score_rect.width // 2, score_rect.y + score_rect.height // 2)


# Game Loop
while running:
    clock.tick(30)
    # handle_quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
            elif event.key == pygame.K_SPACE:
                player.jump() 
                jump_sound.play()       
            
    
    
    # player collide with obstacle using mask
    for obstacle in obstacles:
        if pygame.sprite.collide_mask(player, obstacle):
            running = False
            break
    

    backgrounds.update()
    backgrounds.draw(screen)


    pygame.draw.rect(screen, (100, 100, 100), score_rect_shadow)
    screen.blit(score_box_bg, score_rect)
    screen.blit(score_text, score_text_rect)

    
    player.update()
    player.draw(screen)
    
    
    if len(obstacles) < 2:
        add_obstacles()
        score += 10
        score_text = score_font.render(f'score: {score}', True, (255, 255, 255))
        
    obstacles.update()    
    obstacles.draw(screen)
    
    bg_img_6_layer.update()
    bg_img_6_layer.draw(screen)
    
    
    
    # display update
    pygame.display.flip()
            




# Game Over Screen
game_over_view = True

game_over_bg = pygame.image.load('./assets/images/trak2_faded1a.tga').convert_alpha()
game_over_bg = pygame.transform.scale(game_over_bg, (300, 150))
game_over_bg_rect = game_over_bg.get_rect()
game_over_bg_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
game_over_bg_shadow = pygame.rect.Rect(game_over_bg_rect.x+4, game_over_bg_rect.y, game_over_bg_rect.width-8, game_over_bg_rect.height+4)


game_over_font = pygame.font.SysFont('Arial', 50)
game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)


escape_font = pygame.font.SysFont('Arial', 20)
escape_text = escape_font.render('Press ESC to exit', True, (0, 255, 0))
escape_surface = escape_text.get_rect()
escape_surface.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)

# Game Over Loop
while game_over_view:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over_view = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over_view = False
    
    pygame.draw.rect(screen, (100, 100, 100), game_over_bg_shadow)
    screen.blit(game_over_bg, game_over_bg_rect)
    screen.blit(game_over_text,game_over_text_rect)
    screen.blit(escape_text, escape_surface)
            
    pygame.display.flip()    


# Clean up and quit
pygame.quit()