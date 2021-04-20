#!/usr/bin/bash

# CONFIG
SAVE_DIR=$(xdg-user-dir PICTURES)
# END CONFIG

user_lang="${LANG:0:5}"

if [ "${user_lang,,}" = "pl_pl" ]; then
    lang_format="Format pliku"

    lang_scr_whole="Screenshot całego ekranu"
    lang_scr_fragment="Screenshot fragmentu ekranu"

    lang_delay="Opóźnienie:"
    lang_nodelay="Brak opóźnienia"

    lang_save_png="Zapisz jako png"
    lang_save_jpg="Zapisz jako jpg"
    lang_copy_clipboard="Skopiuj do schowka"

    lang_copied="Zapisano screenshot w schowku"
    lang_saved="Zapisano screenshot w pliku"
else
    lang_format="File format"

    lang_scr_whole="Screenshot of whole screen"
    lang_scr_fragment="Screenshot of selected region"

    lang_delay="Delay:"
    lang_nodelay="No delay"

    lang_save_png="Save as png"
    lang_save_jpg="Save as jpg"
    lang_copy_clipboard="Copy to clipboard"

    lang_copied="Screenshot copied to clipboard"
    lang_saved="Screenshot saved to file"
fi

lang_scr_whole="📷 $lang_scr_whole"
lang_scr_fragment="📷 $lang_scr_fragment"

lang_nodelay="🕰 $lang_nodelay"
lang_delay="⏰ $lang_delay"

lang_save_png="🖼️ $lang_save_png"
lang_save_jpg="🖼️ $lang_save_jpg"
lang_copy_clipboard="🖼️ $lang_copy_clipboard"

rofi_delay=$(
    echo -e "$lang_nodelay\n$lang_delay 1s\n$lang_delay 3s\n$lang_delay 5s\n$lang_delay 10s" |
    rofi -dmenu -p "screenshot" -lines 5
) || exit 2

rofi_save_method=$(
    echo -e "$lang_save_png\n$lang_save_jpg\n$lang_copy_clipboard" |
    rofi -dmenu -p "screenshot" -lines 3
) || exit 3

rofi_scr_type=$(
    echo -e "$lang_scr_whole\n$lang_scr_fragment" |
    rofi -dmenu -p "screenshot" -lines 2
) || exit 4

if [ "$rofi_scr_type" = "$lang_scr_fragment" ]; then
    screen_fragment=$(slop --highlight --tolerance=0 --color=0.3,0.4,0.6,0.4 -n -f '-g %g ')
fi

if [ "$rofi_delay" = "$lang_delay 1s" ]; then
    sleep 1
elif [ "$rofi_delay" = "$lang_delay 3s" ]; then
    sleep 3
elif [ "$rofi_delay" = "$lang_delay 5s" ]; then
    sleep 5
elif [ "$rofi_delay" = "$lang_delay 10s" ]; then
    sleep 10
fi

filename="Screenshot $(date '+%Y-%m-%d, %R:%S')"
filepath="$SAVE_DIR/$filename.png"
tempfilepath="/tmp/$filename.png"

if [ "$rofi_scr_type" = "$lang_scr_fragment" ]; then
    ffcast -q $screen_fragment png "$tempfilepath"
else
    ffcast -q png "$tempfilepath"
fi


if [ "$rofi_save_method" = "$lang_copy_clipboard" ]; then
    xclip -selection clipboard -t "image/png" "$tempfilepath"
    notify-send "$lang_copied"
elif [ "$rofi_save_method" = "$lang_save_jpg" ]; then
    convert "/tmp/$filename.png" "/tmp/$filename.jpg"
    mv "/tmp/$filename.jpg" "$SAVE_DIR"
    notify-send "$lang_saved" "$SAVE_DIR/$filename.jpg"
else
    mv "$tempfilepath" "$filepath"
    notify-send "$lang_saved" "$SAVE_DIR/$filename.png"
fi

rm "$tempfilepath"
