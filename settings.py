
class Settings:
    """A class to store all settings for Survival Simulation"""

    def __init__(self):
        """Initialise the game's static settings"""
        # Screen settingsd
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10, 10, 10)

        self.critter_limit = 1
        # initial speed available - will be modified during the game
        # May alter color as health improves
        self.critter_color = (100, 100, 200)
        # Cycles since  critter last ate.
        self.critter_count = 0
        # food settings
        self.food_width = 5
        self.food_height = 5
        self.food_color = (10, 210, 10)
        food_value = int(input("Please input a food value between 1 and 20"))
        self.food_value = food_value
        self.run_time = int(input("Please in put the number of days in whole (suggest 20 to 100)"))

        self.food_max = 20
        self.food_reproduce_max = 10000
        self.food_reproduce_min = 5000

    def initialize_dynamic_settings(self):

        # Health status will vary with movement and food eaten
        self.critter_health = 100
        # Speed may vary
        self.critter_speed = 0.5
        # health expended basic factor used with speed and strength for final values
        self.critter_expend = 0.001
        # reproduction factor
        self.critter_reproduce = 1.1
        self.critter_attack = False
        self.no_attack_time = 0


