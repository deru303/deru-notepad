#!/bin/bash

USER_LANG="${LANG:0:5}"

if [ "${USER_LANG,,}" = "pl_pl" ]; then
    PC_SHUTDOWN="Wyłącz komputer"
    PC_REBOOT="Uruchom ponownie"
    PC_LOGOUT="Wyloguj mnie"
    PC_LOCK="Zablokuj komputer"
    NOTIFICATION_NAME="Menedżer zasilania"
    NOTIFICATION="Wysłano dyspozycję wyłączenia zasilania. Komputer powinien za chwilę się wyłączyć."
else
    PC_SHUTDOWN="Shutdown"
    PC_REBOOT="Reboot"
    PC_LOGOUT="Log out"
    PC_LOCK="Lock"
    NOTIFICATION_NAME="Power manager"
    NOTIFICATION="A power off request has been sent. The computer should shut down in a moment."
fi

# Icons
PC_SHUTDOWN="🚪 $PC_SHUTDOWN"
PC_REBOOT="🔃 $PC_REBOOT"
PC_LOGOUT="👥 $PC_LOGOUT"
PC_LOCK="🔒 $PC_LOCK"

selected=$(
    echo -e "$PC_SHUTDOWN\n$PC_REBOOT\n$PC_LOGOUT\n$PC_LOCK" | 
    rofi -dmenu -p "powermenu" -lines 4
)

case $selected in
    "$PC_SHUTDOWN")
        notify-send "$NOTIFICATION_NAME" "$NOTIFICATION"
        sudo shutdown -h now
        ;;

    "$PC_REBOOT")
        notify-send "$NOTIFICATION_NAME" "$NOTIFICATION"
        sudo reboot
        ;;

    "$PC_LOGOUT")
        i3-msg exit || killall dwm
        ;;

    "$PC_LOCK")
        light-locker-command --lock
        ;;
esac
