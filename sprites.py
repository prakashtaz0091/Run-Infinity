import pygame

GRAVITY = 1


class Coin(pygame.sprite.Sprite):
    def __init__(self, image, x, y, velocity=5):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity
        
    
    def update(self):
        self.rect.x -= self.velocity
        if self.rect.right <= 0:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, velocity=5):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity
        
        
    def update(self):
        self.rect.x -= self.velocity
        if self.rect.right <= 0:
            self.kill()
        
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class CustomSpriteGroup(pygame.sprite.Group):
    def draw(self, surface):
        for sprite in self.sprites():
            sprite.draw(surface)


class BackgroundLayer(pygame.sprite.Sprite):
    def __init__(self, image, speed, y_offset=0, scale=1.0, screen_width=800, screen_height=600):
        super().__init__()
        self.image = pygame.transform.scale(image, (screen_width, screen_height))
        self.rect = self.image.get_rect()
        
        # Initial positions
        self.rect.x = 0
        self.rect.y = y_offset
        self.speed = speed

        # Duplicate second image right after the first
        self.second_rect = self.image.get_rect()
        self.second_rect.x = self.rect.width
        self.second_rect.y = y_offset

    def update(self):
        # Scroll both images to the left
        self.rect.x -= self.speed
        self.second_rect.x -= self.speed

        # When the first image moves completely off-screen, reset its position
        if self.rect.right <= 0:
            self.rect.x = self.second_rect.right

        # When the second image moves completely off-screen, reset it too
        if self.second_rect.right <= 0:
            self.second_rect.x = self.rect.right

    def draw(self, surface):
        # Draw both images side by side for seamless scrolling
        surface.blit(self.image, self.rect)
        surface.blit(self.image, self.second_rect)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)



class Player(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, screen_width=800, screen_height=600, scale=1.0):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 0
        self.on_ground = False
        self.animation_speed = 1  # Lower means faster animation
        self.frame_counter = 0
        self.surface_dim = (screen_width, screen_height)
        
        
    def update(self):
        # Simulate gravity effect
        gravity = 0.8  
        jump_strength = -15

        # Apply gravity if the player isn’t on the ground
        if not self.on_ground:
            self.velocity += gravity
        
        # Apply velocity to the player's position
        self.rect.y += self.velocity

        # Prevent falling through the ground
        if self.rect.bottom >= self.surface_dim[1]:
            self.rect.bottom = self.surface_dim[1]
            self.velocity = 0
            self.on_ground = True

        # Animate the horse
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            

    def jump(self):
        if self.on_ground:
            self.velocity = -15  # Initial upward force
            self.on_ground = False


    def draw(self, surface):
        surface.blit(self.image, self.rect)