#/usr/bin/env bash

if [ $(cat /proc/net/wireless | wc -l) = '2' ]; then
    echo ", %"
    exit
fi

interface=$( tail -1 /proc/net/wireless | awk '{print $1}' | sed 's/://g' )
quality=$( tail -1 /proc/net/wireless | awk '{print $3}' | sed 's/\.//g')
quality_percentage=$(awk "BEGIN {print int($quality/70 * 100)}")

ip=$(ip -f inet addr show wlp2s0 | grep -Po 'inet \K[\d.]+')

echo "$ip, $quality_percentage%"
