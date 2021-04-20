# Tworzenie wirtualnego środowiska
$ pip install virtualenv 
$ source virtualenv

getattr(my_function, "__name__")



# Listy (obiekty klasy list)
Listy w porównaniu do krotek są mutable, mają metody append i tak dalej

lista = list()
lista = [10, 50, 80, "360"]

Listy można tworzyć z krotek (i innych kolekcji)
lista = list((10, 20, 30))

# Sety - obiekty klasy set i frozenset

Set jest mutable, frozenset jest immutable

Mimo że dodaję 10 dwa razy, w obiekcie będzie tylko raz
my_set = set()
my_set.add(10)
my_set.add(10)

Sety można tworzyć skróconą składnią
my_set = {10, 20, 30}

Albo można je tworzyć z innych struktur danych
my_set = set((10, 20, 30))

# Słowniki - obiekty klasy dictionary

Słowniki można robić na dużo sposobów różnych
a = dict(A = 1, Z=-1)
a = {'A': 1, 'Z': -1}

Pobranie danego elementu slownika
slownik['A']

# Ogólne operacje na kolekcjach
Dla kolekcji mutable, można w taki sposób usuwać elementy:
del kolekcja[3:6]

any

# Słownik z wartością domyślną - obiekty klasy defaultdict
from collections import defaultdict
dd = defaultdict(int)

Działa jak zwykły słownik, ale jeśli użyjesz nieistniejącej wartości, to zostanie ona utworzona,
a jako jej wartość zostanie ustawiona wartość funkcji int(), czyli zero
Można też własną funkcję tam dać

# Krotki z nazwami - obiekty klasy namedtuple
from collections import namedtuple
WadaWzroku = namedtuple("WadaWzroku", ("lewe_oko", "prawe_oko"))
WadaWzroku = namedtuple("WadaWzroku", "lewe_oko prawe_oko") //dzięki automatycznemu zamienianiu stringow na kolekcje
rogowski = WadaWzroku(10, 20)

# Obiekt Chainmap - szybkie łączenie dużych Słowników
from collections import ChainMap
my_chainmap = ChainMap(jeden_slownik, drugi_slownik, trzeci_slownik)
my_chainmap["klucz"] - spróbuje odnaleźć wartość w jednym z 3 słowników

# Przedziały - obiekty klasy range

Tworzy przedział liczb od 1 do 100, przy czym 100 już nie należy do przedziału, ale jedynka należy
range(1, 100)

Tworzy krotkę na podstawie tego przedziału
my_tuple = tuple(range(1,100))

W przedziałach również działa notacja start,stop,step
range(1,100,2) //co druga liczba od 1 do 100

# Instrukcje warunkowe
if zmienna == 20:
    zrob_cos_fajnego()
elif zmienna == 30:
    zrob_cos_superanckiego()
else:
    zrob_cos_glupiego()

prezydentura = True if wiek >= 35 else False

# Pętle
Iterowanie po elementach kolekcji
for number in [0, 1, 2, 3, 4]:
    print(number)
for number in range(1,5): //wyświetli cyfry 1-4
    print(number)

Iterowanie po elementach kolekcji, ale z pobieraniem pozycji
for position, surname in enumerate(["Rogalski", "Rogowski", "Rogowiecki"]):
    print(position, surname)

Enumrate może przyjmować pozycję startową - od niej będą iterowane elementy

Pętla while
while i < 6:
    do_something()

W Python działa continue oraz break

Pętla for-else i while-else
Blok else jest wykonywany, jeśli pętla NIE ZAKOŃCZY SIĘ użyciem BREAK
people = [('James', 17), ('Kirk', 9), ('Lars', 13)]
for person, age in people:
    if age >= 18:
        driver = (person, age)
        break
else:
    raise Exception("Driver not found")

# Zip - połączenie dwóch kolekcji w zespół krotek
imiona = ("Daniel", "Stanisław", "Anna")
nazwiska = ("Rogowski", "Łożyca", "Kowalska")
zipped = zip(imiona, nazwiska) #można też zipować więcej niż 2 kolekcje

for imie, nazwisko in zipped:
    print(imie, nazwisko) # Wyświetli Daniel Rogowski itd.

for data in zipped:
    imie, nazwisko = data #odpakowanie krotki
    print(imie, nazwisko)


# Moduł itertools

//Count - nieskończone iterowanie (chyba że dasz break)
from itertools import count
for n in count(5, 3): //zaczynając od 5, weź co 3 liczbę
    if n > 20:
        break
    print(n) // wyświetli liczby 5, 8, 11, 14, 17, 20'

//Compress - kompresuje dwie kolekcje, biorąc elementy z pierwszej kolekcji tylko tam, gdzie element z drugiej kolekcji jest równy 1
compress('ABCDEF', [1,0,1,0,1,1])
//czyli zwróci ACEF

// Generatory kombinacji, umożliwiają pobranie wszystkich możliwych ustawień elementów danej kolekcji
literki = ('A', 'B', 'C')
permutacja = permutations(literki)
print(list(permutacja))
//Wyświetli wszystkie możliwe ustawienia kolejności elementów, których jest 3!, czyli 6

# Funkcje
def funkcja():
    do_something()

Funkcje zagnieżdżone
def funkcja():
    def funkcja2():
        do_something()
    funkcja2()

Zaimportowanie zmiennej globalnej
zmienna_globalna = 3
def funkcja():
    zmienna_globalna = 4 //normalnie taki zapis stworzyłby nową zmienną i zaciemnił nazwę zmiennej globalnej
    //aby przeciwdziałać takiemu zachowaniu, należy dodać klauzulę global

zmienna_globalna = 4
def funkcja():
    global zmienna_globalna
    zmienna_globalna = 5 //teraz naprawdę będziemy edytować zmienną globalną

Edytowanie zmiennej z nadrzędnego zasięgu
def funkcja():
    zmienna_lokalna = 30
    def funkcja2():
        nonlocal zmienna_lokalna
        zmienna_lokalna = 30 # dzięki słówku nonlocal, będę edytował zmienną, zamiast tworzyć nową

Funkcja przyjmująca parametry
def funkcja(x, y, z = 20): 
    print("Funkcja z 1 argumentem domyślnym")

funkcja(10, 20, 30)
funkcja(x=10, z=20, y=40)

Funkcja przyjmująca zmienną liczbę argumentów:
def funkcja(*args):
Można ją wywołać przez funkcja(10), funkcja(10, 10, 20) itd.
args będzie typu tuple

Odpakowywanie krotek:
def print_all(*args):
    print(*args) # tu występuje odpakowanie
print_all(10, 20, 30, 40)
Operator gwiazdki odpakowuje krotkę, czyli do metody print nie zostanie wysłany jeden obiekt krotki, tylko 4 pojedyncze obiekty

Puste kolekcje są interpretowane jako False, więc żeby sprawdzić czy są jakiekolwiek argumenty, można napisać
if args:
    do_sth()

Jeszcze inny przykład użycia odpakowania krotek:
krotka = (10, 20, 30, 100)
print(*krotka) //wyświetli "10 20 30 100" zamiast "(10, 20, 30, 100)"

Zmienna liczba argumentów, ale opakowująca słownik, nie krotkę
def funkcja(**kwargs):
    print(kwargs["password"])

Przykład użycia powyższej funkcji:
funkcja(login="Hello", password="World")

W przypadku takich funkcji też działa odpakowywane, ale trzeba użyć operatora **
funkcja(**{"login": "Hello", "password": "World"})

# Funkcje anonimowe (lambdy)
printer = lambda x, y: print("I'm printing a message", x, y)
printer("hello", "world")

[FUNKCJA FILTER]
Praktyczny przykład użycia, wyświetlenie liczb spełniających warunek, żeby być większymi od 18
data = range(5, 55, 5)
checker = lambda x: x > 18
filtered_data = filter(checker, data)
print(*filtered_data)

[INNY PRZYKŁAD UŻYCIA - FUNKCJA MAP]
Funkcja map wywołuje przekazaną funkcję na wszystkich elementach kolekcji
data = [10, 20, 30, 40, 50]
data_2 = map(lambda x: x+5, data)
print(*data_2) //wyświetli 15 25 35 45 55

# Sortowanie kolekcji
nowa_kolekcja = sorted(stara_kolekcja)
stara_kolekcja.sort() //działa tylko na kolekcje mutable

nowa_kolekcja = sorted(stara_kolekcja, reverse=True) //odwróć kolejność sortowania
nowa_kolekcja = sorted(stara_kolekcja, key = lamda item: item.pole) //każdy element kolekcji zostanie poddany funkcji key i dopiero wartość zwrócona przez tę funkcję będzie brana do sortowania


# Reduce - wykonaj po kolei funkcję na każdym elemencie tablicy
from functools import reduce
def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value

Przykład użycia
from operator import mul # Mul to funkcja mnożąca dwie liczby
def factorial(n):
    return reduce(mul, range(1, n + 1))

# Autodokumentacja klasy lub funkcji
def my_function():
    """Dokumentacja zamknięta w trzech cudzysłowach"""
    pass
można ją pobrać poprzez
my_function.__doc__
lub getattr(my_function, "__doc__")

# Pakiety, moduły, importowanie

Pojęcia:
pakiet - folder
moduł - plik z rozszerzeniem py

Aby folder był pakietem, musi zawierać plik (chociażby pusty) o nazwie __init__.py

Mamy przykładowe drzewo plików:
|
| - plik: run.py
| - folder: test_package
| - - - - plik: test.py
| - - - - plik: __init__.py

Plik test.py zawiera taki oto kod:
def test_function()
    print("Test text")


Możliwe kombinacje pliku run.py:

import test_package.test
test_package.test.test_function()

from test_package.test import test_function
test_function()

from test_package import test
test.test_function()

# List comprehensions - skrótowy zapis listy

Generalny szablon list comprehenson:
[wyrażenie_zwracane for nazwa_na_element_kolekcji in kolekcja if warunek_na_elemencie_kolekcji]

Znalezienie kwadratów liczb parzystych z przedziału 1 - 100
squares = [number ** 2 for number in range(1, 101) if number % 2 == 0]

Inny przykład, oprócz samych wyników wyświetla jeszcze dane (zwraca krotkę dana - wynik)
squares = [(number, number**2) for number in range(1, 101) if number % 2 == 0]
for square in squares:
    print(square[0], square[1])

List comprehensions użyte jako filter
movies = [("Film 1", 2002), ("Film 2", 2000)] //lista filmów, każdy film to osobna krotka z tytułem i datą wydania
movies_old = [title for title, year in movies if year <= 2000] //lista filmów, które wyszły przed 2000

Zadnieżdżone List comprehension
tabliczka = ["{} * {} = {}".format(x, y, x * y) for x in range(1,11) for y in range(1,11)]
for dzialanie in tabliczka:
    print(dzialanie)

# Dict comprehensions

d = {
    "sposób_generowania_klucza": sposób_generowania_wartości
    for wartość1, wartość2 in kolekcja
    if warunek_filtrujący_element_kolekcji
}

# Set comprehensions - tez istnieje, taka sama skladnia jak w list comprehension, ale uzywa {} zamiast []

# Yield - działa identycznie jak w C#
Yield zwraca obiekt klasy generator, który jest iteratorem
def counter():
    number = 0
    while True:
        number += 5
        yield number

for position, surname in enumerate(counter()):
    print(position, number)
    if position == 100:
        break

Istnieje też yield from JAKIŚ_ITERATOR, które od razu yielduje kilka liczb z danego, innego iteratora, na przykład
Funkcja zwracająca kwadraty liczb z podanego przedziału, korzystając z generator expression
def get_squares(start, end):
    yield from (n ** 2 for n in rage(start, end))

# Generator expression, jak list comprehension, ale ma nawias okrągłe

my_list = [n ** 2 for n in range(1, 100)]
my_gen_expr = (n ** 2 for n i in range(1, 100))
sum(my_list) # wolniejsze, bo iterujemy dwa razy (raz tworzenie listy, drugi raz sumowanie)
sum(my_gen_expr) # szybsze, bo tylko 1 iteracja

Generator expression dziala tylko przy pierwszej iteracji, przy następnych już nie da się z niego wyciągnąć żadnych danych

# Dekorator funkcji - wzorzec projektowy

Niniejszy przykład pozwala obliczyć czas wykonania dowolnej funkcji
from time import time
from functools import wraps

def measure(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time()
        result = func(*args, **kwargs)
        print("Wykonanie funkcji", func.__name__, "zajęło", time() - t)
        return result
    return wrapper

def cube(n):
    return n ** 3

Dekorowanie funkcji cube funkcją measure
cube = measure(cube)

cube(100)

UWAGA!
Zamiast pisać cube = measure(cube)
Powinno się po prostu napisać
@measure
def cube(n):
    return n**3
Takie zapisy są równoznaczne

# Decorator factory

Dekorator (funkcja dekorująca) może przyjmować wyłącznie inną funkcję
Aby mieć dekorator, który przyjmuje też inne argumenty, należy zrobić funkcję tworzącą dekorator

def decorator_factory(argument):
    def decorator(func_to_call):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func_to_call(*args, **kwargs)
            do_sth()
            return result
    return decorator

@dekorator_factory(20)
def funkcja_dekorowana():
    pass

# Klasy
class NewClass:
    def funkcja(): # funkcja tak jakby statyczna
        pass
    def metoda(self) # metody przyjmują 1 argument self
        pass

dir(obiekt)  # pokaż atrybuty obiektu

Aby oznaczyć metodę jako jednoznacznie statyczną, należy ją opatrzyć dekoratorem @staticmethod
@staticmethod
def metoda():
    pass

Są jeszcze metody @classmethod, które jako pierwszy argument zawsze przyjmują obiekt klasy (cls)
Poniżej najprostszy przykad wzorca Factory
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @classmethod
    def from_tuple(cls, arg_tuple): # cls to to samo co Point
        return cls(*arg_tuple)
Ogólnie rzecz biorąc, w kodzie nigdy nie powinno się używać nazwy klasy (Point)
Należy używać albo @classmethod i cls, albo self.__class__

NewClass.pole = 20 # pole tak jakby statyczne
obiekt = NewClass()
obiekt.pole # pole będące własnością obiektu

W Pythonie nie ma konstruktora, jest za to inicjalizator
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
p1 = Point(10, 2)
print(p1.y)

Dziedziczenie
class ThreeDimentionalPoint(Point):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z
p2 = ThreeDimentionalPoint(10, 2, 30)
print(p2.y, p2.z)

Dziedziczenie działa tak, że jeżeli w klasie-dziecku nie można znaleźć jakiegoś elementu,
to Python zacznie po kolei we wszystkich rodzicach szukać, zgodnie z kolejnością MRO - MethodResolutionOrder
dowolny_obiekt.__class__.mro()

Dziedziczyć można po więcej niż 1 klasie

# Name mangling
Jeżeli w klasie, w dowolnej metodzie, zamieścimy deklarację
self._pole = 30
To pole zostanie oznaczone jako prywatne
(Dalej można je edytować, to tylko kwestia przyjętej konwencji)

Jeżeli w klasie, w dowolnej funkcji, zamieścimy deklarację
self.__pole = 30
To stworzymy pole, które będzie dedykowane danej klasie - dzieci nie będą miały do niej dostępu
Tak naprawdę to pole będzie się nazywało self._NAZWAKLASY__nazwapola
Ten mechanizm nazywamy name manglingiem

Jeśli podkreślnik jest na końcu, to oznacza to, że dany obiekt próbuje obejść nazwę istniejącego keyworda
na przykład nazwa zmiennej def_ zamiast def, bo def to reserved keywoard

# Property decorator
class Person:
    def __init__(self, age):
        self.age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if 18 <= value <= 120:
            self._age = value
        else:
            raise ValueError("Age must be within <18; 120>")

p1 = Person(18)
p2 = Person(13)  # spowoduje wyjątek, bo setter uniemożliwia ustawienie wartości mniejszych niż 18

# Iteratory - przykładowy iterator, który iteruje się wyłącznie po parzystych elementach wskazanej  kolekcji

class EvenIterator:
    def __init__(self, iterable):
        self._iterable = iterable
        self._indexes = [num for num in range(0, len(iterable), 2)]

    def __iter__(self):
        return self

    def __next__(self):
        if self._indexes:
            return self._iterable[self._indexes.pop(0)]
        else:
            raise StopIteration


x = EvenIterator("abcdefghijklmnop")
print(*x)  # operator odpakowania - gwiazdka

# Wyjątki

BaseException - klasa bazowa dla wszystkich wyjątków (w tym np wyjątek wciśnięcia Ctrl+C)
Exception - klasa bazowa dla wszystkich wyjątków tworzonych przez użytownika

raise Exception()  # rzucenie wyjątkiem

class MyException(Exception):
    pass

try:
    # rzeczy do wykonania w bloku try
except (ValueError, TypeError) as e:
    # rzeczy do wykonania jak wyjątek nastąpi
else:
    # rzeczy do wykonania jak wyjątek nie nastąpi
finally:
    # rzeczy do wykonania jak wyjątek wystąpi lub nie wystąpi


# Skryptowanie
if __name__ == "__main__":
    pass
If wykona się tylko, jeżeli moduł właczono z poziomu konsoli (a nie na przykład zaimportowano)

UNION, type hinting w funkcjach

klauzula with

Biblioteka pickle, json, html, beautifoulsoup