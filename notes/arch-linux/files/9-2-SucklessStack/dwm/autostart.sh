#!/bin/sh
compton -b -f &
light-locker &
dwmblocks &

/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
