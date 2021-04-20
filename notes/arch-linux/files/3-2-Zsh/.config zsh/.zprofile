xdg-user-dirs-update

XINIT_LOGFILE="$HOME/.cache/xinit.log"
[[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]] && exec startx "$HOME/.config/X11/.xinitrc" > "$XINIT_LOGFILE" 2>&1
