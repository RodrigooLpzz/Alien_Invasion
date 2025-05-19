import pygame

from alien_invasion import AlienInvasion

class AIPlayer:

    def __init__(self, ai_game: AlienInvasion):
        """Automatic player for Alien Invasion"""

        # Need a reference to the game object
        self.ai_game = ai_game
        ai_game.playing_with_ia = True

        self.previous_level = self.ai_game.stats.level
    

    def run_game(self):
        """Replaces the original run_game(), so we can interject our own 
        controls"""

        # Start out in an active state
        self.ai_game.game_active = True
        self.ai_game._check_play_buttom()

        self.ai_game.settings.bullet_speed = 90
        self.ai_game.settings.ship_speed = 30


        # Start the main loop for the game
        while True:
            # Still call ai_game._check_events(), so we can use keyboard to 
            # quit

            self.ai_game._check_events()
            self._implement_strategy()

            current_level = self.ai_game.stats.level
            if current_level != self.previous_level:
                self.previous_level = current_level

                
            if self.ai_game.game_active:
                self.ai_game.ship.update()
                self.ai_game._update_bullets()
                self.ai_game._update_aliens()

            self.ai_game._update_screen()
            self.ai_game.clock.tick(60)

    def _implement_strategy(self):
        """Implement an automated strategy for playing the game."""

        if not self.ai_game.aliens:
            return

        target_alien = self._get_target_alien()
        ship = self.ai_game.ship

        # Moverse hacia el alien
        if ship.rect.centerx < target_alien.rect.centerx - 5:
            ship.moving_right = True
            ship.moving_left = False
        elif ship.rect.centerx > target_alien.rect.centerx + 5:
            ship.moving_right = False
            ship.moving_left = True
        else:
            # Ya está alineado con el alien
            ship.moving_right = False
            ship.moving_left = False

            # Si no hay balas, dispara
            if len(self.ai_game.bullets) == 0:
                self.ai_game._fire_bullet()



    def _get_target_alien(self):
        """Get a specific alien to target."""
        bot_x = self.ai_game.ship.rect.centerx
        # Find the right-most alien in the bottom row.
        #   Pick the first alien in the group. Then compare all others, 
        #   and return the alien with the greatest x and y rect attributes.
        target_alien = self.ai_game.aliens.sprites()[0]                 # 3
        for alien in self.ai_game.aliens.sprites():
            if alien.rect.y > target_alien.rect.y:                      # 4
                # This alien is farther down than target_alien.
                target_alien = alien
            elif alien.rect.y < target_alien.rect.y:                    # 5
                # This alien is above target_alien.
                continue
            else:
                if abs(alien.rect.x - bot_x) < abs(target_alien.rect.x - bot_x):
                    target_alien = alien

        return target_alien
        


        



if __name__ == '__main__':
    ai_game = AlienInvasion()

    ai_player = AIPlayer(ai_game)
    ai_player.run_game()
        