import numpy as np
import random as rand
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math 


class GridEntity:
    def __init__(self, world_object):
        self.world_object = world_object
        self.x_coordinate, self.y_coordinate = world_object.generate_random_coordinate()

    def get_coordinates(self):
        return [self.x_coordinate, self.y_coordinate]

class MovingEntity(GridEntity):
    def __init__(self, hp, stamina, speed, hunger, awareness_radius, world_object):
        super().__init__(world_object)
        self.hp = hp
        self.stamina = stamina
        self.speed = speed
        self.hunger = hunger
        self.awareness_radius = awareness_radius
        self.world_object = world_object

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

    def get_shortest_path(self, point_a, coordinate_list):
        pythag_list = []
        x_a = point[0]
        y_a = point[1]
        for coordinates in coordinate_list:
            x_b = coordinate_list[0]
            y_b = coordinate_list[1]
            c = sqrt(abs(x_a-x_b)**2 + abs(y_a-y_b)**2)
            pythag_list.append(c)
        shortest_path = min(pythag_list)
        i = pythag_list.index(shortest_path)
        
        return coordinate_list[i]

    def get_vector_angle(self, point_a, point_b):
        x_a = point_a[0]
        y_a = point_a[1]
        x_b = point_b[0]
        y_b = point_b[1]
        dx = x_b - x_a
        dy = y_b - y_a

        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)

        angle = round((angle_deg + 360) % 360, 1)
        return angle

    def calculate_compass_move(self, point_a, point_b):
        angle = self.get_vector_angle()
        if 337.5 <= angle < 360 or 0 <= angle < 22.5:
            return "E"
        elif 22.5 <= angle < 67.5:
            return "NE"
        elif 67.5 <= angle < 112.5:
            return "N"
        elif 112.5 <= angle < 157.5:
            return "NW"
        elif 157.5 <= angle < 202.5:
            return "W"
        elif 202.5 <= angle < 247.5:
            return "SW"
        elif 247.5 <= angle < 292.5:
            return "S"
        elif 292.5 <= angle < 337.5:
            return "SE" 


    def within_radius(self, point_a, point_b, radius):
        x_a, y_a = point_a[0], point_a[1]
        x_b, y_b = point_b[0], point_b[1]
        pythag = sqrt(abs(x_a-x_b)**2 + abs(y_a-y_b)**2)
        if pythag  <= radius:
            return True

    def take_damage(self, value):
        self.hp -= value

    def hunger_damage(self):
        if self.hunger  <= 0:
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

class WorldGrid:
    def __init__(self, x_dimension, y_dimension):
        self.x_dimension = x_dimension
        self.y_dimension = y_dimension
        self.x_grid, self.y_grid = np.meshgrid(
            np.arange(0, x_dimension),
            np.arange(0, y_dimension),
            copy=True,
            indexing='ij'
        )
        self.humans = []
        self.zombies = []
        self.human_camps = []
        self.supermarkets = []
        self.fig, self.axes = plt.subplots()
        self.axes.plot([], [], 'k.', markersize=2) #start with empty plot


    def generate_random_coordinate(self):
        x = rand.randint(0, self.x_dimension)
        y = rand.randint(0,self.y_dimension)
        return x,y

    def get_all_camp_coordinates(self):
        camp_coordinates = []
        for camp in self.human_camps:
           coordinates = camp.get_coordinates() 
           camp_coordinates.append(coordinates)
        return camp_coordinates


    def get_all_supermarket_coordinates(self):
        supermarket_coordinates = []
        for supermarket in self.supermarkets:
           coordinates = supermarket.get_coordinates() 
           supermarket_coordinates.append(coordinates)
        return supermarket_coordinates

    """"
    def add_ready_human(self, human):
        self.humans.append(human)
        self.add_human_to_plot(human.x_coordinate, human.y_coordinate)
        return human

    
    def add_human(self):
        stats = {
            'hp': 10,
            'stamina': 2,
            'speed': 1,
            'awareness_radius': 1
        }
        hunger = 0
        extra_points = 10
        stat_keys = list(stats.keys())

        for _ in range(extra_points):
            chosen_stat = rand.choice(stat_keys)
            stats[chosen_stat] += 1

        human = Human(
            hp=stats['hp'],
            stamina=stats['stamina'],
            speed=stats['speed'],
            hunger=hunger,
            awareness_radius=stats['awareness_radius'],
            world=self
        )

        self.humans.append(human)
        self.add_human_to_plot(human.x_coordinate, human.y_coordinate)
        return human

    def add_zombie(self):
        stats = {
            'hp': 10,
            'stamina': 2,
            'speed': 1,
            'awareness_radius': 1,
            'infection_probability': 0.5
        }
        hunger = 0
        extra_points = 10
        stat_keys = list(stats.keys())

        for _ in range(extra_points):
            chosen_stat = rand.choice(stat_keys)
            if chosen_stat == 'infection_probability':
                stats[chosen_stat] = min(stats[chosen_stat] + 0.05, 1.0)
            else:
                stats[chosen_stat] += 1

        zombie = Zombie(
            hp=stats['hp'],
            stamina=stats['stamina'],
            speed=stats['speed'],
            hunger=hunger,
            awareness_radius=stats['awareness_radius'],
            infection_probability=stats['infection_probability'],
            world=self
        )

        self.zombies.append(zombie)
        self.add_zombie_to_plot(zombie.x_coordinate, zombie.y_coordinate)
        return zombie

    def add_ready_zombie(self, zombie):
        self.zombies.append(zombie)
        self.add_zombie_to_plot(zombie.x_coordinate, zombie.y_coordinate)
        return zombie
    """
    
    def add_supermarket(self, food_available):
        supermarket = Supermarket(food_available, self)
        self.add_supermarket_to_plot(supermarket.x_coordinate, supermarket.y_coordinate)
        return supermarket

    def add_human_camp(self, capacity):
        human_camp = HumanCamp(capacity, self)
        self.human_camps.append(human_camp)
        self.add_human_camp_to_plot(human_camp.x_coordinate, human_camp.y_coordinate)
        return human_camp

    def decrease_supermarket_food(self, supermarket_object, human_object):
        food_taken = human_object.get_gluttony_rate()
        supermarket_object.food_available -= food_taken
   
    def add_human_to_plot(self, x, y):
        self.axes.plot(x, y, c='blue')

    def add_zombie_to_plot(self, x, y):
        self.axes.plot(x, y, c='green')

    def add_supermarket_to_plot(self, x, y):
        self.axes.plot(x, y, 'ro')
        self.fig.canvas.draw()

    def add_human_camp_to_plot(self, x, y):
        self.axes.plot(x, y, c='purple')

    def update_plot(self, frame = None):
        pass
        #self.axes.clear()  # clearing the axes
        
    def show_plot(self): # Creates an xy plot for testing purposes
        anim = FuncAnimation(self.fig, self.update_plot, interval=1000) #may not be needed when Yang finishes his script
        plt.show()  

class Supermarket(GridEntity):
    def __init__(self, food_available, world_object):
        super().__init__(world_object)
        self.food_available = food_available
        self.world_object = world_object

    def get_food_available(self):
        return self.food_available

class HumanCamp:
    def __init__(self, capacity, world_object):
        super().__init__(world_object)
        self.capacity = capacity
        self.humans = []
        self.population = len(self.humans)
        self.world_object = world_object
        
    def get_capacity(self):
        return self.capacity

    def get_population(self):
        return self.population

    def add_human_to_camp(self, human_object):
        if self.population >= self.capacity:
            return "Too many humans in this camp."
        else:
            self.population += 1
            self.humans.append(human_object)
        
myworld = WorldGrid(20,20)
#print(f"X-GRID:{myworld.x_grid}, Y-GRID:{myworld.y_grid}")
for i in range(10):
    myworld.add_supermarket(i)
myworld.show_plot()