class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.ship_speed = 10
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 3
        self.bullet_width = 10.0
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 100

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 0.5
        # fleet_direction of 1 represents right; -1 represent left
        self.fleet_direction = 1