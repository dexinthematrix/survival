import pygame
from pygame.sprite import Sprite
import random


class Food(Sprite):
    """A class to manage the food that will be generated"""
    # Each food item generated at a random position on screen.
    # Each food item will be added the feed group.

    def __init__(self, ss_game):
        """Initialize each food item and set start position"""

        super(Food, self).__init__()
        self.screen = ss_game.screen
        self.screen_rect = ss_game.screen.get_rect()
        self.settings = ss_game.settings
        # Create a food at (0,0) and then set the correct position.
        self.rect = pygame.Rect(0, 0, self.settings.food_width, self.settings.food_height)
        self.rect.midleft = self.screen_rect.midleft
        self.color = self.settings.food_color

        # Randomize the position of this item of food
        self.y = random.randint(1, self.settings.screen_height)
        self.x = random.randint(1, self.settings.screen_width)
        # Set the food rectangle to the randomised x and y
        self.rect.x = self.x
        self.rect.y = self.y
        # Set the reproduction time for the individual food element.
        self.food_reproduce_time = random.randint(self.settings.food_reproduce_min,self.settings.food_reproduce_max)
        # Set a time of growth for the individual food element - this is the clock to run for reproduction.
        self.grow_time = 0

    def draw_food(self):
        """Draw the food to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
