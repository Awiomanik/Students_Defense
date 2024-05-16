"""
Prototypical Enemy Class.

Just a playground for testing enemy functionality. Not meant for production.

This module defines the Enemy class which represents a generic enemy.
The enemy moves, with some autonomy, within a predefined circle 
that moves along a predefined path and has various
attributes like health, size, and speed.
"""


# IMPORTS
import pygame
import random

# Aliases for often used functions
vec = pygame.math.Vector2


# ENEMY CLASS
class Enemy:
    """
    A class that represents an enemy, capable of autonomous movement within a dynamic boundary.

    This class models an enemy with a circular autonomy zone, moving along a predefined path, 
    reflecting some degree of unpredictable behavior and responding to the game's environment.

    
    Class-level atributes:

    enemy_count (int): Tracks the number of enemy instances.

    
    Instance-level atributes:

    health (int): Health of the enemy, defining how much damage it can take before being defeated.
    
    size (int): The size of the enemy's graphic in pixels. Assumes the graphic is square (size x size).
    
    pos (pygame.math.Vector2): The current position of the enemy on the game map in pixels.
    
    autonomy_radius_pos (pygame.math.Vector2): The center position of the circle defining the autonomy radius within which the enemy can move in pixels.
    
    current_autonomy_radius_target (pygame.math.Vector2): The current target position within the path that the autonomy radius is moving towards in pixels.
    
    current_autonomy_radius_direction (pygame.math.Vector2): A normalized vector representing the direction from the autonomy radius center to the current target.
    
    path (list[tuple[int, int]]): The predefined path that the enemy's autonomy radius follows, represented as a list of pixel coordinate tuples.
    
    path_index (int): The current index in the path that the enemy's autonomy radius is targeting.
    
    num_of_targets (int): The total number of targets in the path that the enemy will attempt to reach.
    
    path_widths (list[int]): Widths of the path at each segment, used to dynamically adjust the autonomy radius.
    
    speed (int): The speed at which the enemy's autonomy radius moves towards its endpoint in pixels per frame.
    
    current_autonomy_radius (int): The current size of the autonomy radius within which the enemy can move.
    
    local_pos (pygame.math.Vector2): The enemy's position relative to the center of the autonomy radius.
    
    face (pygame.Surface): The graphical representation of the enemy, loaded from the specified path and scaled to the given size.
    
    max_local_speed (int): The maximum speed at which the enemy can move within its autonomy radius.

    current_local_speed (pygame.math.Vector2): Current local speed of the enemy within the autonomy radius relative to the autonomy radius center in pixels per frame, limited by max_local_speed.


    Methods:

    move_autonomy_radius() -> bool:
        Moves the autonomy radius towards the current target and updates its size. Returns True if the end of the path is reached.

    move_enemy() -> None:
        Moves the enemy within its autonomy radius, ensuring it doesn't exit this boundary.

    update() -> bool:
        Updates the enemy's position by first moving the autonomy radius and then adjusting the enemy's position within it. Returns True if the enemy reaches the endpoint of its path.

    draw(screen, draw_autonomy_radius=False) -> None:
        Draws the enemy and optionally its autonomy radius on the specified game screen.

    __del__() -> None:
        Cleans up the enemy instance, decrementing the class-level enemy counter.
    """
    
    # Enemies counter
    enemy_count = 0

    def __init__(self, 
                 graphic_path: str, 
                 path_to_follow: list[tuple[int, int]],
                 path_widths: list[int],
                 size: int = 100, 
                 speed: int = 5,
                 max_local_speed: int = 5,
                 health: int = 100) -> None:
        """
        Initialize the Enemy object with given attributes.

        Parameters:
        graphic_path : str -- Path (absolute or relative) to the graphic image of the enemy.
        path_to_follow : list[tuple[int, int]] -- List of tuples representing the path coordinates in pixels (width, height).
        path_widths : list[int] -- List of integers representing the widths of the path at each segment in pixels.
        size : int, optional -- Size of the enemy grphic in pixels (Enemy graphics should be squeres side size) (default is 100).
        speed : int, optional -- Speed of the enemy in tenths of a pixel per frame. Defines movement of the autonomy_radius within which the enemy moves self-directed (default is 5).
        max_local_speed : int, optional -- Defines the maximum speed at which the enemy moves inside the autonomy_radius in pixels per frame. Measure of motion chaoticity of the enemy. Not recommended to set below 5. (default is 5)
        health : int, optional -- Health of the enemy (default is 100).
        """
        # Basic enemy parameters
        self.health = health
        self.size = size

        # Global enemy movement
        # Starting position of the center of autonomy radius
        self.autonomy_radius_pos = vec(path_to_follow[0])  
        # Position of the first target for the enemy
        self.current_autonomy_radius_target = vec(path_to_follow[1]) 
        # Vector pointing from autonomy radius center to current target
        self.current_autonomy_radius_direction = \
            vec((self.current_autonomy_radius_target - self.autonomy_radius_pos).normalize())
        # List of targets to follow
        self.path = path_to_follow
        # Current target index
        self.path_index = 1
        # Number of targets to visit by enemy (-starting point)
        self.num_of_targets = len(path_to_follow) - 1 
        # Width of the path at each segment between two targets
        self.path_widths = [path_widths[0]] + path_widths + [path_widths[-1]]
        # Speed of the autonomy readius movement towards endpoint
        self.speed = speed

        # Movement of the enemy within autonomy radius
        # Radius of enemy's autonomy
        self.current_autonomy_radius = path_widths[0]
        # Position of the enemy relative to the center of the autonomy radius
        component = int(self.current_autonomy_radius / 1.5) # ~= sqrt(2)
        self.local_pos = vec(random.randint(-component, component), 
                             random.randint(-component, component))
        # Starting position of the enemy on the map (Global)
        self.pos = vec(path_to_follow[0]) + self.local_pos 
        # Maximum speed of the enemy within the autonomy radius
        self.max_local_speed = max_local_speed
        # Current relative speed of movement within the autonomy radius
        component = int(max_local_speed / 1.5) # ~= sqrt(2)
        self.current_local_speed = vec(random.randint(-component, component), 
                                        random.randint(-component, component))


        # Image loaded and scaled it to the given size
        self.face = pygame.transform.scale(pygame.image.load(graphic_path), (size, size))

        # Update class-level enemy counter
        Enemy.enemy_count += 1

        # logging for testing rasons
        print(f"New enemy just dropped!\nCurrent number of enemies on the map: {Enemy.enemy_count}\n")

    def move_autonomy_radius(self) -> bool:
        """
        Move the autonomy radius towards the current target, updating its position and size.

        This function manages the movement of the autonomy radius, which encircles the enemy. 
        It checks if the autonomy radius has reached its current target point on the path. 
        - If the target is reached, it snaps to this point and updates to the next target if available. 
        - If the endpoint of the path is reached, a message is printed. 
        - If not yet at the target, the autonomy radius moves towards it. 
        The size of the autonomy radius is adjusted based on the path widths to account for narrowing or widening of the path.

        The function operates by calculating the distance to the target 
        and comparing it to the enemy's speed to decide whether to move or snap to the target. 
        It also dynamically adjusts the size of the autonomy radius based on the current, previous, and next path widths 
        to handle corners and path width changes smoothly.

        Returns:
        bool -- Returns True if the autonomy radius center has reached the end of the path, otherwise False.
        """
        # helping variable
        distance = self.autonomy_radius_pos.distance_to(self.current_autonomy_radius_target)

        # If current position of circle at target position (or closer then speed)
        if distance <= self.speed:
            # Snap position of the circle to the next target
            self.autonomy_radius_pos = self.current_autonomy_radius_target.copy()  

            # If current target not the endpoint
            if self.path_index < self.num_of_targets:
                # Update atributes
                self.path_index += 1
                self.current_autonomy_radius_target = vec(self.path[self.path_index])
                self.current_autonomy_radius_direction = \
                    vec((self.current_autonomy_radius_target - self.autonomy_radius_pos).normalize())

            # Autonomy radius center reached the target
            else: return True

        # If target not yet reached, move autonomy radius towards the target
        else: self.autonomy_radius_pos += self.current_autonomy_radius_direction * self.speed

        # Update circle size (make it accordingly smaller if cornering to/from smaller path)
        self.current_autonomy_radius = \
            min(self.path_widths[self.path_index], 
                distance + self.path_widths[self.path_index + 1], 
                distance + self.path_widths[self.path_index - 1])

        # Update circle size to not be smaller then the enemy + 2, so to make it at least wiggle a bit
        self.current_autonomy_radius = max(self.current_autonomy_radius, self.size//2 + 2)

        # Autonomy circle has not yet reached endpoint, return False
        return False

    def move_enemy(self) -> None:
        """
        Move the enemy within the autonomy_radius.

        
        Ensure the enemy stays within the current autonomy_radius and update its speed.
        """

        # Randomly adjust speed of the enemy
        self.current_local_speed += vec(random.randint(-1, 1), random.randint(-1, 1))

        # Check if changed speed did exceed maximum speed for the enemy and if so slow it down
        if self.current_local_speed.length() > self.max_local_speed:
            self.current_local_speed /= 2

        # Test if enemy did walk outside of the autonomy radius
        if self.local_pos.length() > self.current_autonomy_radius:
            # Normalized vector pointing from autonomy radius center towards the enemy
            direction = (self.pos - self.autonomy_radius_pos).normalize()
            # Put enemy on the point on boundary of the autonomy radius closest to the enemy
            self.local_pos = direction * self.current_autonomy_radius
            # Bounce the enemy of the boundary by setting its speed to opposite with some dumping
            self.current_local_speed = -self.current_local_speed * 0.5

        # If enemy in the autonomy radius set new local enemy position within the autonomy radius
        else:
            self.local_pos += self.current_local_speed

        # Set global position of the enemy on the map 
        self.pos = self.autonomy_radius_pos + self.local_pos

    def update(self) -> bool:
        """
        Update the enemy's position by moving its autonomy radius along its predefined path and adjusting its position within it.

        This method first attempts to move the autonomy radius toward the current target. 
        If the autonomy radius center has reached the endpoint of the path, it logs a message and returns True.
        If the endpoint is not yet reached, it then adjusts the enemy's position within the autonomy radius.

        Returns:
        bool -- True if the enemy has reached the endpoint, otherwise False.
        """
        # Move the autonomy radius and see if it reached the endpoint
        if self.move_autonomy_radius(): 
            print(f"Enemy has reached the endpoint!\nRemaining enemies: {Enemy.enemy_count - 1}\n")
            return True
        
        # If endpoint not yet reached move enemy and return False
        self.move_enemy()
        return False

    def draw(self, screen, draw_autonomy_radius=False) -> None:
        """
        Draw the enemy on the screen.

        Parameters:
        screen : pygame.Surface -- The surface to draw the enemy on (pygame.screen).
        draw_autonomy_radius : bool, optional -- If True, draw a circle representing the current autonomy_radius of the enemy (default is False).
        """
        # Draw the enemy
        screen.blit(self.face, (int(self.pos.x) - self.size//2, int(self.pos.y) - self.size//2))
        
        # If testing flag is on draw the autonomy radius of the enemy
        if draw_autonomy_radius:
            pygame.draw.circle(screen, (0, 255, 0), 
                               (int(self.autonomy_radius_pos.x), int(self.autonomy_radius_pos.y)), 
                               self.current_autonomy_radius, 1)

    def __del__(self) -> None:
        """
        Destructor called when an Enemy instance is about to be destroyed.
        
        Decrements the global enemy_count.
        """
        Enemy.enemy_count -= 1







