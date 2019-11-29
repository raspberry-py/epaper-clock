import time
from datetime import datetime
from itertools import cycle

from lib import epd2in13
from modules.watches import Watches


class Application:
    STATE_INIT_FULL_UPDATE = 1
    STATE_INIT_PART_UPDATE = 2
    STATE_SWITCH_SCREEN_INIT = 3
    STATE_SWITCH_SCREEN_UPDATE = 4

    def __init__(self, modules):
        assert len(modules) > 0

        self.epd = epd2in13.EPD()

        self.modules = cycle(map(lambda m: (m[0], m[1]((self.epd.height, self.epd.width))), modules))

        self.state = self.STATE_INIT_FULL_UPDATE

        self.last_switch = datetime.min
        self.active_module = None

    def __del__(self):
        self.epd.sleep()

    def get_image(self):
        return self.epd.getbuffer(self.active_module[1].image)

    def loop(self):
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(255)

        while True:
            t = datetime.now()

            if self.active_module is None or (t - self.last_switch).seconds >= self.active_module[0]:
                self.active_module = next(self.modules)
                self.last_switch = t
                self.state = self.STATE_INIT_FULL_UPDATE

            self.active_module[1].update()

            if self.state == self.STATE_INIT_FULL_UPDATE:
                self.epd.init(self.epd.FULL_UPDATE)
                self.state = self.STATE_SWITCH_SCREEN_INIT

            if self.state == self.STATE_INIT_PART_UPDATE:
                self.epd.init(self.epd.PART_UPDATE)
                self.state = self.STATE_SWITCH_SCREEN_UPDATE

            if self.state == self.STATE_SWITCH_SCREEN_INIT:
                self.epd.displayPartBaseImage(self.get_image())
                self.state = self.STATE_INIT_PART_UPDATE

            if self.state == self.STATE_SWITCH_SCREEN_UPDATE:
                self.epd.displayPartial(self.get_image())

            time.sleep(5)


if __name__ == '__main__':
    app = Application([
        (300, Watches)
    ])
    try:
        app.loop()
    except KeyboardInterrupt:
        del app
