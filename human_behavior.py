import random
import math
from entity_structure import MovingEntity, GridEntity
import scipy as sci


class Human(MovingEntity):
    _counter = 0 #this is used to create the id, you can see it increments by 1 for each instance created
    def __init__(self, hp, stamina, speed, hunger, awareness_radius, world_object):
        super().__init__(hp, stamina, speed, hunger, awareness_radius, world_object)
        Human._counter += 1
        self.id = "human " + str(self._counter)
    
    def get_id(self):
        return self.id

    def consume_food(self):
        while self.hunger <= 100:
            self.hunger += 10
   
    def sleep(self):
        self.stamina = 100

    def get_nearest_supermarket_position(self):
        tree, coordinate_list = self.world_object.get_all_supermarket_coordinates()
        distance, index = tree.query(self.get_coordinates())
        return supermarket, coordinate_list[index]

    def get_nearest_human_camp_position(self):
        tree, coordinate_list = self.world_object.get_all_human_coordinates()
        distance, index = tree.query(self.get_coordinates())
        return coordinate_list[index]

    
    def get_nearest_zombie_position(self):
        tree, coordinate_list = self.world_object.get_all_zombie_coordinates()
        if tree is None or not coordinate_list:
            return None, None  
        distance, index = tree.query(self.get_coordinates())
        zombie = self.world_object.zombies[index]
        return zombie, coordinate_list[index]


    def zombie_nearby(self):
        zombie, zombie_coords = self.get_nearest_zombie_position()
        if self.within_radius(self.get_coordinates(), zombie_coords, self.awareness_radius):
            return True


    def run_away_from_zombie(self, zombie_coordinates):
        direction = self.calculate_compass_direction(zombie_coordinates, self.get_coordinates())
        self.move(direction)

    def run_away_from_zombie2(self, zombie_coordinates):
        U_attr = self.calculate_attractive_potential()
        U_rep = self.calculate_repulsive_potential(zombie_coordinates)
        U_x = [U_attr[0] + U_rep[0], U_attr[1] + U_rep[1]]
        force = -U_x
        angle_rad = math.atan2(force[0], force[1])
        angle_deg = math.degrees(angle_rad)
        angle = round((angle_deg + 360) % 360, 1) 
        direction = self.categorize_compass_direction(angle)
        self.move(direction)

    def calculate_attractive_potential(self):
        nearest_camp_coords = self.get_nearest_human_camp_position()
        k_attr = 5
        distance = self.get_shortest_path(self.get_coordinates(),nearest_camp_coords)
        #U_attr = (1/2)*attractive_gain_constant*distance**2
        human_coords = self.get_coordinates()
        dx = human_coords[0] - nearest_camp_coords[0]
        dy = human_coords[1] - nearest_camp_coords[1]
        magnitude = math.sqrt(dx**2 + dy**2)
        if magnitude > 0:
            attractive_direction_vector = [(dx/magnitude) *k_attr, (dy/magnitude) * k_attr]
            return attractive_direction_vector
        else:
            return 0

    def calculate_repulsive_potential(self, zombie_coordinates):
        k_rep = 5
        influence_range = 4
        dx = self.coordinate_list[0] - zombie_coordinates[0]
        dy = self.coordinate_list[1] - zombie_coordinates[1]
        magnitude = math.sqrt(dx**2 + dy**2)
        repulsive_direction_vector = [(dx/magnitude) * k_rep, (dy/magnitude) * k_rep]

        if distance <= influence_range: 
            U_rep = (1/2)*repulsive_gain_constant*(distance**(-1)-influence_range**(-1))**2
        else:
            U_rep = 0

        return repulsive_direction_vector

    def move_towards_building(self, building_coordinates):
        direction = self.calculate_compass_direction(building_coordinates, self.get_coordinates())
        self.move(direction)

    def attack_zombie(self, zombie_object, value):
        point_a = self.get_coordinates()
        if self.within_radius(point_a, zombie_object.get_coordinates(), self.awareness_radius):
            zombie_object.take_damage(value)

 
    def update_behavior(self):
        if self.hp <= 0:
            self.world_object.add_zombie(self.hp, self.stamina, self.speed, self.hunger, self.awareness_radius, 0.5)
            self.world_object.delete_human(self)
            print("Deleted human")
            
            return

        zombie, zombie_coords = self.get_nearest_zombie_position()
        if zombie is None:
            random_direction = random.choice(["N","S","W","E","NW","NE","SW","SE"])
            self.move(random_direction)
        elif self.within_radius(self.get_coordinates(), zombie_coords, self.awareness_radius):
            self.run_away_from_zombie(zombie_coords)
        else:
            random_direction = random.choice(["N","S","W","E","NW","NE","SW","SE"])
            self.move(random_direction)
    

        



