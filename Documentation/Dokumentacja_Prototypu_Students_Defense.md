### Dokumentacja Gry Student Defense

#### 1. Instrukcja Uruchomienia Gry

##### 1.1 Wymagane Biblioteki
Aby uruchomić gry, należy zainstalować poniższe biblioteki:
- `pygame`
- `os`

Komenda instalacji:
```bash
pip install pygame
```

##### 1.2 Uruchomienie Prototypu
1. Po uruchomieniu gry pojawi się intro, które zostanie wyświetlone na ekranie.
2. Następnie pojawi się główne menu, w którym gracz może wybrać rozpoczęcie gry lub zakończenie.
3. Po wyborze rozpoczęcia gry gracz przechodzi do właściwej rozgrywki.
4. Podczas rozgrywki gracz może kupować oraz budować wieże i bronić swoją pozycję przed nadchodzącymi falami wrogów.

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

#### 2.5 Klasa `Enemy`
- **Metody:**
 - `__init__(self, life: int, speed: int, image, position: Tuple[int, int], destination: Tuple[int, int])`: Inicjalizuje przeciwnika z określonymi parametrami.
 - `calculate_direction(self) -> Tuple[float, float]`: Oblicza kierunek ruchu przeciwnika na podstawie jego pozycji i celu.
 - `move(self)`: Przesuwa przeciwnika w kierunku celu.
 - `update(self)`: Aktualizuje stan przeciwnika (np. wykonuje ruch).
 - `__str__(self) -> str`: Zwraca reprezentację przeciwnika jako string.

##### 2.6 Klasa `Game`
- **Metody:**
  - `__init__(self, display_intro: bool = True) -> None`: Inicjalizuje instancję gry.
  - `run_game_loop(self) -> None`: Rozpoczyna główną pętlę rozgrywki.
  - `__main__()`: Funkcja uruchamiająca grę.



#### 3. Planowany Diagram Klas UML

Diagram klas przedstawia zależności pomiędzy klasami oraz ich atrybuty i metody:

----------------------------------------
|                Game                  |
----------------------------------------
| - ui: UI                             |
| - towers: TowerManager               |
| - player: Player                     |
| - level: Level                       |
----------------------------------------
| + __init__(display_intro: bool)      |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|                 UI                   |
----------------------------------------
| - screen: pygame.Surface             |
| - clock: pygame.time.Clock           |
| - mouse_click: bool                  |
| - pos: Tuple[int, int]               |
| - gfx_path: str                      |
----------------------------------------
| + intro()                            |
| + main_menu() -> bool                |
| + load_lvl(map_name: str,            |
|            towers_names: Dict[str,   |
|                         str],        |
|            bullets_names: Dict[str, |
|                            str]) ->  |
|            None                      |
| + update()                           |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|             TowerManager             |
----------------------------------------
| - towers: List[Tower]                |
----------------------------------------
| + reset()                            |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|               Player                 |
----------------------------------------
| - name: str                          |
| - gold: int                          |
| - tower_manager: TowerManager        |
| - placed_towers: List[Tower]         |
----------------------------------------
| + can_afford_tower(tower: Tower) ->  |
|   bool                               |
| + place_tower(tower: Tower, x: int,  |
|   y: int) -> bool                    |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|                Level                 |
----------------------------------------
| - level_number: int                  |
| - enemy_waves: List[Dict[str,       |
|                   Tuple[int, int]]] |
----------------------------------------
| + add_wave(enemy_type: Enemy,       |
|            quantity: int,            |
|            interval: int) -> None    |
| + start_level() -> None              |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|                Map                   |
----------------------------------------
| - name: str                          |
| - paths: Tuple[Tuple[Coord]]         |
| - grid: List[List[bool]]             |
----------------------------------------
| + __init__(name: str,               |
|             map_data_directory: str) |
| + load_map_data(path: str) -> None  |
| + __str__() -> str                   |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|                Enemy                 |
----------------------------------------
| - life: int                          |
| - speed: int                         |
| - image                              |
| - x: int                             |
| - y: int                             |
| - position                           |
| - destination                        |
| - direction                          |
----------------------------------------
| + __init__(life: int,                |
|            speed: int,               |
|            image,                    |
|            position,                 |
|            destination)             |
| + calculate_direction() -> Tuple[int,|
|                                int]   |
| + move() -> None                     |
| + update() -> None                   |
| + __str__() -> str                   |
----------------------------------------


#### 4. Zaktualizowany Plan Działania na Kolejne Tygodnie Pracy
- Implementacja podstawowej mechaniki gry, w tym rysowanie interfejsu użytkownika, ruchu przeciwników i ataków wież.
- Dodanie zaawansowanych funkcji, takich jak różne typy przeciwników i wież oraz bardziej złożone ścieżki ruchu.
- Testowanie i optymalizacja kodu, aby upewnić się, że gra działa płynnie i bez błędów.


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
