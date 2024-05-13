#!/usr/bin/env python3

import calendar
import random
import subprocess
import time
from datetime import datetime
from math import log10
from threading import Thread

from gpiozero import CPUTemperature
from sense_hat import SenseHat

REFRESH_TIME = 0.2
TEMP_FACTOR = 1.8

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
GRAY_DARK = (100, 100, 100)
RED = (255, 0, 0)
RED_LIGHT = (255, 60, 60)
BLUE = (0, 0, 255)
BLUE_LIGHT = (110, 110, 255)
GREEN = (0, 255, 0)
GREEN_LIGHT = (120, 255, 120)
ORANGE = (255, 145, 0)
ORANGE_LIGHT = (255, 160, 40)

JOYSTICK_ORIENTATION = {
    0: ("up", "down", "left", "right"),
    90: ("right", "left", "up", "down"),
    180: ("down", "up", "right", "left"),
    270: ("left", "right", "down", "up"),
}

LED_NUMBERS = (
    # 0
    (1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1),
    # 1
    (0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1),
    # 2
    (0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1),
    # 3
    (1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0),
    # 4
    (0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0),
    # 5
    (1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0),
    # 6
    (0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0),
    # 7
    (1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0),
    # 8
    (0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0),
    # 9
    (0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0),
    # Null
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
)


class VirtualAssistant:
    def __init__(self):
        self.rot = 0
        self.decibel = 0
        self.mode = "temperature"
        self.display = list()

    def auto_rotate_display(self):
        while True:
            x = round(sense.get_accelerometer_raw()["x"], 0)
            y = round(sense.get_accelerometer_raw()["y"], 0)

            self.rot = 0

            if x == -1:
                self.rot = 90

            elif y == -1:
                self.rot = 180

            elif x == 1:
                self.rot = 270

            sense.set_rotation(self.rot)

            time.sleep(REFRESH_TIME)

    def get_decibel(self):
        while True:
            try:
                soundmeter_output = subprocess.check_output(["soundmeter", "--collect", "--seconds", "0.5"]).decode(
                    "utf-8"
                )
                rms = int(soundmeter_output.strip().split(" ")[-1])
                self.decibel = round(20 * log10(rms))

            except:
                continue

    def run(self):
        rotate_thread = Thread(target=self.auto_rotate_display, daemon=True)
        rotate_thread.start()

        decibel_thread = Thread(target=self.get_decibel, daemon=True)
        decibel_thread.start()

        while True:
            if self.mode == "month":
                month = int(datetime.today().strftime("%m"))

                self.display.clear()

                if month >= 10:
                    for i in range(0, 32, 4):
                        self.display += [
                            WHITE if j == 1 else BLACK for j in LED_NUMBERS[int(str(month)[0])][i : i + 4]
                        ]
                        self.display += [GRAY if j == 1 else BLACK for j in LED_NUMBERS[int(str(month)[1])][i : i + 4]]

                elif month >= 1 and month <= 9:
                    for i in range(0, 32, 4):
                        self.display += [WHITE if j == 1 else BLACK for j in LED_NUMBERS[0][i : i + 4]]
                        self.display += [GRAY if j == 1 else BLACK for j in LED_NUMBERS[month][i : i + 4]]

                sense.low_light = True
                sense.set_pixels(self.display)

            elif self.mode == "date":
                date = int(datetime.today().strftime("%d"))

                self.display.clear()

                if date >= 10:
                    for i in range(0, 32, 4):
                        self.display += [WHITE if j == 1 else BLACK for j in LED_NUMBERS[int(str(date)[0])][i : i + 4]]
                        self.display += [GRAY if j == 1 else BLACK for j in LED_NUMBERS[int(str(date)[1])][i : i + 4]]

                elif date >= 1 and date <= 9:
                    for i in range(0, 32, 4):
                        self.display += [WHITE if j == 1 else BLACK for j in LED_NUMBERS[0][i : i + 4]]
                        self.display += [GRAY if j == 1 else BLACK for j in LED_NUMBERS[date][i : i + 4]]

                sense.low_light = True
                sense.set_pixels(self.display)

            elif self.mode == "calendar":
                year = int(datetime.today().strftime("%Y"))
                month = int(datetime.today().strftime("%m"))
                date = int(datetime.today().strftime("%d"))

                total_days = int(calendar.month(year, month).replace("\n", " ").split()[-1])

                weekdays = [
                    0 if datetime(year, month, 1).weekday() + 1 == 7 else datetime(year, month, 1).weekday() + 1
                ]

                for _ in range(total_days - 1):
                    weekdays.append(0 if weekdays[-1] + 1 == 7 else weekdays[-1] + 1)

                self.display.clear()

                self.display.append(BLUE_LIGHT)

                for _ in range(1, 6):
                    self.display.append(RED_LIGHT)

                self.display.append(BLUE_LIGHT)
                self.display.append(BLACK)

                for _ in range(weekdays[0]):
                    self.display.append(BLACK)

                for i, weekday in enumerate(weekdays, 1):
                    if i == date:
                        self.display.append(RED)

                    else:
                        if weekday == 0 or weekday == 6:
                            self.display.append(GRAY_DARK)

                        else:
                            self.display.append(WHITE)

                    if weekday == 6:
                        self.display.append(BLACK)

                for _ in range(64 - len(self.display)):
                    self.display.append(BLACK)

                sense.low_light = True
                sense.set_pixels(self.display)

            elif self.mode == "rainbow":
                self.display.clear()

                for _ in range(64):
                    self.display.append(random.sample(range(0, 255), 3))

                sense.low_light = False
                sense.set_pixels(self.display)

            elif self.mode == "temperature":
                sense_temp = (sense.get_temperature_from_humidity() + sense.get_temperature_from_pressure()) / 2
                cpu_temp = CPUTemperature().temperature
                temp = sense_temp - ((cpu_temp - sense_temp) / TEMP_FACTOR)
                temp_rounded = round(temp)

                self.display.clear()

                if temp_rounded >= 10:
                    for i in range(0, 32, 4):
                        self.display += [
                            RED if j == 1 else BLACK for j in LED_NUMBERS[int(str(temp_rounded)[0])][i : i + 4]
                        ]
                        self.display += [
                            RED_LIGHT if j == 1 else BLACK for j in LED_NUMBERS[int(str(temp_rounded)[1])][i : i + 4]
                        ]

                elif temp_rounded >= 0 and temp_rounded <= 9:
                    for i in range(0, 32, 4):
                        self.display += [BLACK for _ in LED_NUMBERS[-1][i : i + 4]]
                        self.display += [RED if j == 1 else BLACK for j in LED_NUMBERS[temp_rounded][i : i + 4]]

                # print(sense_temp, cpu_temp, temp)

                sense.low_light = True
                sense.set_pixels(self.display)

            elif self.mode == "humidity":
                humidity = sense.humidity
                humidity_rounded = round(humidity)

                self.display.clear()

                if humidity_rounded >= 10:
                    for i in range(0, 32, 4):
                        self.display += [
                            BLUE if j == 1 else BLACK for j in LED_NUMBERS[int(str(humidity_rounded)[0])][i : i + 4]
                        ]
                        self.display += [
                            BLUE_LIGHT if j == 1 else BLACK
                            for j in LED_NUMBERS[int(str(humidity_rounded)[1])][i : i + 4]
                        ]

                elif humidity_rounded >= 0 and humidity_rounded <= 9:
                    for i in range(0, 32, 4):
                        self.display += [BLACK for _ in LED_NUMBERS[-1][i : i + 4]]
                        self.display += [BLUE if j == 1 else BLACK for j in LED_NUMBERS[humidity_rounded][i : i + 4]]

                sense.low_light = True
                sense.set_pixels(self.display)

            elif self.mode == "decibel":
                self.display.clear()

                if self.decibel >= 10:
                    for i in range(0, 32, 4):
                        self.display += [
                            GREEN if j == 1 else BLACK for j in LED_NUMBERS[int(str(self.decibel)[0])][i : i + 4]
                        ]
                        self.display += [
                            GREEN_LIGHT if j == 1 else BLACK for j in LED_NUMBERS[int(str(self.decibel)[1])][i : i + 4]
                        ]

                elif self.decibel >= 0 and self.decibel <= 9:
                    for i in range(0, 32, 4):
                        self.display += [BLACK for _ in LED_NUMBERS[-1][i : i + 4]]
                        self.display += [GREEN if j == 1 else BLACK for j in LED_NUMBERS[self.decibel][i : i + 4]]

                sense.low_light = True
                sense.set_pixels(self.display)

            elif self.mode == "hour":
                hour = int(datetime.now().strftime("%H"))

                self.display.clear()

                if hour >= 10:
                    for i in range(0, 32, 4):
                        self.display += [
                            ORANGE if j == 1 else BLACK for j in LED_NUMBERS[int(str(hour)[0])][i : i + 4]
                        ]
                        self.display += [
                            ORANGE_LIGHT if j == 1 else BLACK for j in LED_NUMBERS[int(str(hour)[1])][i : i + 4]
                        ]

                elif hour >= 0 and hour <= 9:
                    for i in range(0, 32, 4):
                        self.display += [ORANGE if j == 1 else BLACK for j in LED_NUMBERS[0][i : i + 4]]
                        self.display += [ORANGE_LIGHT if j == 1 else BLACK for j in LED_NUMBERS[hour][i : i + 4]]

                sense.low_light = True
                sense.set_pixels(self.display)

            elif self.mode == "minute":
                minute = int(datetime.now().strftime("%M"))

                self.display.clear()

                if minute >= 10:
                    for i in range(0, 32, 4):
                        self.display += [
                            ORANGE if j == 1 else BLACK for j in LED_NUMBERS[int(str(minute)[0])][i : i + 4]
                        ]
                        self.display += [
                            ORANGE_LIGHT if j == 1 else BLACK for j in LED_NUMBERS[int(str(minute)[1])][i : i + 4]
                        ]

                elif minute >= 0 and minute <= 9:
                    for i in range(0, 32, 4):
                        self.display += [ORANGE if j == 1 else BLACK for j in LED_NUMBERS[0][i : i + 4]]
                        self.display += [ORANGE_LIGHT if j == 1 else BLACK for j in LED_NUMBERS[minute][i : i + 4]]

                sense.low_light = True
                sense.set_pixels(self.display)

            elif self.mode == "second":
                second = int(datetime.now().strftime("%S"))

                self.display.clear()

                if second >= 10:
                    for i in range(0, 32, 4):
                        self.display += [
                            ORANGE if j == 1 else BLACK for j in LED_NUMBERS[int(str(second)[0])][i : i + 4]
                        ]
                        self.display += [
                            ORANGE_LIGHT if j == 1 else BLACK for j in LED_NUMBERS[int(str(second)[1])][i : i + 4]
                        ]

                elif second >= 0 and second <= 9:
                    for i in range(0, 32, 4):
                        self.display += [ORANGE if j == 1 else BLACK for j in LED_NUMBERS[0][i : i + 4]]
                        self.display += [ORANGE_LIGHT if j == 1 else BLACK for j in LED_NUMBERS[second][i : i + 4]]

                sense.low_light = True
                sense.set_pixels(self.display)

            time.sleep(REFRESH_TIME)


if __name__ == "__main__":
    sense = SenseHat()
    sense.clear()

    asst = VirtualAssistant()

    asst_thread = Thread(target=asst.run, daemon=True)
    asst_thread.start()

    event_old, event_new = None, None

    while True:
        for event in sense.stick.get_events():
            event_old, event_new = event_new, (event.direction, event.action)

            if event_new[1] == "released" and event_old[1] != "released":
                # up
                if event_old[0] == JOYSTICK_ORIENTATION[asst.rot][0]:
                    if event_old[1] == "pressed":
                        if asst.mode != "month":
                            asst.mode = "month"

                        else:
                            asst.mode = "date"

                    else:
                        asst.mode = "calendar"

                # down
                elif event_old[0] == JOYSTICK_ORIENTATION[asst.rot][1]:
                    if event_old[1] == "pressed":
                        if asst.mode != "flashlight":
                            asst.mode = "flashlight"

                            sense.clear()
                            sense.low_light = False
                            sense.clear(WHITE)

                        else:
                            asst.mode = "flashlight_dim"

                            sense.clear()
                            sense.low_light = True
                            sense.clear(WHITE)

                    else:
                        asst.mode = "rainbow"

                # left
                elif event_old[0] == JOYSTICK_ORIENTATION[asst.rot][2]:
                    if event_old[1] == "pressed":
                        if asst.mode != "temperature":
                            asst.mode = "temperature"

                        else:
                            asst.mode = "humidity"

                    else:
                        asst.mode = "decibel"

                # right
                elif event_old[0] == JOYSTICK_ORIENTATION[asst.rot][3]:
                    if event_old[1] == "pressed":
                        if asst.mode != "hour":
                            asst.mode = "hour"

                        else:
                            asst.mode = "minute"

                    else:
                        asst.mode = "second"

                # middle
                else:
                    if event_old[1] == "pressed":
                        asst.mode = "sleep"

                        sense.clear()

                    else:
                        pass
