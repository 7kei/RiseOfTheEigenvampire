import pygame
import os
from Projectile import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, max_health=100):
        super().__init__()

        # Position and physics properties
        self.x = x
        self.y = y
        self.speed = 5
        self.velocity_y = 0
        self.is_jumping = False
        self.jumpCount = 10
        self.facing_right = True  # Default facing direction

        # Health attributes
        self.max_health = max_health
        self.current_health = max_health

        # Load animations
        self.animations = {
            "idle": self.load_animation('assets/wizard/idle'),
            "run": self.load_animation('assets/wizard/run'),
            "jump": self.load_animation('assets/wizard/jump'),
            "attack2": self.load_animation('assets/wizard/attack2'),
            "death": self.load_animation('assets/wizard/death')
        }

        # Set initial animation
        self.current_animation = "idle"
        self.animation_index = 0
        self.image = self.animations[self.current_animation][self.animation_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Flag to track whether the player is in the attack animation
        self.in_attack_animation = False

    def load_animation(self, path):
        """Load all images in a folder as animation frames."""
        return [pygame.image.load(os.path.join(path, img)) for img in sorted(os.listdir(path))]

    def handle_input(self):
        """Handle player input for movement, jumping, and attacking."""
        keys = pygame.key.get_pressed()

        # Trigger attack animation on mouse click if not already attacking
        if pygame.mouse.get_pressed()[0] and not self.in_attack_animation:
            self.in_attack_animation = True
            self.current_animation = "attack2"  # Set to attack animation
            self.animation_index = 0  # Start from the first frame

        # If the attack animation is not active, handle other movements and animations
        if not self.in_attack_animation:
            # Movement and facing direction
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.x -= self.speed
                self.facing_right = False
                self.current_animation = "run"
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.x += self.speed
                self.facing_right = True
                self.current_animation = "run"
            else:
                self.current_animation = "idle"

            # Jumping
            if not self.is_jumping:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.is_jumping = True

            # Handle jumping mechanics (Gravity and Jumping)
            if self.is_jumping:
                if self.jumpCount >= -10:
                    neg = 1
                    if self.jumpCount < 0:
                        neg = -1
                    self.y -= (self.jumpCount ** 2) * 0.3 * neg  # Applying jump arc
                    self.jumpCount -= 1
                else:
                    self.is_jumping = False
                    self.jumpCount = 10

    def update_animation(self):
        """Update animation frame based on current action and direction."""
        if self.in_attack_animation:
            # Determine the facing direction during attack based on mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < self.x:
                self.facing_right = False  # Face left if mouse is to the left
            else:
                self.facing_right = True  # Face right if mouse is to the right

            # Run through the attack animation frames
            self.animation_index += 0.15
            if self.animation_index >= len(self.animations["attack2"]):
                self.animation_index = 0  # Reset the animation after completing
                self.in_attack_animation = False  # End attack animation
        else:
            self.animation_index += 0.15  # Adjust animation speed to slow down frames

            if self.animation_index >= len(self.animations[self.current_animation]):
                self.animation_index = 0

        # Get the current frame for the selected animation
        frame = self.animations[self.current_animation][int(self.animation_index)]

        # Flip the frame if the player is facing left
        self.image = pygame.transform.flip(frame, True, False) if not self.facing_right else frame
        
        # Update rect to center the player sprite
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        """Update player position and animation."""
        # Update animation (does not depend on input)
        self.update_animation()  # Update the animation frame regardless of input

        # Prevent the player from falling below the ground level (e.g., 500 is the ground level)
        if self.y >= 790:
            self.y = 790  # Reset position to ground level
            self.is_jumping = False
            self.jumpCount = 10  # Reset jump count

    def handle_attack(self, mouse_x, mouse_y):
        """Handle player attack animation and create projectiles."""
        self.current_animation = "attack2"
        self.animation_index = 0  # Reset animation to start from the first frame
        
        # Pass path to the projectile's animation frames
        projectile_path = 'assets/projectile'  # Example path for your projectile animation frames
        return Projectile(self.x, self.y, mouse_x, mouse_y, projectile_path)
    
    def draw(self, window):
        """Draw the player on the game window and show the rectangle."""
        # Draw the player sprite using rect to ensure it's centered
        window.blit(self.image, self.rect.topleft)  # Draw the image at the top-left of the rect

        # Optional: Draw the rectangle around the player for visualization
        # Reduce the size of the rectangle by half (you can change the factor as needed)
        reduced_width = self.rect.width // 3.5
        reduced_height = self.rect.height // 2
        reduced_rect = pygame.Rect(self.rect.centerx - reduced_width // 2, self.rect.centery - reduced_height // 2, reduced_width, reduced_height)

        pygame.draw.rect(window, (255, 0, 0), reduced_rect, 2)  # Red rectangle with a 2-pixel border

