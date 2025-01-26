try:
    import board
    import neopixel
except NotImplementedError:
    pass


class Pixel:
    def __init__(self, period: int, divider=1.0):
        self.period = period
        self.dimmer = Dimmer(divider)
        self.pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

    def scan(self):
        self.set_pixel((0, self.period, self.period))

    def measure(self):
        self.set_pixel((0, 0, self.period))

    def done(self):
        self.set_pixel((0, self.period, 0))

    def wlan(self):
        self.pixel.fill((self.period, self.period, 0))

    def ntp(self):
        self.pixel.fill((self.period, 0, self.period))

    def sensors(self):
        self.pixel.fill((0, self.period, self.period))

    def mqtt(self):
        self.pixel.fill((self.period, self.period, self.period))

    def progress(self, value):
        self.set_pixel((value, self.period - value, 0))

    def set_pixel(self, rgb):
        rgb = tuple([self.dimmer.dim(value) for value in rgb])
        self.pixel.fill(rgb)


class Dimmer:

    def __init__(self, divider: float):
        self.divider = divider

    def dim(self, value):
        return int(round(value / self.divider))


if __name__ == "__main__":

    dimmer = Dimmer(7)
    for i in range(16):
        print(i, dimmer.dim(i))
