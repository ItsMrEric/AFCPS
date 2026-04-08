import pygame
import math
from pydub import AudioSegment
import pygame

# ===== CONFIG =====
WIDTH, HEIGHT = 800, 600
FPS = 60
BPM = 138.0
N_MOTORS = 5
N_MOTORS_PUMPS = 5
N_LEDS1 = 30
N_LEDS2 = 84


# angular frequency (rad/s)
omega = 2 * math.pi * BPM / 60.0


# ===== FUNCTIONS =====
def tconv(x):
    s = str(int(x))

    if len(s) <= 5:
        return int(s)

    base = int(s[-5:])     # LAST 5 digits
    prefix = int(s[:-5])   # EVERYTHING BEFORE THEM

    return prefix * 60000 + base
def untconv(ms):
    prefix = ms // 60000
    base = ms % 60000

    return prefix * 100000 + base

# ===== MOTION FUNCTIONS =====



def n(i, t):
    return 0

def sin1(i, t):
    return 10 * math.sin(t * 0.002 + i)
def sin2(i, t):
    return math.sin(t * 0.002) * 30
def sin3(i, t):
    return math.sin(t * 0.005 + i) * 30
def sin4(i, t_ms):
    t = t_ms / 1000.0
    return math.sin((omega / 1.8) * t + i) * 10
def sin5(i, t_ms):
    t = t_ms / 1000.0
    return math.sin((omega / 2.0) * t - 0.5 + i) * 10
def saw1(t_ms, i, bpm=138.0):
    f = bpm / 120.0
    t = t_ms / 1000.0
    phase = f * t
    return (phase - math.floor(phase)) * 2 - 1
def sin6(i, t_ms):
    t = t_ms / 1000.0
    return math.sin((omega / 1.8) * t + i) * 6


def led1_n(i, t):
    return (0, 0, 0)

def led1_wave(i, t):
    return (-255, -255, -math.sin(t * 0.005 + i) * 100 - 100)

def led2_n(i, t):
    return (0, 0, 0)

def led2_wave(i, t):
    return (-255, -255, -math.sin(t * 0.005 + i) * 100 - 100)


def shift_layers(layers, offset):
    new_layers = []
    for layer in layers:
        new_layers.append(
            l(
                untconv(layer.start + offset),
                untconv(layer.end + offset),
                layer.fade_in,
                layer.fade_out,
                layer.motors,
                layer.pumps,
                layer.motion
            )
        )
    return new_layers
def shift_layers_led1(layers, offset):
    new_layers = []
    for layer in layers:
        
        new_layers.append(
            led1_l(
                untconv(layer.start + offset),
                untconv(layer.end + offset),
                layer.fade_in,
                layer.fade_out,
                layer.leds,
                layer.led_motion
            )
        )
    return new_layers
def shift_layers_led2(layers, offset):
    new_layers = []
    for layer in layers:
        
        new_layers.append(
            led2_l(
                untconv(layer.start + offset),
                untconv(layer.end + offset),
                layer.fade_in,
                layer.fade_out,
                layer.leds,
                layer.led_motion
            )
        )
    return new_layers

def shift_start(layers, offset):
    new_layers = []
    for layer in layers:
        new_layers.append(
            l(
                untconv(layer.start + offset),
                untconv(layer.end),
                layer.fade_in,
                layer.fade_out,
                layer.motors,
                layer.pumps,
                layer.motion
            )
        )
    return new_layers
def shift_start_led1(layers, offset):
    new_layers = []
    for layer in layers:
        new_layers.append(
            led1_l(
                untconv(layer.start + offset),
                untconv(layer.end),
                layer.fade_in,
                layer.fade_out,
                layer.leds,
                layer.led_motion
            )
        )
    return new_layers
def shift_start_led2(layers, offset):
    new_layers = []
    for layer in layers:
        new_layers.append(
            led2_l(
                untconv(layer.start + offset),
                untconv(layer.end + offset),
                layer.fade_in,
                layer.fade_out,
                layer.leds,
                layer.led_motion
            )
        )
    return new_layers

def shift_end(layers, offset):
    new_layers = []
    for layer in layers:
        new_layers.append(
            l(
                untconv(layer.start),
                untconv(layer.end + offset),
                layer.fade_in,
                layer.fade_out,
                layer.motors,
                layer.pumps,
                layer.motion
            )
        )
    return new_layers
def shift_end_led1(layers, offset):
    new_layers = []
    for layer in layers:
        new_layers.append(
            led1_l(
                untconv(layer.start + offset),
                untconv(layer.end + offset),
                layer.fade_in,
                layer.fade_out,
                layer.leds,
                layer.led_motion
            )
        )
    return new_layers
def shift_end_led2(layers, offset):
    new_layers = []
    for layer in layers:
        new_layers.append(
            led2_l(
                untconv(layer.start + offset),
                untconv(layer.end + offset),
                layer.fade_in,
                layer.fade_out,
                layer.leds,
                layer.led_motion
            )
        )
    return new_layers

# ===== LAYER CLASS =====
class l:
    def __init__(self, start, end, fade_in, fade_out, motors, pumps, motion):
        self.start = tconv(start)
        self.end = tconv(end)
        self.fade_in = fade_in
        self.fade_out = fade_out
        self.motors = motors
        self.pumps = pumps
        self.motion = motion

    def active(self, t):
        return self.start <= t <= self.end

    def weight(self, t):
        local_t = t - self.start
        total = self.end - self.start

        if self.fade_in > 0 and local_t < self.fade_in:
            return local_t / self.fade_in

        elif self.fade_out > 0 and local_t > total - self.fade_out:
            return 1.0 - (local_t - (total - self.fade_out)) / self.fade_out

        else:
            return 1.0
        
class led1_l:
    def __init__(self, start, end, fade_in, fade_out, leds = [(255, 255, 255)] * 30, led_motion = led1_n):
        self.start = tconv(start)
        self.end = tconv(end)
        self.fade_in = fade_in
        self.fade_out = fade_out
        self.leds = leds
        self.led_motion = led_motion

    def active(self, t):
        return self.start <= t <= self.end

    def weight(self, t):
        local_t = t - self.start
        total = self.end - self.start

        if self.fade_in > 0 and local_t < self.fade_in:
            return local_t / self.fade_in

        elif self.fade_out > 0 and local_t > total - self.fade_out:
            return 1.0 - (local_t - (total - self.fade_out)) / self.fade_out

        else:
            return 1.0
        
class led2_l:
    def __init__(self, start, end, fade_in, fade_out, leds = [(255, 255, 255)] * 84, led_motion = led2_n):
        self.start = tconv(start)
        self.end = tconv(end)
        self.fade_in = fade_in
        self.fade_out = fade_out
        self.leds = leds
        self.led_motion = led_motion

    def active(self, t):
        return self.start <= t <= self.end

    def weight(self, t):
        local_t = t - self.start
        total = self.end - self.start

        if self.fade_in > 0 and local_t < self.fade_in:
            return local_t / self.fade_in

        elif self.fade_out > 0 and local_t > total - self.fade_out:
            return 1.0 - (local_t - (total - self.fade_out)) / self.fade_out

        else:
            return 1.0
        


# ===== LAYERS =====
led1_layers = shift_layers_led1([
    led1_l(1000, 400920, 340, 0),
    led1_l(137360, 400920, 340, 0, led_motion = led1_wave),
    led1_l(149530, 400920, 340, 0),
    led1_l(342550, 400920, 58370, 0, [(0, 0, 0)] * 30),
], 750)

led2_layers = shift_layers_led2([
    led2_l(1000, 400920, 340, 0),
    led2_l(137360, 400920, 340, 0, led_motion = led2_wave),
    led2_l(149530, 400920, 340, 0),
    led2_l(342550, 400920, 58370, 0, [(0, 0, 0)] * 84),
], 750)




layers = [
    l(
        start=700, end=12170,
        fade_in=1000, fade_out=1000,
        motors=[90, -1, 90, -1, 90],
        pumps=[0, -1, 0, -1, 0],
        motion=sin2
    ),
]
temp0 = [
    l(0, 200, 0, 0, [-1, -1, -1, -1, -1], [100, -1, 100, -1, 100], n),
    l(430, 650, 0, 0, [-1, -1, -1, -1, -1], [100, -1, 100, -1, 100], n),
    l(860, 1060, 0, 0, [-1, -1, -1, -1, -1], [100, -1, 100, -1, 100], n),
    l(1300, 1400, 0, 0, [-1, -1, -1, -1, -1], [100, -1, 100, -1, 100], n),
    l(1510, 1630, 0, 0, [-1, -1, -1, -1, -1], [100, -1, 100, -1, 100], n),
    l(1950, 2390, 0 ,0, [-1, -1, -1, -1, -1], [100, -1, 0, -1, 0], n),
    l(2390, 2600, 0, 0, [-1, -1, -1, -1, -1], [0, -1, 100, -1, 0], n),
    l(2600, 2820, 0, 0, [-1, -1, -1, -1, -1], [0, -1, 0, -1, 100], n),
    l(3040, 3260, 0, 0, [-1, -1, -1, -1, -1], [100, -1, 100, -1, 100], n),
]
for i in range(4):
    layers += shift_layers(temp0, i * 3440 + 700)


temp1= [
    l(12800, 17300, 0, 0, [-1, -1, -1, -1, -1], [0, -1, 0, -1, 0], n),
    l(12801, 17300, 900, 0, [-1, -1, -1, -1, -1], [200, -1, 200, -1, 200], n),
    l(13600, 17360, 0, 0, [90, -1, 90, -1, 90], [200, -1, 200, -1, 200], n),
    l(13601, 17360, 850, 0, [80, -1, 80, -1, 80], [200, -1, 200, -1, 200], n),
    l(13890, 17360, 850, 0, [100, -1, 100, -1, 100], [200, -1, 200, -1, 200], n),
    l(14740, 17360, 890, 0, [80, -1, 80, -1, 80], [200, -1, 200, -1, 200], n),
    l(15630, 17360, 860, 0, [100, -1, 100, -1, 100], [200, -1, 200, -1, 200], n),
    l(16500, 17360, 860, 0, [80, -1, 80, -1, 80], [200, -1, 200, -1, 200], n),
    l(17360, 20830, 860, 0, [80, -1, 80, -1, 80], [200, -1, 200, -1, 200], n),
    l(17361, 20830, 850, 0, [90, -1, 90, -1, 90], [150, -1, 150, -1, 150], sin3),
    l(18000, 20830, 240, 0, [80, -1, 90, -1, 100], [130, -1, 150, -1, 130], n),
    l(18800, 20830, 130, 0, [100, -1, 90, -1, 80], [150, -1, 200, -1, 150], n),
    l(19540, 20830, 500, 0, [90, -1, 90, -1, 90], [100, -1, 100, -1, 100], sin3),
    l(20200, 20830, 629, 0, [80, -1, 80, -1, 80], [200, -1, 200, -1, 200], n),
    l(20830, 27819, 0, 0, [80, -1, 80, -1, 80], [200, -1, 200, -1, 200], n),
    l(20831, 27819, 860, 0, [100, -1, 100, -1, 100], [200, -1, 200, -1, 200], n),
    l(21690, 27819, 860, 0, [80, -1, 80, -1, 80], [200, -1, 200, -1, 200], n),
    l(22550, 27819, 860, 0, [100, -1, 100, -1, 100], [200, -1, 200, -1, 200], n),
    l(23410, 27819, 860, 0, [100, -1, 90, -1, 80], [150, -1, 200, -1, 150], n),
    l(24680, 27819, 500, 0, [90, -1, 100, -1, 110], [200, -1, 180, -1, 160], n),
    l(25500, 27819, 500, 0, [70, -1, 80, -1, 90], [160, -1, 180, -1, 200], n),
    l(26500, 27819, 1000, 0, [90, -1, 90, -1, 90], [100, -1, 100, -1, 100], sin3),
    l(26500, 27819, 1270, 0, [-1, -1, -1, -1, -1], [0, -1, 0, -1, 0], n),
]

layers += shift_layers(temp1, 750)
temp2 = [
    l(27821, 31299, 0, 0, [-1, -1, -1, -1, -1], [0, -1, 0, -1, 0], n),
    l(27822, 31299, 1715, 0, [-1, -1, -1, -1, -1], [230, -1, 230, -1, 230], n),
    l(29540, 31299, 1720, 0, [-1, -1, -1, -1, -1], [50, -1, 50, -1, 50], n),
    l(31300, 34779, 0, 0, [-1, -1, -1, -1, -1], [50, -1, 50, -1, 50], n),
    l(31301, 34779, 1715, 0, [-1, -1, -1, -1, -1], [230, -1, 230, -1, 230], n),
    l(33060, 34779, 1709, 0, [-1, -1, -1, -1, -1], [50, -1, 50, -1, 50], n)
]
layers += shift_layers(temp2, 750)

temp3 = [
    l(27820, 34770, 0, 0, [80, -1, 80, -1, 80], [-1, -1, -1, -1, -1], n),
    l(27821, 34770, (34770 - 27820) / 16 - 1, 0, [100, -1, 100, -1, 100], [-1, -1, -1, -1, -1], n),
    l(28250, 34770, (34770 - 27820) / 16 - 1, 0, [80, -1, 80, -1, 80], [-1, -1, -1, -1, -1], n)
]

for i in range(16):
    layers += shift_start(shift_layers(temp3, 750), i * ((34770 - 27820) / 8))

temp4 = [
    l(34780, 40870, 0, 0, [-1, -1, -1, -1, -1], [0, -1, 0, -1, 0], n),
    l(34781, 40870, 1710, 0, [-1, -1, -1, -1, -1], [230, -1, 230, -1, 230], n),
    l(36500, 40870, 1710, 0, [-1, -1, -1, -1, -1], [100, -1, 100, -1, 100], n),
    l(36500, 40870, 1710, 0, [-1, -1, -1, -1, -1], [230, -1, 230, -1, 230], n),
    l(38240, 40870, 1710, 0, [-1, -1, -1, -1, -1], [100, -1, 100, -1, 100], n),
    l(34780, 40870, 0, 0, [70, -1, 80, -1, 90], [-1, -1, -1, -1, -1], n),
    l(34781, 40870, 859, 0, [90, -1, 100, -1, 110], [-1, -1, -1, -1, -1], n),
    l(35641, 40870, 858, 0, [90, -1, 80, -1, 70], [-1, -1, -1, -1, -1], n),
    l(36500, 40870, 859, 0, [110, -1, 100, -1, 90], [-1, -1, -1, -1, -1], n),
    l(37360, 40870, 859, 0, [80, -1, 80, -1, 80], [-1, -1, -1, -1, -1], n),
    l(38260, 40870, 859, 0, [90, -1, 90, -1, 90], [-1, -1, -1, -1, -1], sin5),
    l(40000, 40870, 870, 0, [90, -1, 90, -1, 90], [100, -1, 100, -1, 100], n),
]
layers += shift_layers(temp4, 750)
temp5 = [
    l(40870, 41720, 0, 0, [90, -1, 90, -1, 90], [100, -1, 100, -1, 100], n),
    l(40871, 41720, 420, 0, [100, -1, 100, -1, 100], [150, -1, 150, -1, 150], n ),
    l(41295, 41720, 420, 0, [80, -1, 80, -1, 80], [200, -1, 200, -1, 200], n),
    l(41720, 43459, 0, 0, [80, -1, 80, -1, 80], [200, -1, 200, -1, 200], n),
    l(41721, 43459, 850, 0, [100, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(42160, 43459, 850, 0, [-1, -1, 110, -1, -1], [-1, -1, -1, -1, -1], n),
    l(42590, 43459, 850, 0, [-1, -1, -1, -1, 120], [-1, -1, -1, -1, -1], n),
    l(43460, 48669, 0, 0, [100, -1, 110, -1, 120], [200, -1, 200, -1, 200], n),
    l(43461, 48669, 850, 0, [60, -1, 70, -1, 80], [200, -1, 200, -1, 200], n),
    l(44320, 48669, 850, 0, [90, -1, 90, -1, 90], [-1, -1, -1, -1, -1], n),
    l(45200, 48669, 500, 0, [90, -1, 90, -1, 90], [100, -1, 100, -1, 100], sin4),
    l(45570, 48669, 500, 0, [100, -1, 90, -1, 80], [180, -1, 180, -1, 180], n),
    l(46220, 48669, 500, 0, [80, -1, 90, -1, 100], [200, -1, 200, -1, 200], n),
    l(46660, 48669, 500, 0, [90, -1, 90, -1, 90], [100, -1, 100, -1, 100], sin1),
    l(48268, 48669, 200, 0, [70, -1, 70, -1, 70], [50, -1, 50, -1, 50], n),
]
layers += shift_layers(temp5, 750)

temp6 = [
    l(48670, 55629, 0, 0, [70, -1, 70, -1, 70], [50, -1, 50, -1, 50], n),
    l(48671, 55629, 1710, 0, [110, -1, 110, -1, 110], [200, -1, 200, -1, 200], n),
    l(50430, 55629, 850, 0, [80, -1, 80, -1, 80], [150, -1, 150, -1, 150], n),
    l(51290, 55629, 850, 0, [100, -1, 90, -1, 80], [100, -1, 200, -1, 100], n),
    l(51291, 55629, 700, 0, [-1, -1, 90, -1, -1], [-1, -1, -1, -1, -1], sin4),
    l(53460, 55629, 640, 0, [80, -1, 80, -1, 80], [200, -1, 200, -1, 200], n),
    l(54100, 55629, 700, 0, [80, -1, 80, -1, 80], [-1, -1, -1, -1, -1], sin4),
    l(54770, 55629, 640, 0, [100, -1, 100, -1, 100], [200, -1, 200, -1, 200], n),
    l(55630, 109100, 0, 0, [100, -1, 100, -1, 100], [200, -1, 200, -1, 200], n),
    l(55631, 109100, 860, 0, [80, -1, 80, -1, 80], [230, -1, 230, -1, 230], n),
    l(56500, 109100, 860, 0, [100, -1, 100, -1, 100], [230, -1, 230, -1, 230], n),
    l(57370, 109100, 640, 0, [80, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(57800, 109100, 860, 0, [-1, -1, 80, -1, -1], [-1, -1, -1, -1, -1], n),
    l(58240, 109100, 860, 0, [-1, -1, -1, -1, 80], [-1, -1, -1, -1, -1], n),
    l(59110, 109100, 430, 0, [90, -1, 90, -1, 90], [-1, -1, -1, -1, -1], sin6),
    l(59110, 109100, 860, 0, [-1, -1, -1, -1, -1], [130, -1, 180, -1, 230], n),
    l(59980, 109100, 860, 0, [90, -1, 100, -1, 110], [230, -1, 180, -1, 130], n),
    l(100860, 109100, 430, 0, [90, -1, 90, -1, 90], [100, -1, 100, -1, 100], sin5),
    l(102580, 109100, 1720, 0, [90, -1, 90, -1, 90], [240, -1, 240, -1, 240], n),
    l(104320, 109100, 1720, 0, [-1, -1, -1, -1, -1], [50, -1, 50, -1, 50], n),
    l(104330, 109100, 430, 0, [85, -1, 85, -1, 85], [-1, -1, -1, -1, -1], n),
    l(104760, 109100, 430, 0, [95, -1, 95, -1, 95], [-1, -1, -1, -1, -1], n),
    l(105200, 109100, 430, 0, [85, -1, 85, -1, 85], [-1, -1, -1, -1, -1], n),
    l(105630, 109100, 430, 0, [100, -1, 100, -1, 100], [-1, -1, -1, -1, -1], n),
    l(106070, 109100, 0, 0, [-1, -1, -1, -1, -1], [200, -1, 200, -1, 200], n),
    l(106071, 109100, 1270, 0, [-1, -1, -1, -1, -1], [50, -1, 50, -1, 50], n),
    l(106060, 109100, 1270, 0, [80, -1, 80, -1, 80], [-1, -1, -1, -1, -1], n),
    l(107370, 109100, 0, 0, [-1, -1, -1, -1, -1], [235, -1, 235, -1, 235], n),
    l(107371, 109100, 1000, 0, [-1, -1, -1, -1, -1], [0, -1, 0, -1, 0], n),
    l(107370, 109100, 1000, 0, [90, -1, 90, -1, 90], [-1, -1, -1, -1, -1], n),
    l(109110, 137350, 0, 0, [90, -1, 90, -1, 90], [0, -1, 0, -1, 0], n),
    l(109111, 137350, 430, 0, [75, -1, 75, -1, 75], [255, -1, 255, -1, 255], n),
    l(109540, 137350, 860, 0, [105, -1, 105, -1, 105], [-1, -1, -1, -1, -1], n),
    l(110410, 137350, 860, 0, [75, -1, 75, -1, 75], [-1, -1, -1, -1, -1], n),
    l(111290, 137350, 860, 0, [-1, -1, -1, -1, 105], [-1, -1, -1, -1, -1], n),
    l(111720, 137350, 860, 0, [-1, -1, 105, -1, -1], [-1, -1, -1, -1, -1], n),
    l(112150, 137350, 860, 0, [105, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(113020, 137350, 860, 0, [75, -1, 75, -1, 75], [-1, -1, -1, -1, -1], n),
    l(113890, 137350, 860, 0, [105, -1, 105, -1, 105], [-1, -1, -1, -1, -1], n),
    l(114760, 137350, 860, 0, [75, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(115190, 137350, 860, 0, [-1, -1, 75, -1, -1], [-1, -1, -1, -1, -1], n),
    l(115630, 137350, 860, 0, [-1, -1, -1, -1, 75], [-1, -1, -1, -1, -1], n),
    l(116500, 137350, 860, 0, [90, -1, 80, -1, 70], [-1, -1, -1, -1, -1], n),
    l(117370, 137350, 860, 0, [110, -1, 100, -1, 90], [-1, -1, -1, -1, -1], n),
    l(118240, 137350, 860, 0, [80, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(118670, 137350, 860, 0, [-1, -1, 80, -1, -1], [-1, -1, -1, -1, -1], n),
    l(119110, 137350, 860, 0, [-1, -1, -1, -1, 80], [-1, -1, -1, -1, -1], n),
    l(119980, 137350, 860, 0, [100, -1, 100, -1, 100], [-1, -1, -1, -1, -1], n),
    l(120850, 137350, 430, 0, [85, -1, 85, -1, 85], [-1, -1, -1, -1, -1], n),
    l(121280, 137350, 430, 0, [95, -1, 95, -1, 95], [-1, -1, -1, -1, -1], n),
    l(121720, 137350, 860, 0, [80, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(122150, 137350, 860, 0, [-1, -1, 80, -1, -1], [-1, -1, -1, -1, -1], n),
    l(122580, 137350, 860, 0, [-1, -1, -1, -1, 80], [-1, -1, -1, -1, -1], n),
    l(123450, 137350, 0, 0, [80, -1, 80, -1, 80], [255, -1, 255, -1, 255], n),
    l(123451, 137350, 860, 0, [-1, -1, -1, -1, -1], [200, -1, 200, -1, 200], n),
    l(123451, 137350, 860, 0, [90, -1, 90, -1, 90], [-1, -1, -1, -1, -1], sin6),
    l(124540, 137350, 430, 0, [80, -1, 90, -1, 100], [255, -1, 255, -1, 255], n),
    l(125190, 137350, 640, 0, [100, -1, 90, -1, 80], [255, -1, 255, -1, 255], n),
    l(126280, 137350, 640, 0, [80, -1, 80, -1, 80], [-1, -1, -1, -1, -1], n),
    l(126930, 137350, 860, 0, [100, -1, 100, -1, 100], [-1, -1, -1, -1, -1], n),
    l(127800, 137350, 860, 0, [80, -1, 80, -1, 80], [-1, -1, -1, -1, -1], n),
    l(128670, 137350, 430, 0, [95, -1, 95, -1, 95], [-1, -1, -1, -1, -1], n),
    l(129100, 137350, 430, 0, [85, -1, 85, -1, 85], [-1, -1, -1, -1, -1], n),
    l(129540, 137350, 860, 0, [100, -1, 100, -1, 100], [-1, -1, -1, -1, -1], n),
    l(130410, 137350, 860, 0, [80, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(130840, 137350, 860, 0, [-1, -1, 80, -1, -1], [-1, -1, -1, -1, -1], n),
    l(131280, 137350, 860, 0, [-1, -1, -1, -1, 80], [-1, -1, -1, -1, -1], n),
    l(132150, 137350, 430, 0, [95, -1, 95, -1, 95], [-1, -1, -1, -1, -1], n),
    l(132580, 137350, 430, 0, [85, -1, 85, -1, 85], [-1, -1, -1, -1, -1], n),
    l(133020, 137350, 430, 0, [95, -1, 95, -1, 95], [-1, -1, -1, -1, -1], n),
    l(133450, 137350, 430, 0, [85, -1, 85, -1, 85], [-1, -1, -1, -1, -1], n),
    l(133890, 137350, 500, 0, [100, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(134100, 137350, 500, 0, [-1, -1, 100, -1, -1], [-1, -1, -1, -1, -1], n),
    l(134320, 137350, 500, 0, [-1, -1, -1, -1, 100], [-1, -1, -1, -1, -1], n),
    l(134760, 137350, 500, 0, [80, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(134970, 137350, 500, 0, [-1, -1, 80, -1, -1], [-1, -1, -1, -1, -1], n),
    l(135190, 137350, 500, 0, [-1, -1, -1, -1, 80], [-1, -1, -1, -1, -1], n),
    l(135620, 137350, 860, 0, [105, -1, -1, -1, -1], [50, -1, -1, -1, -1], n),
    l(136060, 137350, 860, 0, [-1, -1, 105, -1, -1], [-1, -1, 50, -1, -1], n),
    l(136490, 137350, 840, 0, [-1, -1, -1, -1, 105], [-1, -1, -1, -1, 50], n),
    l(137351, 149530, 0, 0, [105, -1, 105, -1, 105], [50, -1, 50, -1, 50], n),
    l(137360, 149530, 1720, 0, [-1, -1, -1, -1, -1], [130, -1, 130, -1, 130], n),
    l(139100, 149530, 1720, 0, [-1, -1, -1, -1, -1], [50, -1, 50, -1, 50], n),
    l(140840, 149530, 1720, 0, [-1, -1, -1, -1, -1], [130, -1, 130, -1, 130], n),
    l(142580, 149530, 1720, 0, [-1, -1, -1, -1, -1], [50, -1, 50, -1, 50], n),
    l(144320, 149530, 1720, 0, [-1, -1, -1, -1, -1], [130, -1, 130, -1, 130], n),
    l(146060, 149530, 1720, 0, [-1, -1, -1, -1, -1], [50, -1, 50, -1, 50], n),
    l(147800, 149530, 1290, 0, [-1, -1, -1, -1, -1], [100, -1, 100, -1, 100], n),
]

layers += shift_layers(temp6, 750)

temp7 = [
    l(137360, 149530, 0, 0, [105, -1, 105, -1, 105], [-1, -1, -1, -1, -1], n),
    l(137361, 149530, 430, 0, [75, -1, 75, -1, 75], [-1, -1, -1, -1, -1], n),
    l(137800, 149530, 430, 0, [105, -1, 105, -1, 105], [-1, -1, -1, -1, -1], n),
]

for i in range (4):
    layers += shift_layers(shift_start(temp7, i*867), 750)

temp8 = [
    l(140840, 149530, 430, 0, [75, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(141060, 149530, 430, 0, [-1, -1, 75, -1, -1], [-1, -1, -1, -1, -1], n),
    l(141280, 149530, 430, 0, [-1, -1, -1, -1, 75], [-1, -1, -1, -1, -1], n),
    l(141710, 149530, 430, 0, [105, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(141930, 149530, 430, 0, [-1, -1, 105, -1, -1], [-1, -1, -1, -1, -1], n),
    l(142140, 149530, 430, 0, [-1, -1, -1, -1, 105], [-1, -1, -1, -1, -1], n),
    l(142580, 149530, 860, 0, [90, -1, 90, -1, 90], [-1, -1, -1, -1, -1], sin6),
    l(144320, 149530, 430, 0, [105, -1, 105, -1, 105], [-1, -1, -1, -1, -1], n),
    l(144750, 149530, 430, 0, [75, -1, 75, -1, 75], [-1, -1, -1, -1, -1], n),
    l(145129, 149530, 430, 0, [105, -1, 105, -1, 105], [-1, -1, -1, -1, -1], n),
    l(145620, 149530, 430, 0, [75, -1, 75, -1, 75], [-1, -1, -1, -1, -1], n),
    l(146060, 149530, 430, 0, [105, -1, 105, -1, 105], [-1, -1, -1, -1, -1], n),
    l(146490, 149530, 430, 0, [75, -1, 75, -1, 75], [-1, -1, -1, -1, -1], n),
    l(146930, 149530, 430, 0, [105, -1, 105, -1, 105], [-1, -1, -1, -1, -1], n),
    l(147360, 149530, 430, 0, [75, -1, 75, -1, 75], [-1, -1, -1, -1, -1], n),
    l(147800, 149530, 430, 0, [105, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(148230, 149530, 430, 0, [-1, -1, 105, -1, -1], [-1, -1, -1, -1, -1], n),
    l(148670, 149530, 430, 0, [-1, -1, -1, -1, 105], [-1, -1, -1, -1, -1], n),
    l(148670, 149530, 430, 0, [75, -1, -1, -1, -1], [-1, -1, -1, -1, -1], n),
    l(149110, 149530, 430, 0, [-1, -1, 75, -1, 75], [-1, -1, -1, -1, -1], n),
]
layers += shift_layers(temp8, 750)

temp9 = [
    l(149530, 158230, 0, 0, [75, -1, 75, -1, 75], [100, -1, 100, -1, 100], n),
    l(149531, 158230, 860, 0, [100, -1, 100, -1, 100], [-1, -1, -1, -1, -1], sin6),
    l(150040, 158230, 860, 0, [70, -1, 70, -1, 70], [200, -1, 200, -1, 200], n),
    l(151270, 158230, 1090, 0, [95, -1, 95, -1, 95], [-1, -1, -1, -1, -1], n),
    l(152360, 158230, 430, 0, [85, -1, 85, -1, 85], [-1, -1, -1, -1, -1], n),
    l(153010, 158230, 860, 0, [100, -1, 100, -1, 100], [-1, -1, -1, -1, -1], n),

]

layers += shift_layers(temp9, 750)










base_motors = [90] * N_MOTORS
base_pumps = [0] * N_MOTORS_PUMPS
base_leds1 = [(0, 0, 0)] * N_LEDS1
base_leds2 = [(0, 0, 0)] * N_LEDS2

t = 130000

t = tconv(t)

# ===== INIT PYGAME =====
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-Layer Pump + Motor Simulation")
clock = pygame.time.Clock()

audio = AudioSegment.from_file(r"d:\All my stuff\Music\Other's songs\Viva La Vida.mp3")
start_ms = t
cut = audio[start_ms:]
cut.export("temp.wav", format="wav")
pygame.mixer.music.load("temp.wav")
pygame.mixer.music.play()

running = True

while running:
    dt = clock.tick(FPS)  # milliseconds since last frame
    screen.fill((20, 20, 20))

    # ===== EVENTS =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ===== COMPUTE OUTPUTS =====
    motor_out = base_motors[:]
    pump_out = base_pumps[:]
    led1_out = base_leds1[:]
    led2_out = base_leds2[:]
    motor_weight = [1.0] * N_MOTORS
    pump_weight = [1.0] * N_MOTORS_PUMPS

    for layer in (l for l in layers if l.active(t)):
        if not layer.active(t):
            continue

        w = layer.weight(t)
        active_layers = []
        for layer in layers:
            if layer.active(t):
                active_layers += [layer]
        for i in range(N_MOTORS):
            current = None

            for layer in active_layers:
                if layer.motors[i] != -1:
                    w = layer.weight(t)
                    target = layer.motors[i] + layer.motion(i, t)
                    
                    if current is None:
                        current = target
                    else:
                        
                        # crossfade between layers
                        current = current * (1 - w) + target * w

            if current is not None:
                motor_out[i] = current

        for i in range(N_MOTORS_PUMPS):
            value = None
            total_weight = 0
            for layer in active_layers:
                if layer.pumps[i] != -1:
                    w = layer.weight(t)
                    value = layer.pumps[i] if value is None else value * (1 - w) + layer.pumps[i] * w
                    total_weight += w
            if value is not None:
                pump_out[i] = value
        for i in range(N_LEDS1):
            current = None

            for layer in led1_layers:
                if layer.leds[i] != -1 and layer.active(t):
                    w = layer.weight(t)
                    target = (int(layer.leds[i][0] + layer.led_motion(i, t)[0]), int(layer.leds[i][1] + layer.led_motion(i, t)[1]), int(layer.leds[i][2] + layer.led_motion(i, t)[2]))
                    if current is None:
                        current = (int(led1_out[i][0] * (1 - w) + target[0] * w), int(led1_out[i][1] * (1 - w) + target[1] * w), int(led1_out[i][2] * (1 - w) + target[2] * w))
                    else:
                        # crossfade between layers
                        current = (int(current[0] * (1 - w) + target[0] * w), int(current[1] * (1 - w) + target[1] * w), int(current[2] * (1 - w) + target[2] * w))
            if current is not None:
                led1_out[i] = current
        for i in range(N_LEDS2):
            current = None

            for layer in led2_layers:
                if layer.leds[i] != -1 and layer.active(t):
                    w = layer.weight(t)
                    target = (int(layer.leds[i][0] + layer.led_motion(i, t)[0]), int(layer.leds[i][1] + layer.led_motion(i, t)[1]), int(layer.leds[i][2] + layer.led_motion(i, t)[2]))
                    if current is None:
                        current = (int(led2_out[i][0] * (1 - w) + target[0] * w), int(led2_out[i][1] * (1 - w) + target[1] * w), int(led2_out[i][2] * (1 - w) + target[2] * w))
                    else:
                        # crossfade between layers
                        current = (int(current[0] * (1 - w) + target[0] * w), int(current[1] * (1 - w) + target[1] * w), int(current[2] * (1 - w) + target[2] * w))
            if current is not None:
                led2_out[i] = current
        


    # normalize
    for i in range(N_MOTORS):
        motor_out[i] /= motor_weight[i]

    for i in range(N_MOTORS_PUMPS):
        pump_out[i] /= pump_weight[i]

    for i in range(N_MOTORS):
        # ===== LAYOUT SETTINGS =====
        motor_height = 40
        motor_width = 20
        spacing = 110   # smaller gap between motors

        total_width = (N_MOTORS - 1) * spacing
        start_x = WIDTH // 2 - total_width // 2

        cx = start_x + i * spacing

        # Motor position (top of motor = pivot point)
        top_y = 450
        pivot_x = cx
        pivot_y = top_y

        # Motor angle
        angle_deg = motor_out[i]
        angle_rad = math.radians(angle_deg)

        # Pump power
        pump_power = pump_out[i] / 255.0

        # Skip beam if no power
        if pump_power <= 0.01:
            beam_length = 0
        else:
            beam_length = 50 + pump_power * (0.6 * HEIGHT)

        # Beam endpoint
        x2 = pivot_x + beam_length * math.cos(angle_rad)
        y2 = pivot_y - beam_length * math.sin(angle_rad)

        # ===== DRAW BEAM (blue) =====
        if pump_power > 0.01:
            pygame.draw.line(screen, (0, 180, 255), (pivot_x, pivot_y), (x2, y2), 6)
            pygame.draw.circle(screen, (0, 200, 255), (int(x2), int(y2)), 4)

        # ===== DRAW MOTOR (white, thicker) =====
        motor_rect = pygame.Rect(
            pivot_x - motor_width // 2,
            pivot_y,
            motor_width,
            motor_height
        )
        pygame.draw.rect(screen, (255, 255, 255), motor_rect)

        # Pivot point
        pygame.draw.circle(screen, (255, 255, 255), (pivot_x, pivot_y), 5)

    led1_y = 560
    led1_start_x = 100
    led1_end_x = screen.get_width() - led1_start_x
    led1_space =(led1_end_x - led1_start_x) / len(led1_out)
    count = 0
    for i in led1_out:
        
        pygame.draw.circle(screen, i, (count*led1_space + led1_start_x, led1_y), 10)

        count += 1

    led2_y = 540
    led2_start_x = 100
    led2_end_x = screen.get_width() - led2_start_x - 10
    led2_space =(led2_end_x - led2_start_x) / len(led2_out)
    count = 0
    for i in led2_out:
        
        pygame.draw.circle(screen, i, (count*led2_space + led2_start_x, led2_y), 5)

        count += 1
    
    # ===== UPDATE TIME =====
    t += dt

    pygame.display.flip()


pygame.quit()
