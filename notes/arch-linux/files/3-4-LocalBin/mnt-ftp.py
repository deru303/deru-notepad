#!/usr/bin/env python3
import os
import sys


class Color:
   BOLD = '\033[1m'
   END = '\033[0m'


def get_executable_name():
    return os.path.basename(sys.argv[0])


def print_actions():
    print(f"{Color.BOLD}Uruchom skrypt z argumentem, aby wykonać akcję:\n")
    print(f"Zamontuj katalog FTP:{Color.END}")
    print(f"{get_executable_name()} mount")
    print(f"{get_executable_name()} mount /mnt/ftp ftp.example.com ssl_unrestricted username password\n")
    print(f"{Color.BOLD}Odmontuj katalog FTP:{Color.END}")
    print(f"{get_executable_name()} umount{Color.END}")
    print(f"{get_executable_name()} umount /mnt/path-to-dir{Color.END}")


def mount_action():
    if len(sys.argv) >= 7:
        mount_path, mount_host, mount_ssl, mount_username, mount_password = sys.argv[2:7]
    elif len(sys.argv) >= 6:
        mount_path, mount_host, mount_ssl, mount_username = sys.argv[2:6]
        mount_password = None
    elif len(sys.argv) >= 5:
        mount_path, mount_host, mount_ssl = sys.argv[2:5]
        mount_username, mount_password = (None, ) * 2
    elif len(sys.argv) >= 4:
        mount_path, mount_host = sys.argv[2:4]
        mount_username, mount_password, mount_ssl = (None, ) * 3
    elif len(sys.argv) >= 3:
        mount_path = sys.argv[2]
        mount_username, mount_password, mount_ssl, mount_host = (None, ) * 4
    else:
        mount_path, mount_username, mount_password, mount_ssl, mount_host = (None, ) * 5

    if mount_path is None:
        print(f"{Color.BOLD}Podaj ścieżkę do istniejącego folderu, w którym chcesz zamontować katalog FTP.{Color.END}")
        mount_path = input("mount_path: "); print()

    if not os.path.isdir(mount_path):
        print(f"{Color.BOLD}Wskazana przez ciebie ścieżka nie jest istniejącym folderem!{Color.END}")
        print("Przerywam...")
        exit(1)
    
    mount_path = os.path.abspath(mount_path)

    if mount_host is None:
        print(f"{Color.BOLD}Podaj adres hosta, pod którym znajduje się twój serwer FTP.{Color.END}")
        mount_host = input("mount_host: "); print()

    if mount_ssl is None:
        print(f"{Color.BOLD}Wybierz rodzaj szyfrowania SSL, którego chcesz używać do połączenia się:{Color.END}")
        print("ssl - normalne szyfrowanie TLS/SSL")
        print("ssl_unrestricted - użyj tej opcji, jeżeli serwer posługuje się niezaufanym certyfikatem self-signed")
        print("no_ssl - brak szyfrowania SSL")
        mount_ssl = input("mount_ssl: "); print()

    mount_ssl = mount_ssl.lower()
    if mount_ssl not in ("ssl", "no_ssl", "ssl_unrestricted"):
        print(f"{Color.BOLD}Wskazana przez ciebie metoda szyfrowania nie istnieje!{Color.END}")
        print("Przerywam...")
        exit(1)

    if mount_username is None:
        print(f"{Color.BOLD}Podaj nazwę użytkownika FTP. Wpisz anonymous, jeśli chcesz zalogować się anonimowo.{Color.END}")
        mount_username = input("mount_username: "); print()

    if mount_password is None:
        print(f"{Color.BOLD}Podaj hasło użytkownika FTP.{Color.END}")
        mount_password = input("mount_password: "); print()

    if mount_ssl == "ssl":
        ssl_args = "ssl,tlsv1,ssl_control,"
    elif mount_ssl == "ssl_unrestricted":
        ssl_args = "ssl,tlsv1,ssl_control,no_verify_hostname,no_verify_peer,"
    else: 
        ssl_args = ""
    
    command = f'curlftpfs "{mount_host}" "{mount_path}" -o {ssl_args}user={mount_username}:{mount_password}'
    print(f"{Color.BOLD}Wywołuję komendę:\n{Color.END}{command}")
    os.system(command)


def umount_action():
    if len(sys.argv) > 2:
        umount_path = sys.argv[2]
    else:
        print(f"{Color.BOLD}Wprowadź ścieżkę do katalogu FTP, który chcesz odmontować!{Color.END}")
        umount_path = input("umount_path: ")
        print()
    command=f"fusermount -u '{umount_path}'"
    print(f"{Color.BOLD}Wywołuję komendę:\n{Color.END}{command}\n")
    exit_code = os.system(command)
    if exit_code == 0:
        print("Polecenie wykonano pomyślnie.")


def main():
    if len(sys.argv) == 1:
        print_actions()
    elif sys.argv[1] == "mount":
        mount_action()
    elif sys.argv[1] == "umount":
        umount_action()
    else:
        print(f"{Color.BOLD}Nierozpoznana akcja!")
        print(f"{Color.END}Wywołaj skrypt bez argumentów, by wyświetlić listę akcji.")


if __name__ == "__main__":
    os.system("modprobe fuse")
    main()
    
