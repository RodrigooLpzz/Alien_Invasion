import unittest
from unittest.mock import patch
import pygame
from alien_invasion import AlienInvasion
from ship import Ship
from bullet import Bullet
from alien import Alien

class TestAlienInvasion(unittest.TestCase):
    """Test cases for Alien Invasion game"""

    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch('pygame.display.set_mode')
    def setUp(self, mock_display):
        mock_display.return_value = pygame.Surface((1200, 800))
        self.ai = AlienInvasion()

    def test_game_initialization(self):
        """Test that game initializes properly"""
        self.ai._create_fleet() 
        self.assertIsInstance(self.ai, AlienInvasion)
        self.assertIsInstance(self.ai.ship, Ship)
        self.assertEqual(len(self.ai.bullets), 0)
        self.assertGreater(len(self.ai.aliens), 0)

    def test_ship_movement(self):
        """Test ship movement controls"""
        self.ai.ship.moving_right = True
        initial_pos = self.ai.ship.rect.x
        self.ai.ship.update()
        self.assertGreater(self.ai.ship.rect.x, initial_pos)

        self.ai.ship.moving_right = False
        self.ai.ship.moving_left = True
        initial_pos = self.ai.ship.rect.x
        self.ai.ship.update()
        self.assertLess(self.ai.ship.rect.x, initial_pos)

class TestBullet(unittest.TestCase):
    """Test cases for Bullet class"""

    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch('pygame.display.set_mode')
    def setUp(self, mock_display):
        mock_display.return_value = pygame.Surface((800, 600))
        self.ai = AlienInvasion()
        self.bullet = Bullet(self.ai)

    def test_bullet_movement(self):
        """Test bullet moves upward"""
        initial_pos = self.bullet.rect.y
        self.bullet.update()
        self.assertLess(self.bullet.rect.y, initial_pos)

class TestAlien(unittest.TestCase):
    """Test cases for Alien class"""

    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch('pygame.display.set_mode')
    def setUp(self, mock_display):
        mock_display.return_value = pygame.Surface((800, 600))
        self.ai = AlienInvasion()
        self.alien = Alien(self.ai)

    def test_alien_movement(self):
        """Test alien movement and edge detection"""
        initial_pos = self.alien.rect.x
        self.alien.update()
        self.assertGreater(self.alien.rect.x, initial_pos)

        self.alien.rect.right = self.ai.screen.get_rect().right
        self.assertTrue(self.alien.check_edges())

    def test_ship_hit(self):
        """Test ship hit detection and game over"""
        initial_lives = self.ai.stats.ships_left
        alien = Alien(self.ai)
        alien.rect.center = self.ai.ship.rect.center
        self.ai.aliens.add(alien)

        self.ai._ship_hit()
        self.assertEqual(self.ai.stats.ships_left, initial_lives - 1)

        self.ai.stats.ships_left = 1
        self.ai._ship_hit()
        self.assertFalse(self.ai.game_active)

    def test_key_events(self):
        """Test keyboard event handling"""
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        pygame.event.post(event)
        self.ai._check_events()
        self.assertTrue(self.ai.ship.moving_right)

        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT)
        pygame.event.post(event)
        self.ai._check_events()
        self.assertFalse(self.ai.ship.moving_right)

if __name__ == '__main__':
    unittest.main()
