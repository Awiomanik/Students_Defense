# Assets specification 

## audio
(For future use)


-------------------------------------------------------------------------------------------------------------
## gfx

### bullets
(Holds bullets images as png files)


### enemies
(Holds enemies images as png files 60px x 60px)


### HUD
(Holds grphics used in HUD as png files with designated names)
- Towers (200px x 200px):
  (Towers corresponding to towers Assets/gfx/towers rescaled)
- Buttons:
    - `Exit.png` (240px x 240px)
    - `Fast_forward_NA.png` (240px x 240px)
    - `Fast_forward_Off.png` (240px x 240px)
    - `Fast_forward_On.png` (240px x 240px)
    - `Fast_forward_On_2.png` (240px x 240px)
    - `Pause` (240px x 240px)
    - `Play` (240px x 240px)


### maps
(Holds map background images for gamplay and releted data like paths, string representation of accessible tiles, etc... Every map should have image file and assosieted with it data file with the same name.)

- `Name.png` Contains map background image for gameplay. (1920px x 1080px)
- `Name.dat` Contains map related data as lines starting with a key word, colon, corresponding data (except few), id est:
    - Name: xyz
    - Author: xyz
    - Date and time: YYYY-MM-DD HH:MM:SS.ffffff
    - Grid: 
      +---------------------------------+
      |                                 |
      |                                 |
      |       x x x x x x x x           |
      |                     x           |
      |                     x           |
      |                     x x x x x x |
      |                                 |
      | x x x x x x x x x x x x x x x x |
      | x x x x x x x x x x x x x x x x |
      +---------------------------------+
    - size of tile: #px by #px
    - Size of the grid: # tiles by # tiles
    - Paths:
      Path #:
      #, # > #, # > #, # > ...
    Grid should have x's in spots coresponding to tiles that cannot have tower placed on them (tiles with path, tiles with obsticles, two bottom rows are always covered ).
    Paths should have possible paths itemized in seperete rows with numerating rows. The paths itself are 
    written in a format "tile x coord, tile y coord > tile 2 x coord, tile 2 y coord > ...".


### menu
(Contains graphics used in mein menu as png files)

- `high_scores_background.png` (1920px x 1080px)
- `main_menu.png` (1920px x 1080px)


### towers
(Holds towers images as png files 120px x 120px)


-------------------------------------------------------------------------------------------------------------
## lvl_data
(Holds data detailing consecutive levels. Files should be named lvl_#.dat where # are consecutive level numbers)

- `lvl_#.dat` Contains keywords followed by colons and values, id est:
    - Map: xyz (Name of the map used in that level)
    - Gold: # (Amount of gold (integer) player starts level with)
    - Lives: # (Number of lives player starts level with)
    - Wave #: #-xyz (Waves description, first # refers to wave number (consecutive rows should contain following waves information), second # describes number of enemies in that wave, xyz is the name of the enemy in enemy_types dictionary that is public class atribute of the enemy class (`Classes\Enemy\Enemy.py`))
    - Available_towers: xyz, xyz2, xyz3,... (Names of towers (defined as keys of a tower_types dictionary that is public class atribute of the Tower class (`Classes\Tower\Tower_Classes.py`)))


-------------------------------------------------------------------------------------------------------------
## menu_data
(Holds all relevant data that does not concern gameplay itself like high scores)

- `hs.dat` Contains encrypted score records, encrypting and decrypting functions ca be found in `Classes\Utilities.py`.


