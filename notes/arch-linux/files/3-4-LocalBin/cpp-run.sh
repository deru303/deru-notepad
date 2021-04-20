#!/bin/sh

if [ -f "main.cpp" ]; then
    g++ main.cpp -o main.bin
    chmod a+x main.bin
    ./main.bin
    echo ""
else
    echo "Błąd, nie znaleziono programu do uruchomienia."
    echo "Uruchom ten skrypt w folderze, w którym znajduje się plik main.cpp!"
fi
