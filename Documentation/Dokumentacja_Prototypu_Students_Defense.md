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

#### 2. Instrukcja Użytkowania

##### 2.1 Klasa `Level`
- **Metody:**
  - `__init__(self, level_number: int)`: Inicjalizuje poziom o podanym numerze.
  - `add_wave(self, enemy_type: enm.Enemy, quantity: int, interval: int)`: Dodaje falę przeciwników.
  - `get_waves(self) -> List[Dict[str, Tuple[int, int]]]`: Zwraca listę fal przeciwników.
  - `start_level(self)`: Rozpoczyna poziom, wyświetlając informacje o falach przeciwników.

##### 2.2 Klasa `Map`
- **Metody:**
  - `__init__(self, name: str = "TEST_1", map_data_directory: str = None)`: Inicjalizuje mapę na podstawie pliku danych mapy.
  - `load_map_data(self, path: str)`: Ładuje dane mapy z pliku.

##### 2.3 Klasa `Tower`
- **Metody:**
  - `__init__(self, range: int, damage: int, atk_speed: int, shot_count: int, targeting: bool, bouncing: bool, own_asset, shot_asset)`: Inicjalizuje wieżę z podanymi parametrami.

##### 2.4 Klasa `Tower_Manager`
- **Metody:**
  - `__init__(self, tower_type: Tower, coord, enemies)`: Inicjalizuje menedżera wież dla podanego typu wieży, współrzędnych i przeciwników.
  - `reset(cls)`: Resetuje listę wież.
  - `attack(self)`: Wykonuje atak wieży na wrogów w zasięgu.

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
