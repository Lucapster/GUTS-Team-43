import numpy as np
import random as rand
import matplotlib.pyplot as plt
import scipy as sci
from matplotlib.animation import FuncAnimation
import math 
from human_behavior import Human
from zombie_behavior import Zombie
from entity_structure import GridEntity


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
        self.is_night = False

        self.fig, self.axes = plt.subplots()
        self.axes.set_xlim(0, self.x_dimension)
        self.axes.set_ylim(0, self.y_dimension)
        self.axes.set_title("Zombie Apocalypse Simulation")

        self.human_scatter = self.axes.plot([], [], 'bo', label="Humans")[0]
        self.zombie_scatter = self.axes.plot([], [], 'go', label="Zombies")[0]

        self.supermarket_scatter = None
        self.camp_scatter = None
        self.legend = None #need to initalize it as none and create legend in draw_static_background()

    def generate_random_coordinate(self):
        x = rand.randint(0, self.x_dimension)
        y = rand.randint(0, self.y_dimension)
        return x, y

    def get_all_camp_coordinates(self):
        return [camp.get_coordinates() for camp in self.human_camps]

    def get_all_supermarket_coordinates(self):
        return [supermarket.get_coordinates() for supermarket in self.supermarkets]

    def get_all_human_coordinates(self):
        if not self.humans:
            return None, []
        coords = [h.get_coordinates() for h in self.humans]
        return sci.spatial.cKDTree(coords), coords

    def get_all_zombie_coordinates(self):
        if not self.zombies:
            return None, []
        coords = [z.get_coordinates() for z in self.zombies]
        return sci.spatial.cKDTree(coords), coords

    def add_human(self, hp, stamina, speed, hunger, awareness_radius):
        human = Human(hp, stamina, speed, hunger, awareness_radius, self)
        self.humans.append(human)
        return human

    def add_zombie(self, hp, stamina, speed, hunger, awareness_radius, infection_probability):
        zombie = Zombie(hp, stamina, speed, hunger, awareness_radius, infection_probability, self)
        self.zombies.append(zombie)
        return zombie

    def add_supermarket(self, food_available):
        supermarket = Supermarket(food_available, self)
        self.supermarkets.append(supermarket)
        return supermarket

    def add_human_camp(self, capacity):
        camp = HumanCamp(capacity, self)
        self.human_camps.append(camp)
        return camp

    def delete_zombie(self, zombie_object):
        if zombie_object in self.zombies:
            self.zombies.remove(zombie_object)
            del zombie_object

    def delete_human(self, human_object):
        if human_object in self.humans:
            self.humans.remove(human_object)
            del human_object

    
    def draw_static_background(self):
        handles = [self.human_scatter, self.zombie_scatter]
        labels = ["Humans", "Zombies"]

        if self.supermarkets:
            xs, ys = zip(*[s.get_coordinates() for s in self.supermarkets])
            self.supermarket_scatter = self.axes.plot(xs, ys, 'rs', markersize=6)[0]
            handles.append(self.supermarket_scatter)
            labels.append("Supermarkets")

        if self.human_camps:
            xs, ys = zip(*[c.get_coordinates() for c in self.human_camps])
            self.camp_scatter = self.axes.plot(xs, ys, 'p', color='purple', markersize=8)[0]
            handles.append(self.camp_scatter)
            labels.append("Camps")

        if self.legend is None:
            self.legend = self.axes.legend(handles, labels, loc="upper right", framealpha=0.9)



    
    def update(self, frame):
        for h in list(self.humans):
            h.update_behavior()
        for z in list(self.zombies):
            z.update_behavior()

        if self.humans:
            hx, hy = zip(*[h.get_coordinates() for h in self.humans])
            self.human_scatter.set_data(hx, hy)
        else:
            self.human_scatter.set_data([], [])

        if self.zombies:
            zx, zy = zip(*[z.get_coordinates() for z in self.zombies])
            self.zombie_scatter.set_data(zx, zy)
        else:
            self.zombie_scatter.set_data([], [])

        return [self.human_scatter, self.zombie_scatter]


    def show_plot(self):
        self.draw_static_background()

        anim = FuncAnimation(
            self.fig,
            self.update,
            interval=200,
            blit=False,
            repeat=False
        )
        plt.show()


class Supermarket(GridEntity):
    def __init__(self, food_available, world_object):
        super().__init__(world_object)
        self.food_available = food_available

    def get_food_available(self):
        return self.food_available


class HumanCamp(GridEntity):
    def __init__(self, capacity, world_object):
        super().__init__(world_object)
        self.capacity = capacity
        self.humans = []
        self.population = 0

    def add_human_to_camp(self, human_object):
        if self.population >= self.capacity:
            return "Too many humans in this camp."
        else:
            self.population += 1
            self.humans.append(human_object)



myworld = WorldGrid(20, 20)

# add entities
for _ in range(10):
    myworld.add_human(100, 100, 1, 100, 10)
for _ in range(10):
    myworld.add_zombie(100, 100, 1, 100, 10, 0.5)
for _ in range(2):
    myworld.add_supermarket(50)
for _ in range(2):
    myworld.add_human_camp(10)

h = Human(100, 100, 1, 100, 10, myworld)
print("Before move:", h.get_coordinates())
h.move("N")
h.move("N")
h.move("N")
h.move("N")
print("After move:", h.get_coordinates())
# run
myworld.show_plot()



