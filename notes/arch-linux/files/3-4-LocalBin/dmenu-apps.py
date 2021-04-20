#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE, STDOUT

# Ścieżki do katalogów, w których skrypt będzie szukał plików .desktop z aplikacjami
application_directories = [
    "/usr/share/applications",
    os.path.join(os.environ["HOME"], ".local/share/applications")
]

# Ścieżka do pliku, w którym skrypt będzie przechowywał informacje o częstotliwości używania aplikacji
usage_file = os.path.join(os.environ["HOME"], ".cache/dmenu-usage-cache.txt")

# Słownik przechowujący dane aplikacji w formacie "nazwa-pliku.desktop" => obiekt DesktopFile
desktop_files = dict()

# Pobiera język użytkownika w dwóch wersjach - krótkiej, np. pl oraz długiej, np. pl_PL
# Jeżeli nie uda się ustalić języka, jako oba języki zostanie przyjęta wartość "DEFAULT_LANG" 
language_long = os.environ.get("LANG", "DEFAULT_LANG").split(".")[0]
language_short = os.environ.get("LANG", "DEFAULT_LANG").split("_")[0]

# Środowisko graficzne, które ma uruchomione użytkownik
session = os.environ["DESKTOP_SESSION"] or os.environ["XDG_SESSION_DESKTOP"] or os.environ["XDG_CURRENT_DESKTOP"] or "unrecognized"
session = session.lower()

# Klasa reprezentująca plik .desktop z danymi na temat jakiejś aplikacji
class DesktopFile:
    def __init__(self):
        self.names = dict()
        self.generic_names = dict()
        self.categories = list()
        self.hidden = False
        self.only_show_in = list()

    def __str__(self):
        app_name = \
            self.names.get(language_short) or \
            self.names.get(language_long) or \
            self.names.get("DEFAULT_LANG") or \
            self.generic_names.get(language_short) or \
            self.generic_names.get(language_long) or\
            self.generic_names.get("DEFAULT_LANG")
        return "🔵 " + app_name
        

# Wczytanie wszystkich odnalezionych plików .desktop do słownika desktop_files
for dir in application_directories:
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)

        # Nie przetwarzaj pliku, jeśli nie ma rozszerzenia .desktop
        if not file.endswith(".desktop"):
            continue

        # Jeżeli już wcześniej napotkałeś plik o takiej samej nazwie,
        # zamiast tworzyć nowy obiekt DesktopFile zmodyfikuj poprzednij.
        if desktop_files.get(file) is None:
            current_app = DesktopFile()
            desktop_files[file] = current_app
        else:
            current_app = desktop_files[file]

        # Otwórz plik .desktop i czytaj go linijka po linijce
        with open(file_path, "r") as f:
            for line in f:

                # Jeśli napotkano na sekcję akcji (np. akcja otwarcia karty incognito w przypadku Firefoxa),
                # zakończ analizowanie tego pliku desktop
                if "[Desktop Action" in line:
                    break

                # Wczytaj klucz i wartość danej linijki (key-value pair)
                # oraz przejdź do następnej linijki, jeśli bieżąca nie zawiera klucza i wartości
                kv_pair = line.split("=", 1)
                if len(kv_pair) <= 1:
                    continue
                kv_pair[1] = kv_pair[1].replace("\n", "")

                # Aplikację uznajemy za ukrytą, jeśli ma ustawione Hidden lub NoDisplay na True
                if kv_pair[0] == "Hidden" or kv_pair[0] == "NoDisplay":
                    current_app.hidden = bool(kv_pair[1])
                    continue

                # Wczytanie środowisk graficznych, w których ma być wyświetlana aplikacja
                if kv_pair[0].startswith("OnlyShowIn"):
                    current_app.only_show_in = kv_pair[1].split(";")
                    continue

                # Wczytanie kategorii aplikacji
                if kv_pair[0].startswith("Categories"):
                    current_app.categories = kv_pair[1].split(";")
                    continue
                
                # Jeżeli dany klucz ma zastrzeżenie językowe (np. GenericName[pl]), pobierz kod tego języka.
                # Jeżeli go nie ma, jako kod języka przyjmij "DEFAULT_LANG".
                if "[" not in kv_pair[0]:
                    lang = "DEFAULT_LANG"
                else:
                    lang = kv_pair[0][kv_pair[0].find("[")+1:kv_pair[0].find("]")]
                
                # Wczytanie pozycji Name i GenericName
                if kv_pair[0].startswith("Name"):
                    current_app.names[lang] = kv_pair[1]
                elif kv_pair[0].startswith("GenericName"):
                    current_app.generic_names[lang] = kv_pair[1]

# Na podstawie słownika generuje listę nieukrytych aplikacji do wyświetlenia w formacie 
# ("nazwapliku.desktop", "czytelna nazwa aplikacji do wyświetlenia użytkownikowi")
# Aplikacje, które nie zgadzają się z klauzulą OnlyShowIn pliku .desktop są pomijane
display_list = []
for app_filename, app_obj in desktop_files.items():
    if len(app_obj.only_show_in) != 0 and session not in app_obj.only_show_in:
        continue

    if not app_obj.hidden:
        display_list.append((app_filename, str(app_obj)))

# Odczytuje plik usage_file, zapisując częstotliwość ilość do usage_dict
# w formacie "nazwapliku.desktop" => ilość_użyć
usage_dict = dict() 
with open(usage_file, "r") as f:
    for line in f:
        line_entries = line.split(" ")
        if len(line_entries) != 2:
            continue
        elif int(line_entries[1] == 0):
            continue
        else:
            usage_dict[line_entries[0]] = int(line_entries[1])

# Aplikacje bez wpisów nt. częstotliwości użytkowania (będą sortowane alfabetycznie)
apps_without_entry = [
    (display_tuple[0], display_tuple[1])
    for display_tuple
    in display_list
    if display_tuple[0] not in usage_dict.keys()
]

# Aplikacje z wpisami nt. częstotliwości użytkowania (bęzą sortowane wg tej częstotliwości)
apps_with_entry = [
    (display_tuple[0], display_tuple[1])
    for display_tuple
    in display_list
    if display_tuple[0] in usage_dict.keys()
]

# Sortowanie obu powyższych list
apps_without_entry.sort(key=lambda el: el[1])
apps_with_entry.sort(key=lambda el: usage_dict[el[0]], reverse=True)

# Połączenie posortowanych list jako nowa, posortowana lista display_list
display_list = apps_with_entry + apps_without_entry

# Przekazuje nazwy aplikacji na standardowe wyjście dmenu
dmenu_process = Popen(['/usr/bin/env', 'dmenu', '-i'], stdin=PIPE, stdout=PIPE)    
for application_filename, application in display_list:
    dmenu_process.stdin.write(application.encode("UTF-8"))
    dmenu_process.stdin.write("\n".encode("UTF-8"))
dmenu_process.stdin.close()
dmenu_process.wait()

# Kończy działanie skryptu, jeśli użytkownik nie wybrał żadnej opcji
if dmenu_process.returncode != 0:
    exit(dmenu_process.returncode)

# Pobiera opcję wybraną przez użytkownika
chosen_app = dmenu_process.stdout.readline().decode("UTF-8").replace("\n", "")
if not chosen_app:
    exit(1)

# Pobiera nazwę pliku .desktop przypisanego do aplikacji wybranej przez użytkownika
chosen_app_filename = None
for app_filename, app_displayname in display_list:
    if chosen_app == app_displayname:
        chosen_app_filename = app_filename
        break
if chosen_app_filename is None:
    exit(1)

# Zapisuje opcję wybraną przez użytkownika w usage_dict i zapisuje usage_dict do usage_file
if usage_dict.get(chosen_app_filename) is not None:
    usage_dict[chosen_app_filename] += 1
else:
    usage_dict[chosen_app_filename] = 1

with open(usage_file, "w") as f:
    for app_filename, app_usagecount in usage_dict.items():
        f.write("{} {}\n".format(app_filename, app_usagecount))

# Uruchamia aplikację wybraną przez użytkownika
os.system('/usr/bin/gtk-launch "{}"'.format(chosen_app_filename))
