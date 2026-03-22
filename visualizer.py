import pygame
import math
from pydub import AudioSegment
import pygame

# ===== CONFIG =====
WIDTH, HEIGHT = 800, 600
FPS = 60
BPM = 138.0
N_MOTORS = 3
N_PUMPS = 3


# angular frequency (rad/s)
omega = 2 * math.pi * BPM / 60.0


# ===== FUNCTIONS =====
def tconv(x):
    x = int(x)

    minutes = x // 100000
    seconds = (x // 1000) % 100
    millis  = x % 1000

    return minutes * 60000 + seconds * 1000 + millis
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


def shift_layers(layers, offset):
    new_layers = []
    for layer in layers:
        new_layers.append(
            l(
                layer.start + offset,
                layer.end + offset,
                layer.fade_in,
                layer.fade_out,
                layer.motors,
                layer.pumps,
                layer.motion
            )
        )
    return new_layers

def shift_start(layers, offset):
    new_layers = []
    for layer in layers:
        new_layers.append(
            l(
                layer.start + offset,
                layer.end,
                layer.fade_in,
                layer.fade_out,
                layer.motors,
                layer.pumps,
                layer.motion
            )
        )
    return new_layers



def shift_end(layers, offset):
    new_layers = []
    for layer in layers:
        new_layers.append(
            l(
                layer.start,
                layer.end + offset,
                layer.fade_in,
                layer.fade_out,
                layer.motors,
                layer.pumps,
                layer.motion
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

# ===== LAYERS =====
layers = []
Layers = [
    l(
        start=700, end=12170,
        fade_in=1000, fade_out=1000,
        motors=[90,90,90],
        pumps=[0, 0, 0],
        motion=sin2
    ),
]
temp0 = [
    l(0, 200, 0, 0, [-1, -1, -1], [100, 100, 100], n),
    l(430, 650, 0, 0, [-1, -1, -1], [100, 100, 100], n),
    l(860, 1060, 0, 0, [-1, -1, -1], [100, 100, 100], n),
    l(1300, 1400, 0, 0, [-1, -1, -1], [100, 100, 100], n),
    l(1510, 1630, 0, 0, [-1, -1, -1], [100, 100, 100], n),
    l(1950, 2390, 0 ,0, [-1, -1, -1], [100, 0, 0], n),
    l(2390, 2600, 0, 0, [-1, -1, -1], [0, 100, 0], n),
    l(2600, 2820, 0, 0, [-1, -1, -1], [0, 0, 100], n),
    l(3040, 3260, 0, 0, [-1, -1, -1], [100, 100, 100], n),
]
for i in range(4):
    layers += shift_layers(temp0, i * 3440 + 700)


temp1= [
    l(12800, 17300, 0, 0, [-1, -1, -1], [0, 0, 0], n),
    l(12801, 17300, 900, 0, [-1, -1, -1], [200, 200, 200], n),
    l(13600, 17360, 0, 0, [90, 90, 90], [200, 200, 200], n),
    l(13601, 17360, 850, 0, [80, 80, 80], [200, 200, 200], n),
    l(13890, 17360, 850, 0, [100, 100, 100], [200, 200, 200], n),
    l(14740, 17360, 890, 0, [80, 80, 80], [200, 200, 200], n),
    l(15630, 17360, 860, 0, [100, 100, 100], [200, 200, 200], n),
    l(16500, 17360, 860, 0, [80, 80, 80], [200, 200, 200], n),
    l(17360, 20830, 860, 0, [80, 80, 80], [200, 200, 200], n),
    l(17361, 20830, 850, 0, [90, 90, 90], [150, 150, 150], sin3),
    l(18000, 20830, 240, 0, [80, 90, 100], [130, 150, 130], n),
    l(18800, 20830, 130, 0, [100, 90, 80], [150, 200, 150], n),
    l(19540, 20830, 500, 0, [90, 90, 90], [100, 100, 100], sin3),
    l(20200, 20830, 629, 0, [80, 80, 80], [200, 200, 200], n),
    l(20830, 27819, 0, 0, [80, 80, 80], [200, 200, 200], n),
    l(20831, 27819, 860, 0, [100, 100, 100], [200, 200, 200], n),
    l(21690, 27819, 860, 0, [80, 80, 80], [200, 200, 200], n),
    l(22550, 27819, 860, 0, [100, 100, 100], [200, 200, 200], n),
    l(23410, 27819, 860, 0, [100, 90, 80], [150, 200, 150], n),
    l(24680, 27819, 500, 0, [90, 100, 110], [200, 180, 160], n),
    l(25500, 27819, 500, 0, [70, 80, 90], [160, 180, 200], n),
    l(26500, 27819, 1000, 0, [90, 90, 90], [100, 100, 100], sin3),
    l(26500, 27819, 1270, 0, [-1, -1, -1], [0, 0, 0], n),
]

layers += shift_layers(temp1, 750)
#31300
temp2 = [
    l(27821, 31299, 0, 0, [-1, -1, -1], [0, 0, 0], n),
    l(27822, 31299, 1715, 0, [-1, -1, -1], [230, 230, 230], n),
    l(29540, 31299, 1720, 0, [-1, -1, -1], [50, 50, 50], n),
    l(31300, 34779, 0, 0, [-1, -1, -1], [50, 50, 50], n),
    l(31301, 34779, 1715, 0, [-1, -1, -1], [230, 230, 230], n),
    l(33060, 34779, 1709, 0, [-1, -1, -1], [50, 50, 50], n)
]
layers += shift_layers(temp2, 750)

temp3 = [
    l(27820, 34770, 0, 0, [80, 80, 80], [-1, -1, -1], n),
    l(27821, 34770, (34770 - 27820) / 16 - 1, 0, [100, 100, 100], [-1, -1, -1], n),
    l(28250, 34770, (34770 - 27820) / 16 - 1, 0, [80, 80, 80], [-1, -1, -1], n)
]

for i in range(16):
    layers += shift_start(shift_layers(temp3, 750), i * ((34770 - 27820) / 8))

temp4 = [
    l(34780, 40870, 0, 0, [-1, -1, -1], [0, 0, 0], n),
    l(34781, 40870, 1710, 0, [-1, -1, -1], [230, 230, 230], n),
    l(36500, 40870, 1710, 0, [-1, -1, -1], [100, 100, 100], n),
    l(36500, 40870, 1710, 0, [-1, -1, -1], [230, 230, 230], n),
    l(38240, 40870, 1710, 0, [-1, -1, -1], [100, 100, 100], n),
    l(34780, 40870, 0, 0, [70, 80, 90], [-1, -1, -1], n),
    l(34781, 40870, 859, 0, [90, 100, 110], [-1, -1, -1], n),
    l(35641, 40870, 858, 0, [90, 80, 70], [-1, -1, -1], n),
    l(36500, 40870, 859, 0, [110, 100, 90], [-1, -1, -1], n),
    l(37360, 40870, 859, 0, [80, 80, 80], [-1, -1, -1], n),
    l(38260, 40870, 859, 0, [90, 90, 90], [-1, -1, -1], sin5),
    l(40000, 40870, 870, 0, [90, 90, 90], [100, 100, 100], n),
]
layers += shift_layers(temp4, 750)
temp5 = [
    l(40870, 41720, 0, 0, [90, 90, 90], [100, 100, 100], n),
    l(40871, 41720, 420, 0, [100, 100, 100], [150, 150, 150], n),
    l(41295, 41720, 420, 0, [80, 80, 80], [200, 200, 200], n),
    l(41720, 43459, 0, 0, [80, 80, 80], [200, 200, 200], n),
    l(41721, 43459, 850, 0, [100, -1, -1], [-1, -1, -1], n),
    l(42160, 43459, 850, 0, [-1, 110, -1], [-1, -1, -1], n),
    l(42590, 43459, 850, 0, [-1, -1, 120], [-1, -1, -1], n),
    l(43460, 48669, 0, 0, [100, 110, 120], [200, 200, 200], n),
    l(43461, 48669, 850, 0, [60, 70, 80], [200, 200, 200], n),
    l(44320, 48669, 850, 0, [90, 90, 90], [-1, -1, -1], n),
    l(45200, 48669, 500, 0, [90, 90, 90], [100, 100, 100], sin4),
    l(45570, 48669, 500, 0, [100, 90, 80], [180, 180, 180], n),
    l(46220, 48669, 500, 0, [80, 90, 100], [200, 200, 200], n),
    l(46660, 48669, 500, 0, [90, 90, 90], [100, 100, 100], sin1),
    l(48268, 48669, 200, 0, [70, 70, 70], [50, 50, 50], n),
]
layers += shift_layers(temp5, 750)

temp6 = [
    l(48670, 55629, 0, 0, [70, 70, 70], [50, 50, 50], n),
    l(48671, 55629, 1710, 0, [110, 110, 110], [200, 200, 200], n),
    l(50430, 55629, 850, 0, [80, 80, 80], [150, 150, 150], n),
    l(51290, 55629, 850, 0, [100, 90, 80], [100, 200, 100], n),
    l(51291, 55629, 700, 0, [-1, 90, -1], [-1, -1, -1], sin4),
    l(53460, 55629, 640, 0, [80, 80, 80], [200, 200, 200], n),
    l(54100, 55629, 700, 0, [80, 80, 80], [-1, -1, -1], sin4),
    l(54770, 55629, 640, 0, [100, 100, 100], [200, 200, 200], n),
    l(55630, 109100, 0, 0, [100, 100, 100], [200, 200, 200], n),
    l(55631, 109100, 860, 0, [80, 80, 80], [230, 230, 230], n),
    l(56500, 109100, 860, 0, [100, 100, 100], [230, 230, 230], n),
    l(57370, 109100, 640, 0, [80, -1, -1], [-1, -1, -1], n),
    l(57800, 109100, 860, 0, [-1, 80, -1], [-1, -1, -1], n),
    l(58240, 109100, 860, 0, [-1, -1, 80], [-1, -1, -1], n),
    l(59110, 109100, 430, 0, [90, 90, 90], [-1, -1, -1], sin6),
    l(59110, 109100, 860, 0, [-1, -1, -1], [130, 180, 230], n), 
    l(59980, 109100, 860, 0, [90, 100, 110], [230, 180, 130], n),
    l(100860, 109100, 430, 0, [90, 90, 90], [100, 100, 100], sin5),
    l(102580, 109100, 1720, 0, [90, 90, 90], [240, 240, 240], n),
    l(104320, 109100, 1720, 0, [-1, -1, -1], [50, 50, 50], n),
    l(104330, 109100, 430, 0, [85, 85, 85], [-1, -1, -1], n),
    l(104760, 109100, 430, 0, [95, 95, 95], [-1, -1, -1], n),
    l(105200, 109100, 430, 0, [85, 85, 85], [-1, -1, -1], n),
    l(105630, 109100, 430, 0, [100, 100, 100], [-1, -1, -1], n),
    l(106070, 109100, 0, 0, [-1, -1, -1], [200, 200, 200], n),
    l(106071, 109100, 1270, 0, [-1, -1, -1], [50, 50, 50], n),
    l(106060, 109100, 1270, 0, [80, 80, 80], [-1, -1, -1], n),
    l(107370, 109100, 0, 0, [-1, -1, -1], [235, 235, 235], n),
    l(107371, 109100, 1000, 0, [-1, -1, -1], [0, 0, 0], n),
    l(107370, 109100, 1000, 0, [90, 90, 90], [-1, -1, -1], n),
    l(109110, 137350, 0, 0, [90, 90, 90], [0, 0, 0], n),
    l(109111, 137350, 430, 0, [85, 85, 85], [255, 255, 255], n),
    l(109540, 137350, 860, 0, [95, 95, 95], [-1, -1, -1], n),
    l(110410, 137350, 860, 0, [85, 85, 85], [-1, -1, -1], n),
    l(111290, 137350, 860, 0, [-1, -1, 95], [-1, -1, -1], n),
    l(111720, 137350, 860, 0, [-1, 95, -1], [-1, -1, -1], n),
    l(112150, 137350, 860, 0, [95, -1, -1], [-1, -1, -1], n),
    l(113020, 137350, 860, 0, [85, 85, 85], [-1, -1, -1], n),
    l(113890, 137350, 860, 0, [95, 95, 95], [-1, -1, -1], n),
    l(114760, 137350, 860, 0, [85, -1, -1], [-1, -1, -1], n),
    l(115190, 137350, 860, 0, [-1, 85, -1], [-1, -1, -1], n),
    l(115630, 137350, 860, 0, [-1, -1, 85], [-1, -1, -1], n),
    
]

layers += shift_layers(temp6, 750)








base_motors = [90] * N_MOTORS
base_pumps = [0] * N_PUMPS

t = 68000

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

    motor_weight = [1.0] * N_MOTORS
    pump_weight = [1.0] * N_PUMPS

    for layer in layers:
        if not layer.active(t):
            continue

        w = layer.weight(t)

        for i in range(N_MOTORS):

            current = None

            for layer in layers:
                if layer.active(t) and layer.motors[i] != -1:
                    w = layer.weight(t)
                    target = layer.motors[i] + layer.motion(i, t)

                    if current is None:
                        current = target
                    else:
                        # crossfade between layers
                        current = current * (1 - w) + target * w

            if current is not None:
                motor_out[i] = current

        for i in range(N_PUMPS):
            value = None
            total_weight = 0
            for layer in layers:
                if not layer.active(t):
                    continue
                if layer.pumps[i] != -1:
                    w = layer.weight(t)
                    value = layer.pumps[i] if value is None else value * (1 - w) + layer.pumps[i] * w
                    total_weight += w
            if value is not None:
                pump_out[i] = value

    # normalize
    for i in range(N_MOTORS):
        motor_out[i] /= motor_weight[i]

    for i in range(N_PUMPS):
        pump_out[i] /= pump_weight[i]

    # ===== DRAW MOTORS (top row) =====
    # ===== DRAW MOTORS + WATER BEAMS =====
    # ===== DRAW MOTORS + WATER BEAMS =====
    for i in range(N_MOTORS):

        cx = 150 + i * 250

        motor_height = 40
        motor_width = 20

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

            # tip
            pygame.draw.circle(screen, (0, 200, 255), (int(x2), int(y2)), 4)

        # ===== DRAW MOTOR (white, thicker) =====
        motor_rect = pygame.Rect(
            pivot_x - motor_width // 2,
            pivot_y,
            motor_width,
            motor_height
        )

        pygame.draw.rect(screen, (255, 255, 255), motor_rect)

        # Optional: draw pivot point
        pygame.draw.circle(screen, (255, 255, 255), (pivot_x, pivot_y), 5)

    # ===== UPDATE TIME =====
    t += dt

    pygame.display.flip()


pygame.quit()
