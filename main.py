from pyglet.window import Window
from pyglet.app import run
from pyglet import clock
from pyglet.shapes import BorderedRectangle
from pyglet.shapes import Rectangle
from pyglet.shapes import Circle
from pyglet.graphics import Batch
import random
import math


class Renderer(Window):
    def __init__(self):
        super().__init__()
        self.background = Rectangle(0, 0, self.width, self.height, color=(194, 172, 100, 255))
        self.die = Die(self.width, self.height / 2, self.width / 2)

    def on_draw(self):
        self.clear()
        self.background.draw()
        self.die.draw()

    def on_update(self, datetime):
        self.die.update(datetime)

    def on_key_press(self, symbol, modifiers):
        self.die = Die(self.width, self.height / 2, self.width / 2)

class Die:
    def __init__(self, x, y, end_x):
        self.x = x
        self.y = y
        self.end_x = end_x
        eyespositions = [
            ((7.5, 7.5),),
            ((-25, -25), (40, 40)),
            ((-25, -25), (7.5, 7.5), (40, 40)),
            ((-25, -25), (40, -25), (40, 40), (-25, 40)),
            ((-25, -25), (40, -25), (7.5, 7.5), (40, 40), (-25, 40)),
            ((-25, -25), (-25, 7.5), (40, -25), (40, 40), (40, 7.5), (-25, 40)),
        ]
        self.surface = BorderedRectangle(x, y, 100, 100, border=2, color=(232, 224, 198, 255), border_color=(248, 246, 238, 255))
        self.schadow = Rectangle(x, y - 50, 100, 5, color=(0, 0, 0, 25))
        self.eyes = []
        self.batch = Batch()
        for o in random.choice(eyespositions):
            eye = Rectangle(x, y, 15, 15, color=(0, 0, 0), batch=self.batch)
            eye.anchor_position = o
            self.eyes.append(eye)
        self.surface.anchor_position = 50, 50
        self.schadow.anchor_position = 50, 2.5
        self.animation_length = 1
        self.animation_time = 0

    def update(self, datetime):
        self.animation_time += datetime
        if self.animation_time < self.animation_length:
            xx = math.pi / 2 * self.animation_time
            road = math.sin(xx)
            rotation = road * -360
            jump = math.pi * 4 * rotation / -360
            curves = abs(math.sin(jump))
            for o in self.eyes:
                o.y = self.y + curves * 25
                o.x = self.x - road * self.end_x
                o.rotation = rotation
                o.opacity = int(self.animation_time * 250)
            self.surface.y = self.y + curves * 25
            self.surface.x = self.x - road * self.end_x
            self.schadow.x = self.x - road * self.end_x - curves * 10
            self.schadow.width = 100 + curves * 20
            self.schadow.height = 5 + curves * 5
            self.surface.rotation = rotation

    def draw(self):
        self.schadow.draw()
        self.surface.draw()
        self.batch.draw()

renderer = Renderer()
clock.schedule_interval(renderer.on_update, 1 / 60)
run()
