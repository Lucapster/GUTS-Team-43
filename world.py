import numpy as np
import random as rand
import matplotlib.pyplot as plt

class GridEntity:
    def __init__(self, world_object):
        self.world_object = world_object
        self.x_coordinate, self.y_coordinate = world_object.generate_random_coordinate()

class MovingEntity(GridEntity):
    def __init__(self, hp, stamina, speed, hunger, awareness_radius, food_value):
        super().__init__(self, world_object)
        self.hp = hp
        self.stamina = stamina
        self.speed = speed
        self.hunger = hunger
        self.awareness_radius = awareness_radius
        self.food_value = food_value

    def get_awareness(self):
        return self.awareness

    def get_hp(self):
        return self.hp

    def get_stamina(self):
        return self.stamina

    def get_speed(self):
        return self.speed

    def get_hunger(self):
        return self.hunger

    def hunger_damage(self):
        if self.hunger <= 0:
            self.hp -= 10


    def move_entity(self, compass_direction):
        if compass_direction == "N":
            self.move_north()
        elif compass_direction == "S":
            self.move_south()
        elif compass_direction == "W":
            self.move_west()
        elif compass_direction == "E":
            self.move_east()
        elif compass_direction == "NW":
            self.move_northwest()
        elif compass_direction == "NE":
            self.move_northeast()
        elif compass_direction == "SW":
            self.move_southwest()
        elif compass_direction == "SE":
            self.move_southeast()

    def move_north(self):
        self.y_coordinate += self.speed

    def move_south(self):
        self.y_coordinate -= self.speed

    def move_west(self):
        self.x_coordinate += self.speed

    def move_east(self):
        self.x_coordinate -= self.speed

    def move_northeast(self):
        self.move_north()
        self.move_east()

    def move_northwest(self):
        self.move_north()
        self.move_east()

    def move_southeast(self):
        self.move_south()
        self.move_east()

    def move_southwest(self):
        self.move_south()
        self.move_east()

            
    def update_entity_coordinate(self, new_x_coordinate, new_y_coordinate):
        self.x_coordinate = new_x_coordinate
        self.y_coordinate = new_y_coordinate

#class StillEntity(GridEntity):
#    def __init__(self, world_object):
#        self.world_object = world_object
#        x_coordinate, y_coordinate = world_object.generate_random_coordinate()

    

class WorldGrid:
    def __init__(self, x_dimension, y_dimension):
        self.x_dimension = x_dimension
        self.y_dimension = y_dimension
        #self.gluttony_rate = gluttony_rate #this will be defined in the simulation engine, will probably move this
        self.x_grid, self.y_grid = np.meshgrid(x_dimension, y_dimension, copy=True, indexing='ij')

    def generate_random_coordinate(self):
        x = rand.randint(0, self.x_dimension)
        y = rand.randint(0,self.y_dimension)
        return x,y
    
    def add_human(self):
        human = Human()
        return human
        # code for adding instancing human_object and adding to grid

    def add_zombie(self):
        zombie = Zombie()
        return zombie
         # code for adding instancing human_object and adding to grid

    def add_supermarket(self, food_available):
        x, y = self.generate_random_coordinate()
        supermarket = Supermarket(food_available)
        # add supermarket to grid

    def decrease_supermarket_food(self, supermarket_object, human_object):
        food_taken = human_object.get_gluttony_rate()
        supermarket_object.food_available -= food_taken

    def add_human_camp(self, capacity):
        human_camp = HumanCamp(capacity)

    def show_plot(self): # Creates an xy plot for testing purposes
        plt.plot(self.x_grid, self.y_grid, marker='o', color='k', linestyle='none')
        plt.show()

class Supermarket:
    def __init__(self, food_available):
        self.food_available = food_available

    def get_food_available(self):
        return self.food_available

class HumanCamp:
    def __init__(self, capacity):
        self.capacity = capacity
        self.humans = []
        self.population = len(self.humans)
        
    def get_capacity(self):
        return self.capacity

    def get_population(self):
        return self.population

    def add_human_to_camp(self, human_object):
        if self.population >= self.capacity:
            return "Too many humans in this camp."
        else:
            self.population += 1
        


test_world = WorldGrid(10, 10)
test_world.show_plot()
