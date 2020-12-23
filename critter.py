import pygame
from pygame.sprite import Sprite
import random
import math


class Critter(Sprite):
    """A class to manage the creatures that will be generated"""

    def __init__(self, ss_game):
        """Initialize each critter and set start position"""

        super(Critter, self).__init__()
        self.screen = ss_game.screen
        self.screen_rect = ss_game.screen.get_rect()
        self.settings = ss_game.settings

        # Create a critter at (0,0) and then set the correct position.
        self.strength = 1.0   # This will be modified for next generation
        self.width, self.height = self.strength * 2, self.strength * 2
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midleft = self.screen_rect.midleft
        self.color = self.settings.critter_color
        self.health = self.settings.critter_health
        self.critter_attack = self.settings.critter_attack
        self.no_attack_time = self.settings.no_attack_time
        self.speed = self.settings.critter_speed
        self.expend = self.settings.critter_expend * (self.speed**2) * (self.strength ** 3)
        self.sensor_timer = 0
        self.type = 1  # random.randint(1, 2)
        self.list = [0, 1]
        choice = random.choice(self.list)
        if choice == 0:
            self.sensor = True
        else:
            self.sensor = False
        self.angle = random.randint(1, 179)
        self.count = self.settings.critter_count
        self.graze_period = random.randint(100, 500)  # Used to see what periods give best survival after a few rounds

        # Store the critter's position as a decimal value.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        # Movement flags initially set False
        self.moving_straight = False
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the critter's position based on the movement flags"""
        # Update the critter's x value, not the rect and limit to the screen width.
        # First cater for type 1 straight line critters
        if self.moving_straight and self.rect.right <= self.screen_rect.right and \
                self.rect.left >= 0 and self.rect.top >= 0 and \
                self.rect.bottom <= self.screen_rect.bottom:
            self.straight_move()
        elif self.moving_straight and self.rect.right > self.screen_rect.right:
            self.angle = random.randint(185, 355)
            self.straight_move()
        elif self.moving_straight and self.rect.left < 0:
            self.angle = random.randint(5, 175)
            self.straight_move()
        elif self.moving_straight and self.rect.top < 0:
            options = [random.randint(275, 360), random.randint(1, 85)]
            self.angle = random.choice(options)
            self.straight_move()
        elif self.moving_straight and self.rect.bottom > self.screen_rect.bottom:
            self.angle = random.randint(95, 265)
            self.straight_move()
        # Now cater for random critters
        if self.moving_right and self.rect.right <= self.screen_rect.right:
            self.x += self.speed * random.randint(1, 10)
            self.health -= self.expend
        if self.moving_left and self.rect.left >= 0:
            self.x -= self.speed * random.randint(1, 10)
            self.health -= self.expend
        if self.moving_up and self.rect.top >= 0:
            self.y -= self.speed * random.randint(1, 10)
            self.health -= self.expend
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.y += self.speed * random.randint(1, 10)
            self.health -= self.expend
        # Set terms for reproduction
        if self.health < self.settings.critter_reproduce * self.settings.critter_health * self.strength * 0.1:
            self.color = (255, 10, 10)
        elif self.health > self.settings.critter_reproduce * self.settings.critter_health * (self.strength**3) * 0.9:
            self.color = (255, 255, 10)
        else:
            self.color = self.settings.critter_color
        # Update rect object from self.x and self.y
        self.rect.x = self.x
        self.rect.y = self.y

    def straight_move(self):
        # Straight move
        self.x += self.speed * math.sin(self.angle * math.pi / 180)
        self.y += self.speed * math.cos(self.angle * math.pi / 180)
        self.health -= self.expend

    def draw_critter(self):
        """Draw the critter to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
