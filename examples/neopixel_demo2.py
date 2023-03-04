#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

# Portions of this script were adapted from:
#  https://github.com/pimoroni/unicorn-hat/blob/master/examples/demo.py

import math
import time
import colorsys

from luma.led_matrix.device import neopixel, ws2812
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, TINY_FONT, LCD_FONT

# create matrix device
#device = neopixel(width=8, height=4)

MY_MATRIX_22x20 = [
  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22,
 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65,
 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66,
 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,100,101,102,103,104,105,106,107,108,109,
131,130,129,128,127,126,125,124,123,122,121,120,119,118,117,116,115,114,113,112,111,110,
132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,
175,174,173,172,171,170,169,168,167,166,165,164,163,162,161,160,159,158,157,156,155,154,
176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,
219,218,217,216,215,214,213,212,211,210,209,208,207,206,205,204,203,202,201,200,199,198,
220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,
263,262,261,260,259,258,257,256,255,254,253,252,251,250,249,248,247,246,245,244,243,242,
264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,
307,306,305,304,303,302,301,300,299,298,297,296,295,294,293,292,291,290,289,288,287,286,
308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,
351,350,349,348,347,346,345,344,343,342,341,340,339,338,337,336,335,334,333,332,331,330,
352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,
395,394,393,392,391,390,389,388,387,386,385,384,383,382,381,380,379,378,377,376,375,374,
396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,
439,438,437,436,435,434,433,432,431,430,429,428,427,426,425,424,423,422,421,420,419,418,
]

device = ws2812(width=22, height=20, mapping=MY_MATRIX_22x20)
device.contrast(5)


# twisty swirly goodness
def swirl(x, y, step):
    x -= (device.width / 2)
    y -= (device.height / 2)

    dist = math.sqrt(pow(x, 2) + pow(y, 2)) / 2.0
    angle = (step / 10.0) + (dist * 1.5)
    s = math.sin(angle)
    c = math.cos(angle)

    xs = x * c - y * s
    ys = x * s + y * c

    r = abs(xs + ys)
    r = r * 64.0
    r -= 20

    return (r, r + (s * 130), r + (c * 130))


# roto-zooming checker board
def checker(x, y, step):
    x -= (device.width / 2)
    y -= (device.height / 2)

    angle = (step / 10.0)
    s = math.sin(angle)
    c = math.cos(angle)

    xs = x * c - y * s
    ys = x * s + y * c

    xs -= math.sin(step / 200.0) * 40.0
    ys -= math.cos(step / 200.0) * 40.0

    scale = step % 20
    scale /= 20
    scale = (math.sin(step / 50.0) / 8.0) + 0.25

    xs *= scale
    ys *= scale

    xo = abs(xs) - int(abs(xs))
    yo = abs(ys) - int(abs(ys))
    l = 0 if (math.floor(xs) + math.floor(ys)) % 2 else 1 if xo > .1 and yo > .1 else .5

    r, g, b = colorsys.hsv_to_rgb((step % 255) / 255.0, 1, l)

    return (r * 255, g * 255, b * 255)


# weeee waaaah
def blues_and_twos(x, y, step):
    x -= (device.width / 2)
    y -= (device.height / 2)

#    xs = (math.sin((x + step) / 10.0) / 2.0) + 1.0
#    ys = (math.cos((y + step) / 10.0) / 2.0) + 1.0

    scale = math.sin(step / 6.0) / 1.5
    r = math.sin((x * scale) / 1.0) + math.cos((y * scale) / 1.0)
    b = math.sin(x * scale / 2.0) + math.cos(y * scale / 2.0)
    g = r - .8
    g = 0 if g < 0 else g

    b -= r
    b /= 1.4

    return (r * 255, (b + g) * 255, g * 255)


# rainbow search spotlights
def rainbow_search(x, y, step):
    xs = math.sin((step) / 100.0) * 20.0
    ys = math.cos((step) / 100.0) * 20.0

    scale = ((math.sin(step / 60.0) + 1.0) / 5.0) + 0.2
    r = math.sin((x + xs) * scale) + math.cos((y + xs) * scale)
    g = math.sin((x + xs) * scale) + math.cos((y + ys) * scale)
    b = math.sin((x + ys) * scale) + math.cos((y + ys) * scale)

    return (r * 255, g * 255, b * 255)


# zoom tunnel
def tunnel(x, y, step):

    speed = step / 100.0
    x -= (device.width / 2)
    y -= (device.height / 2)

    xo = math.sin(step / 27.0) * 2
    yo = math.cos(step / 18.0) * 2

    x += xo
    y += yo

    if y == 0:
        if x < 0:
            angle = -(math.pi / 2)
        else:
            angle = (math.pi / 2)
    else:
        angle = math.atan(x / y)

    if y > 0:
        angle += math.pi

    angle /= 2 * math.pi  # convert angle to 0...1 range

    shade = math.sqrt(math.pow(x, 2) + math.pow(y, 2)) / 2.1
    shade = 1 if shade > 1 else shade

    angle += speed
    depth = speed + (math.sqrt(math.pow(x, 2) + math.pow(y, 2)) / 10)

    col1 = colorsys.hsv_to_rgb((step % 255) / 255.0, 1, .8)
    col2 = colorsys.hsv_to_rgb((step % 255) / 255.0, 1, .3)

    col = col1 if int(abs(angle * 6.0)) % 2 == 0 else col2

    td = .3 if int(abs(depth * 3.0)) % 2 == 0 else 0

    col = (col[0] + td, col[1] + td, col[2] + td)

    col = (col[0] * shade, col[1] * shade, col[2] * shade)

    return (col[0] * 255, col[1] * 255, col[2] * 255)


def gfx(device):
    effects = [tunnel, rainbow_search, checker, swirl]

    step = 0
    while True:
        for i in range(500):
            with canvas(device) as draw:
                for y in range(device.height):
                    for x in range(device.width):
                        r, g, b = effects[0](x, y, step)
                        if i > 400:
                            r2, g2, b2 = effects[-1](x, y, step)

                            ratio = (500.00 - i) / 100.0
                            r = r * ratio + r2 * (1.0 - ratio)
                            g = g * ratio + g2 * (1.0 - ratio)
                            b = b * ratio + b2 * (1.0 - ratio)
                        r = int(max(0, min(255, r)))
                        g = int(max(0, min(255, g)))
                        b = int(max(0, min(255, b)))
                        draw.point((x, y), (r, g, b))

            step += 1

            time.sleep(0.01)

        effect = effects.pop()
        effects.insert(0, effect)


def main():
#    msg = "Neopixel WS2812 LED Matrix Demo"
#    show_message(device, msg, y_offset=-1, fill="green", font=proportional(TINY_FONT))
    msg = "*** RasQberry & Quantum Computing  ***"
    show_message(device, msg, y_offset=12, fill="blue", font=proportional(LCD_FONT), scroll_delay=0.15)
    time.sleep(3)

    with canvas(device) as draw:
        text(draw, (0, -1), txt="A", fill="red", font=TINY_FONT)
        text(draw, (4, -1), txt="T", fill="green", font=TINY_FONT)

    time.sleep(3)

    with canvas(device) as draw:
        draw.line((0, 0, 0, device.height), fill="red")
        draw.line((1, 0, 1, device.height), fill="orange")
        draw.line((2, 0, 2, device.height), fill="yellow")
        draw.line((3, 0, 3, device.height), fill="green")
        draw.line((4, 0, 4, device.height), fill="blue")
        draw.line((5, 0, 5, device.height), fill="indigo")
        draw.line((6, 0, 6, device.height), fill="violet")
        draw.line((7, 0, 7, device.height), fill="white")

    time.sleep(4)

    for _ in range(5):
        for intensity in range(16):
            device.contrast(intensity * 16)
            time.sleep(0.1)

    device.contrast(0x80)
    time.sleep(1)

    gfx(device)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
