import sys
import pygame
import random
import matplotlib.pyplot as plt
import math
from time import sleep

from critter import Critter
from food import Food
from settings import Settings
from display import Display


def _straight_move(critter):
    critter.moving_straight = True


class SurvivalSim:
    """Overall class to manage the simulation assets and behaviours"""

    def __init__(self):
        """Initialse the simulation and create resources"""
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Survival Simulation")
        self.days = 0

        # Create an instance of critters.
        self._create_critters()
        self._create_feed()
        self.stats = {}
        self.days_list = []
        self.critter_totals = []
        self.food_total = []
        self.max_strength_list = []
        self.min_strength_list = []
        self.max_speed_list = []
        self.min_speed_list = []
        self.max_strength = 0
        self.min_strength = 1000
        self.max_speed = 0
        self.min_speed = 1000
        self.run_time = self.settings.run_time
        # Create and instance of the text display
        self.display = Display(self)
    def run_game(self):
        self.settings.initialize_dynamic_settings()

        while self.days < self.run_time:
            self.days += 1
            for i in range(10000):   # Range is what is setting the day intervals for the moment
                self._check_events()
                self._check_food_growth()
                self._critters_moving()
                self._critters_sensing()
                self._check_critters_food()
                self._critter_reproduce_check()
                self.max_strength = 0
                self.min_strength = 1000
                self.max_speed = 0
                self.min_speed = 1000
                self.max_min()

                # Prep the display info.
                self.display.prep_images(self.days, len(self.feed), len(self.critters), self.max_strength,
                                         self.min_strength, self.max_speed, self.min_speed)

                # Countdown to enable attacks NB: no attacks immediately after reset or reproduction
                for critter in self.critters.sprites():
                    if critter.critter_attack is False:
                        critter.no_attack_time += 1
                    if critter.no_attack_time > 2000:
                        critter.critter_attack = True
                # Having enabled attacks, check for attacks
                self._check_critter_critters()
                self.critters.update()
                self.food.update()

                self._update_screen()

            sleep(2)    # sleep to see what is happening
            # Need to pause the sim here and look at stats for how many remaining .
            self._reset()
            # Check to see if the critters group is empty.
            if not self.critters.sprites():
                print(f"The number of days until death was {self.days}")

        # Plot graph after number of days has passed
        for key, value in self.stats.items():
            self.days_list.append(key)
            self.critter_totals.append(value[0])
            self.food_total.append(value[1])
            self.max_strength_list.append(value[2])
            self.min_strength_list.append(value[3])
            self.max_speed_list.append(value[4])
            self.min_speed_list.append(value[5])
        print(self.days_list)
        print(self.critter_totals)
        print(self.max_strength_list)
        print(self.min_strength_list)
        print(self.max_speed_list)
        print(self.min_speed_list)
        # Plot the critters and food supply against days.
        plt.style.use('seaborn')
        fig, ax = plt.subplots()
        ax.plot(self.days_list, self.critter_totals, c='blue', label="Critter Totals")
        ax.plot(self.days_list, self.food_total, c='green', label="Food Supply")
        plt.legend(loc="upper left")
        # Set chart title and label axes.
        ax.set_title("Critter and Food Supply after Each Day", fontsize=20)
        ax.set_xlabel("Days", fontsize=14)
        ax.set_ylabel("Critter Numbers / Food Supply", fontsize=14)

        plt.show()
        plt.savefig('Sim_Food_Critters_per_day.png', bbox_inches='tight')

        # Plot max strength against days.
        plt.style.use('seaborn')
        fig, ax = plt.subplots()
        ax.plot(self.days_list, self.max_strength_list, c='red', label="Max Strength")
        ax.plot(self.days_list, self.min_strength_list, c='blue', label="Min Strength")
        ax.plot(self.days_list, self.max_speed_list, c='green', label="Max Speed")
        ax.plot(self.days_list, self.min_speed_list, c='magenta', label="Min Speed")
        plt.legend(loc="upper left")
        # Set chart title and label axes.
        ax.set_title("Max / Min Strength / Speed for Each Day", fontsize=20)
        ax.set_xlabel("Days", fontsize=14)
        ax.set_ylabel("Max / Min Strength / Speed", fontsize=14)

        plt.show()
        plt.savefig('Sim_MaxMin_Strength_per_day.png', bbox_inches='tight')
        self._check_events()

    def _reset(self):

        # Summarize the days gone and critters present.
        self._stats()

        # Repopulate empty food state:
        if len(self.feed) == 0:
            for i in range(5):
                self.food = Food(self)
                self.feed.add(self.food)

        self._update_screen()
        sleep(5)

    def _create_critters(self):
        self.critters = pygame.sprite.Group()
        for i in range(self.settings.critter_limit):
            self.critter = Critter(self)
            self.critters.add(self.critter)

    def _create_feed(self):
        # Create group of food called feed
        self.feed = pygame.sprite.Group()

        for i in range(self.settings.food_max):
            self.food = Food(self)
            self.feed.add(self.food)

    def _check_food_growth(self):
        for food in self.feed.sprites():
            food.grow_time += 1
            if food.grow_time > food.food_reproduce_time:
                self.food = Food(self)
                self.feed.add(self.food)
                food.grow_time = 0

    def _critters_moving(self):
        for critter in self.critters.sprites():
            if critter.type == 1:       # Allows the straightline part of critter.update to run
                _straight_move(critter)

            if critter.type == 2:       # Set the critters moving on random paths.
                self._random_move(critter)

    def _random_move(self, critter):
        rand_horiz = random.randint(1, 3)
        rand_vert = random.randint(1, 3)

        if rand_horiz == 1:
            critter.moving_right = True
        elif rand_horiz == 2:
            critter.moving_right = False
            critter.moving_left = False
        elif rand_horiz == 3:
            critter.moving_left = True

        if rand_vert == 1:
            critter.moving_up = True
        elif rand_vert == 2:
            critter.moving_up = False
            critter.moving_down = False
        elif rand_vert == 3:
            critter.moving_down = True

    def _critters_sensing(self):
        # For any sensor enabled critters are they near a threat?

        for critter in self.critters.sprites():
            if critter.sensor and critter.sensor_timer >100:
                for other_critter in self.critters.sprites():
                    dist_x = critter.x - other_critter.x
                    dist_y = critter.y - other_critter.y
                    dist = math.sqrt(dist_x**2 + dist_y**2)

                    if dist <= 20 and critter.strength < other_critter.strength and\
                            other_critter.strength > (critter.strength * 1.2):
                        critter.angle += random.randint(45, 315)
                        critter.sensor_timer = 0
            critter.sensor_timer += 1

    def _check_critter_critters(self):
        # See if any critters collide and decide what to do.

        for critter in self.critters.sprites():
            hit_list = pygame.sprite.spritecollide(critter, self.critters, False)

            for hit in hit_list:
                if critter.strength > (hit.strength * 1.3) and critter.critter_attack:
                    critter.health += hit.health
                    critter.strength += (0.15 * hit.strength)  # Eat another and gain strength but
                    critter.width, critter.height = int(critter.strength * 2), int(critter.strength * 2)
                    x = int(critter.x)
                    y = int(critter.y)
                    critter.rect = pygame.Rect(x, y, critter.width, critter.height)
                    critter.expend = self.settings.critter_expend * (critter.speed ** 2) * (critter.strength ** 3)
                    self.critters.remove(hit)

    def _check_critters_food(self):
        # See if any critters have bumped into food

        for critter in self.critters.sprites():
            critter.count += 1    # Increment count since last ate.

            if pygame.sprite.spritecollide(critter, self.feed, True):
                critter.health += self.settings.food_value
                critter.moving_straight = False
                critter.type = 2  # Change to random mode after eating
                critter.count = 0  # Zero count since last ate.

            # If in random mode and not eaten for graze period go straight line.
            if critter.type == 2 and critter.count > critter.graze_period:
                # Turn off the random flags
                critter.moving_right = False
                critter.moving_left = False
                critter.moving_down = False
                critter.moving_up = False
                # Reset to type 1 straight line mode
                critter.type = 1

            # Remove dead critters
            if critter.health <= 0:
                self.critters.remove(critter)

    def _critter_reproduce_check(self):
        for critter in self.critters.sprites():
            if critter.health >= self.settings.critter_reproduce * self.settings.critter_health * (critter.strength **3):
                self._reproduce(critter)

    def _reproduce(self, critter):
        critter.health = critter.health/2
        self.critter = Critter(self)
        self.critter.health = critter.health
        # Add reproductive variation in strength between 0.8 and 1.2 times the original
        self.critter.strength = critter.strength * (1.2 - (random.randint(0, 4) / 10))
        # Add reproductive variation in speed between 0.8 and 1.2 times the original
        self.critter.speed = critter.speed * (1.2 - (random.randint(0, 4) / 10))
        # Redefine the expenditure to ensure up to date values are used.
        self.critter.expend = self.settings.critter_expend * (self.critter.speed ** 2) * (self.critter.strength ** 3)
        # print(self.critter.strength)
        self.critter.width, self.critter.height = int(self.critter.strength * 2), int(self.critter.strength * 2)
        self.critter.x = int(critter.x)
        self.critter.y = int(critter.y)
        self.critter.rect = pygame.Rect(self.critter.x, self.critter.y, self.critter.width, self.critter.height)
        # Set the attack flags to false to prevent reproduced critters attacking each other immediately
        self.critter.critter_attack = False  # Set to True again in the run routine
        critter.critter_attack = False  # Set to True again in the run routine
        if self.critter.strength < 0.5:
            self.critter.kill()
        else:
            self.critters.add(self.critter)

    def _stats(self):
        # Work out the state after each day.
        days = str(self.days)
        critter_no = len(self.critters)
        food_supply = len(self.feed)

        self.max_min()
        # Add the day as a key and the value to the stats dictionary
        self.stats[days] = critter_no, food_supply, self.max_strength, self.min_strength, self.max_speed, self.min_speed


    def max_min(self):

        count = 0
        for critter in self.critters.sprites():
            # Increment the count
            count += 1
            # Check to see which is the max strength and then populate max_strength (and speeds).
            if critter.strength > self.max_strength:
                self.max_strength = critter.strength
            # Same for min_strength
            if critter.strength <= self.min_strength:
                self.min_strength =  critter.strength
            if critter.speed > self.max_speed:
                self.max_speed = critter.speed
            # Same for min_strength
            if critter.speed <= self.min_speed:
                self.min_speed =  critter.speed

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        for critter in self.critters.sprites():
            critter.draw_critter()
        for food in self.feed.sprites():
            food.draw_food()

        # Draw the text image.
        self.display.show_text()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_events(self):
        """ Watch for keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # This is the top right x quit
                sys.exit()


if __name__ == '__main__':
    # Make a game instance and run game.
    ss = SurvivalSim()
    ss.run_game()