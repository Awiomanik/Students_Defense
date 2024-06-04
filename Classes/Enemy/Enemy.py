#they should have they life, speed, image, position and destination 
#enemy moves from his position (tuple) to destination (tuple)

class Enemy():
    def __init__(self, life: int, speed: int, image, position, destination):
        self.life = life
        self.speed = speed
        self.image = image
        self.x, self.y = position 
        self.position = position  #position in game 
        self.destination = destination
        self.direction = self.calculate_direction()


    def calculate_direction(self):
        x_new = self.destination[0] - self.position[0] #coordinates of the direction vector
        y_new = self.destination[1] - self.position[1]
        distance = (x_new**2 + y_new**2) ** 0.5 #length of the vector
        if distance == 0:
            return (0, 0)
        return (x_new / distance, y_new / distance) #normalizing the vector

    def move(self):
        if (self.x, self.y) != self.destination:
            self.x += self.direction[0] * self.speed #adding to x, normalized vector[0]*speed (which is scalar here)
            self.y += self.direction[1] * self.speed

            #for enemy to stop in the right place, not to fly too far
            if (self.direction[0] > 0 and self.x >= self.destination[0]) or (self.direction[0] < 0 and self.x <= self.destination[0]):
                self.x = self.destination[0]
            if (self.direction[1] > 0 and self.y >= self.destination[1]) or (self.direction[1] < 0 and self.y <= self.destination[1]):
                self.y = self.destination[1]

            self.position = (self.x, self.y)

    def update(self):
        self.move()

    def __str__(self):
       return f"Enemy(life={self.life}, speed={self.speed}, position=({self.x}, {self.y}))"
    

    
    


