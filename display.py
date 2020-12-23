import pygame.font


class Display:
    """A class to report staus information"""

    def __init__(self, ss_game):
        """Initalize the display attributes"""
        self.ss_game = ss_game
        self.screen =  ss_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ss_game.settings
        self.days = ss_game.days
        self.food_supply = len(ss_game.feed)
        self.critter_no = len(ss_game.critters)
        self.max_strength = ss_game.max_strength
        self.min_strength = ss_game.min_strength
        self.max_speed = ss_game.max_speed
        self.min_speed = ss_game.min_speed
        # Font settings
        self.text_color = (230, 230, 230)
        self.font =  pygame.font.SysFont(None, 25)

        # Prep the images.
        self.prep_images(self.days, self.food_supply, self.critter_no, self.max_strength, self.min_strength,
                         self.max_speed, self.min_speed)

    def prep_images(self,days,  food, critter_no, max_sgth, min_sgth, max_spd, min_spd):
        """Turn the data into a rendered image"""
        self.days = days
        self.food_supply = food
        self.critter_no = critter_no
        self.max_strength = max_sgth
        self.min_strength = min_sgth
        self.max_speed = max_spd
        self.min_speed = min_spd
        top_line_str1 = f"Day: {self.days}      Food: {self.food_supply}        Critters: {self.critter_no}"
        top_line_str2 = f"        Max Strength: {self.max_strength:10.2f}    Min Strength: {self.min_strength:10.2f}   "
        top_line_str3 = f"        Max Speed: {self.max_speed:10.2f}    Min Speed: {self.min_speed:10.2f}   "
        top_line_str = top_line_str1 + top_line_str2 + top_line_str3
        self.top_line_image = self.font.render(top_line_str, True, self.text_color, self.settings.bg_color)

        # Display the image at the top of the screen.
        self.top_line_rect =  self.top_line_image.get_rect()
        self.top_line_rect.top = self.screen_rect.top

    def show_text(self):
        """Draw the text"""
        self.screen.blit(self.top_line_image, self.top_line_rect)
