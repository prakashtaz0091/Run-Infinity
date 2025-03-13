import pygame
from sprites import BackgroundLayer, CustomSpriteGroup, Player, Obstacle
from random import randint

pygame.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Runner")
running = True



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
bg_img_6_layer = BackgroundLayer(bg_img_6, 6, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)


backgrounds = CustomSpriteGroup()
backgrounds.add(bg_img_1_layer, bg_img_2_layer, bg_img_3_layer, bg_img_4_layer, bg_img_5_layer)




# runner_1 = pygame.image.load('./assets/runner/skeleton-run_0.png').convert_alpha()
# runner_2 = pygame.image.load('./assets/runner/skeleton-run_1.png').convert_alpha()

runner_frames = [ pygame.image.load(f'./assets/runner/skeleton-run_{i}.png').convert_alpha()  for i in range(21)]
scale_factor = 0.3
runner_frames_scaled_down = [ pygame.transform.scale(frame, (frame.get_width() * scale_factor, frame.get_height() * scale_factor)) for frame in runner_frames]

player = Player(runner_frames_scaled_down, x=100, y=SCREEN_HEIGHT - runner_frames_scaled_down[0].get_height()+20, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, scale=0.5)


# obstacle
cactus = pygame.image.load('./assets/images/cactus.png').convert_alpha()
obstacle_sf = 0.2
cactus = pygame.transform.scale(cactus, (cactus.get_width() * obstacle_sf, cactus.get_height() * obstacle_sf))
obs1 = Obstacle(cactus, x=SCREEN_WIDTH, y=SCREEN_HEIGHT - cactus.get_height(), velocity=6)
obs2 = Obstacle(cactus, x=SCREEN_WIDTH+randint(300, 500), y=SCREEN_HEIGHT - cactus.get_height(), velocity=6)

obstacles = pygame.sprite.Group()
obstacles.add(obs1, obs2)



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
            
    
    
    
    
    backgrounds.update()
    backgrounds.draw(screen)
    # bg_img_1_layer.draw(screen)
    
    player.update()
    player.draw(screen)
    
    
    if len(obstacles) < 2:
        new_obstacle = Obstacle(cactus, x=SCREEN_WIDTH+randint(300, 500), y=SCREEN_HEIGHT - cactus.get_height(), velocity=6)
        obstacles.add(new_obstacle)
        
    obstacles.update()    
    obstacles.draw(screen)
    
    bg_img_6_layer.update()
    bg_img_6_layer.draw(screen)
    
    
    
    # display update
    pygame.display.flip()
            
    
pygame.quit()