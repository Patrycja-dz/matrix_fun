import random
import sys
import time

width = 65
height = 45
decay = 26

buffer = bytearray(width * height * decay)

droplets = []

def iterate():
    global droplets
    for  vertical_index in range(height):
        for horizontal_index in range(width):
            value = buffer[vertical_index * width +horizontal_index]
            value -= decay
            if value < 0:
                value = 0
            buffer[horizontal_index + vertical_index * width] = value

    while len(droplets) < int(width * 1.5):
        droplet = [
            random.randint(0, width - 1),
            0,
            1 + random.random() * 1.5,
        ]
        droplets.append(droplet)

    new_droplets = []
    for droplet in droplets:
        x, y, speed = droplet
        next_y = y + speed

        skip_droplet = False
        for i in range(int(y), int(next_y) + 1):
            if i >= height:
                skip_droplet = True
                break
            buffer[x + i * width] = 255

        if not skip_droplet:
            droplet[1] = next_y
            new_droplets.append(droplet)

    droplets = new_droplets




chars = [chr(x) for x in range(0x30a1, 0x30fb)]

def draw():
    o = ["\x1b[2J\x1b[1;1H"]

    for vertical_index in range(height):
        for horizontal_index in range(width):
            value = buffer[vertical_index * width + horizontal_index]

            if value >= 128:
                r = (value - 128) * 2
                g = 255
                b = (value - 128) * 2
            else:
                r = 0
                g = value * 2
                b = 0

            ch = chars[(horizontal_index * 15267 + vertical_index * 91267) % len(chars)]
            o.append(f"\x1b[38;2;{r};{g};{b}m{ch}\x1b[m")

        o.append('\n')

    sys.stdout.write("".join(o))
    sys.stdout.flush()

while True:
    iterate()
    draw()
    time.sleep(0.1)