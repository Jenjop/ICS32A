# spots_game.py

import pygame
import spots



class SpotsGame:
    def __init__(self):
        self._running = True
        self._state = spots.SpotsState()

        
    def run(self) -> None:
        pygame.init()

        self._resize_surface((600, 600))

        clock = pygame.time.Clock()

        while self._running:
            clock.tick(30)
            self._handle_events()
            self._redraw()

        pygame.quit()


    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._on_mouse_button(event.pos)

        self._move_spots()


    def _redraw(self) -> None:
        surface = pygame.display.get_surface()

        surface.fill(pygame.Color(255, 255, 0))
        self._draw_spots()

        pygame.display.flip()


    def _draw_spots(self) -> None:
        for spot in self._state.all_spots():
            self._draw_spot(spot)


    def _draw_spot(self, spot: spots.Spot) -> None:
        frac_x, frac_y = spot.center()
        
        topleft_frac_x = frac_x - spot.radius()
        topleft_frac_y = frac_y - spot.radius()

        bottomright_frac_x = frac_x + spot.radius()
        bottomright_frac_y = frac_y + spot.radius()

        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()

        topleft_pixel_x = topleft_frac_x * width
        topleft_pixel_y = topleft_frac_y * height

        bottomright_pixel_x = bottomright_frac_x * width
        bottomright_pixel_y = bottomright_frac_y * height

        pygame.draw.ellipse(
            surface, pygame.Color(0, 0, 0),
            pygame.Rect(
                topleft_pixel_x, topleft_pixel_y,
                bottomright_pixel_x - topleft_pixel_x,
                bottomright_pixel_y - topleft_pixel_y))


    def _end_game(self) -> None:
        self._running = False


    def _resize_surface(self, size: (int, int)) -> None:
        pygame.display.set_mode(size, pygame.RESIZABLE)


    def _on_mouse_button(self, pos: (int, int)) -> None:
        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()
        
        pixel_x, pixel_y = pos
        
        frac_x = pixel_x / width
        frac_y = pixel_y / height

        self._state.handle_click((frac_x, frac_y))


    def _move_spots(self) -> None:
        self._state.move_all_spots()


if __name__ == '__main__':
    SpotsGame().run()
