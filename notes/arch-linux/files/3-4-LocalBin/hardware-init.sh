#!/bin/sh

xinput set-prop "ELAN0501:00 04F3:3010 Touchpad" "libinput Tapping Enabled" 1
xinput set-prop "ELAN0501:00 04F3:3010 Touchpad" "libinput Disable While Typing Enabled" 0
xinput set-prop "ELAN0501:00 04F3:3010 Touchpad" "libinput Natural Scrolling Enabled" 1

setxkbmap pl
