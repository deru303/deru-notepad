#!/bin/sh

# Konfiguracja skryptu
LOCATION="Cekcyn" # miejsce pobierania pogody
TEMP_FORMAT="%t"  # format temperatury
STRIP_PLUS=true   # czy usuwać znak + z wartości zwróconej przez wttr.in?
EXPIRY_SECS=900   # liczba sekund ważności pobranej pogody
CACHE_FILE="$HOME/.cache/status-weather.cache"

download_weather () {
    weather=$(curl -s "http://wttr.in/$LOCATION?format=$FORMAT")
    
    if [ $STRIP_PLUS = true ]; then
        weather=$(echo "$weather" | sed "s/+//")
    fi

    echo "$weather" > "$CACHE_FILE"
}

if [ -f "$CACHE_FILE" ]; then
    curtime=$(date +%s)
    filetime=$(stat "$CACHE_FILE" -c %Y)
    timediff=$(expr $curtime - $filetime)
    if [ $timediff -gt $EXPIRY_SECS ]; then
        download_weather
    elif ! grep -q '[^[:space:]]' "$CACHE_FILE"; then
        download_weather
    fi
else
    download_weather
fi

cat "$CACHE_FILE"

