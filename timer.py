#!/usr/bin/env python3
# -*- coding: utf8 -*-

import eel
import sys


arg = sys.argv
if len(arg) >= 3:
    HOUR = arg[1]
    MINUTE = arg[2]
    SECOND = arg[3]
else:
    HOUR = 0
    MINUTE = 0
    SECOND = 0


@eel.expose
def timer(hour, minute, second):
    eel.update_time(f"{hour}:{minute}:{second}")
    if type(hour) != int:
        hour = int(hour)
    if type(minute) != int:
        minute = int(minute)
    if type(second) != int:
        second = int(second)
    while hour >= 0 and minute >= 0 and second >= 0:
        eel.sleep(1)
        if eel.reset_status()():
            break
        if eel.timer_status()() == "started":
            second -= 1
            if second < 0:
                minute -= 1
                second = 59
                if minute < 0:
                    hour -= 1
                    minute = 59
                    if hour < 0:
                        hour = 0
                        minute = 0
                        second = 0
                        eel.play_time_up_sound()
                        break
            eel.update_time(f"{hour}:{minute}:{second}")
    return


if __name__ == "__main__":
    eel.init("resource")
    eel.start(f"/html/timer.html?h={HOUR}&m={MINUTE}&s={SECOND}", port=0)
