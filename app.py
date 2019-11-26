from functools import partial
import time
from datetime import datetime

from lib import epd2in13
from modules.watches import Watches


class Application:
    STATE_INIT_FULL_UPDATE = 1
    STATE_INIT_PART_UPDATE = 2
    STATE_SWITCH_SCREEN_INIT = 3
    STATE_SWITCH_SCREEN_UPDATE = 4

    def __init__(self, modules):
        self.epd = epd2in13.EPD()

        self.modules = [{
            "last_switch": datetime.min,
            "interval": interval,
            "module": module((self.epd.height, self.epd.width))}
            for interval, module in modules
        ]
        self.active_module = None
        self.state = self.STATE_INIT_FULL_UPDATE

    def __del__(self):
        self.epd.sleep()

    def get_image(self):
        return self.epd.getbuffer(self.active_module.image)

    def loop(self):
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(255)

        while True:
            t = datetime.now()

            for it in self.modules:
                module = it["module"]
                module.update()

                if (t - it["last_switch"]).seconds >= it["interval"]:
                    it["last_switch"] = t
                    self.active_module = module
                    self.state = self.STATE_INIT_FULL_UPDATE
                    break
                elif self.active_module is None:
                    self.active_module = module

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
        (300, partial(Watches, update_interval=30))
    ])
    try:
        app.loop()
    except KeyboardInterrupt:
        del app
