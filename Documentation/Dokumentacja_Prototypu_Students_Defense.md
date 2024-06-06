### Dokumentacja Prototypu Gry Tower Defense

#### 1. Instrukcja Uruchomienia Prototypu

##### 1.1 Wymagane Biblioteki
Aby uruchomić prototyp, należy zainstalować poniższe biblioteki:
- `pygame`
- `os`

Komenda instalacji:
```bash
pip install pygame
```

##### 1.2 Uruchomienie Prototypu
Uruchom główny skrypt gry, wpisując w terminalu:
```bash
python main.py
```
lub
```bash
python <nazwa_skryptu>.py
```
(Jeśli nazwa głównego skryptu jest inna).

##### UWAGA
Na systemie Windows, jeśli skala ekranu jest ustawiona na większą niż 100% może nie być widać całego okna gry

#### 2. Instrukcja Użytkowania

##### 2.1 Klasa `Level`
- **Metody:**
  - `__init__(self, level_number : int, level_data_directory : str = None)`: Inicjalizuje poziom o podanym numerze.
  - `new_wave(self)`: Dodaje falę przeciwników.
  - `spawn_enemy(self)`: Pojawia przeciwników na mapie.
  - `update(self)`: Zajmuję się pojawianiem i poruszaniem przeciwników po mapie co klaktę.

##### 2.2 Klasa `Map`
- **Metody:**
  - `__init__(self, name: str = "TEST_1", map_data_directory: str = None)`: Inicjalizuje mapę na podstawie pliku danych mapy.
  - `load_map_data(self, path: str)`: Ładuje dane mapy z pliku.

##### 2.3 Klasa `Tower`
- **Metody:**
  - `__init__(self, tower_type : str = "test_tower")`: Inicjalizuje wieżę z podanymi parametrami.
  - `cooldown(self)`: Zajmuję się czasem odnowienia ataku wieży.
  - `setbasecooldown(self)`: Ustawia bazowy czas odnowienia.

##### 2.4 Klasa `Tower_Manager`
- **Metody:**
  - `__init__(self, tower_type_str : str = "test_tower", pos : Coord = Coord(0, 0))`: Inicjalizuje menedżera wież dla podanego typu wieży i współrzędnych.
  - `reset(cls)`: Resetuje listę wież.
  - `attack(self)`: Wykonuje atak wieży na wrogów w zasięgu.
  - `update(cls)`: atakuje przeciwników w zasięgu co klatkę.

##### 2.5 Klasa `Enemy`
- **Metody:**
  - `__init__(self, enemy_type : str = 'test_enemy')`: Inicjalizuje przeciwnika z zadaną prędkością i zdrowiem.
  - `__str__(self)`: Zwraca napis ze wcześniej zadanymi statystykami.

##### 2.6 Klasa `Enemy_Manager`
- **Metody:**
  - `__init__(self,enemy_type : str = 'test_enemy', map : Map = Map())`: Inicjalizuje menedżera przeciwników dla danej mapy.
  - `__repr__(self)`: Zwraca napis z typem, zdrowiem i pozycją przeciwnika.
  - `take_damage(self, damage)`: Zajmuje się wszystkim związanym z otrzymywaniem przez przeciwników obrażeń.
  - `movement(self)`: Definiuje jak przeciwnicy poruszają się przez mapę.
  - `remove_enemy(self)`: Usuwa pokonanych przeciwników.

##### 2.7 Klasa `Player`
- **Metody:**
  - `__init__(self, name : str, gold : int, lives : int, avtw : list[str])`: Inicjalizuje gracza.
  - `affordable_towers(self)`: Sprawdza, na które wieże stać gracza.
  - `deduct_lives(self)`: Odejmuje życia gracza

#### 3. Planowany Diagram Klas UML

Diagram klas przedstawia zależności pomiędzy klasami oraz ich atrybuty i metody:

```plaintext
+----------------+         +--------------+
|    Level       |<>-------|    Enemy     |
+----------------+         +--------------+
| - level_number |         | - name       |
| - enemy_waves  |         | - health     |
+----------------+         +--------------+
| + add_wave()   |
| + get_waves()  |
| + start_level()|
+----------------+

+----------------+         +--------------+
|    Map         |<>-------|    Coord     |
+----------------+         +--------------+
| - name         |         | - x          |
| - paths        |         | - y          |
| - grid         |         +--------------+
+----------------+
| + load_map_data|
+----------------+

+----------------+         +--------------+
|    Tower       |<>-------| Tower_Manager|
+----------------+         +--------------+
| - range        |         | - towers     |
| - damage       |         +--------------+
| - atk_speed    |
| - shot_count   |
| - targeting    |
| - bouncing     |
| - own_asset    |
| - shot_asset   |
+----------------+

+----------------+
| Tower_Manager  |
+----------------+
| - towers       |
+----------------+
| + reset()      |
| + attack()     |
+----------------+
```

#### 4. Zaktualizowany Plan Działania na Kolejne Tygodnie Pracy



#### 5. Zaktualizowany Plan Funkcjonalności Gotowej Aplikacji

- **Podstawowe Funkcje:**
  - Dodawanie fal przeciwników.
  - Zarządzanie wieżami i atakowanie przeciwników.
  - Ładowanie i wyświetlanie map.

- **Zaawansowane Funkcje:**
  - Różnorodne typy wież i przeciwników.
  - Specjalne umiejętności wież 
  - Różne poziomy trudności i różnorodne mapy.
  - Integracja z systemem punktacji i rankingów.

- **Interfejs Użytkownika:**
  - Intuicyjny interfejs do zarządzania grą.
  - Wskaźniki zdrowia, punktów i zasobów.
