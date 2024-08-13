from settings import *
from pygame.time import get_ticks

class Timer:
    def __init__(self, duration, func = None, repeat = None, autostart = False) -> None:
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.func = func
        self.autostart = autostart
        self.repeat = repeat

        if self.autostart:
            self.activate()

    def __bool__(self):
        return self.active

    def activate(self):
        self.active = True
        self.start_time = get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()


    def update(self):
        if get_ticks() - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()