xrdb -merge $HOME/.config/X11/.Xresources

xinput set-prop "ELAN0501:00 04F3:3010 Touchpad" "libinput Tapping Enabled" 1
xinput set-prop "ELAN0501:00 04F3:3010 Touchpad" "libinput Disable While Typing Enabled" 0
xinput set-prop "ELAN0501:00 04F3:3010 Touchpad" "libinput Natural Scrolling Enabled" 1

setxkbmap pl
setxkbmap -option caps:escape

xwallpaper --stretch /usr/share/wallpapers/wallpaper.png
start-pulseaudio-x11

compton -b -f &
dwmblocks &
xss-lock -- slock &

/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &

exec dwm 
