# spots.py

import math
import random



class Spot:
    def __init__(self, center: (float, float), radius: float):
        self._center = center
        self._radius = radius
        self._delta_x = (random.random() * 0.01) - 0.005
        self._delta_y = (random.random() * 0.01) - 0.005


    def center(self) -> (float, float):
        return self._center


    def radius(self) -> float:
        return self._radius


    def move(self) -> None:
        x, y = self._center
        self._center = (x + self._delta_x, y + self._delta_y)


    def contains(self, point: (float, float)) -> bool:
        px, py = point
        cx, cy = self._center
        
        return math.sqrt((px - cx) * (px - cx) + (py - cy) * (py - cy)) <= self._radius
    


class SpotsState:
    def __init__(self):
        self._spots = []


    def all_spots(self) -> [Spot]:
        return self._spots


    def handle_click(self, click_point: (float, float)) -> None:
        for spot in self._spots:
            if spot.contains(click_point):
                self._spots.remove(spot)
                return
        
        self._spots.append(Spot(click_point, 0.05))


    def move_all_spots(self) -> None:
        for spot in self._spots:
            spot.move()

