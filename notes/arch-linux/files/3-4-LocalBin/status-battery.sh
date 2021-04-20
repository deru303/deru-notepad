#!/bin/bash
BATTERY="/sys/class/power_supply/BAT1"

PERCENTAGE=`cat $BATTERY/capacity`
STATUS=`cat $BATTERY/status`

if [ $STATUS = "Charging" ]; then
    SYMBOL=""
elif [ $STATUS = "Discharging" ]; then
    SYMBOL=""
elif [ $STATUS = "Full" ]; then
    SYMBOL=""
elif [ $STATUS = "Unknown" ]; then
    SYMBOL=""
fi

echo "$SYMBOL $PERCENTAGE%"