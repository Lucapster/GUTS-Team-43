import math
import random


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

    def get_shortest_path(self, point_a, point_b):
        pythag_list = []
        x_a = point_a[0]
        y_a = point_a[1]
        x_b = point_b[0]
        y_b = point_b[1]
        c = math.sqrt(abs(x_a-x_b)**2 + abs(y_a-y_b)**2)
        
        return c

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

    def calculate_compass_direction(self, point_a, point_b):
        angle = self.get_vector_angle(point_a, point_b)
        return self.categorize_compass_direction(angle)
       
    def categorize_compass_direction(self, angle):   
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
        pythag = math.sqrt(abs(x_a-x_b)**2 + abs(y_a-y_b)**2)
        if pythag  <= radius:
            return True

    def take_damage(self, value):
        self.hp -= value

    def hunger_damage(self):
        if self.hunger  <= 0:
            self.hp -= 10

    def move(self, compass_direction):
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
        if (self.y_coordinate + self.speed) > self.world_object.y_dimension:
            random.choice([self.move_west, self.move_east])()
            self.move_south()
            return "Out of bounds"
        else:
            self.y_coordinate += self.speed
        

    def move_south(self):
        if (self.y_coordinate + self.speed) < 0:
            random.choice([self.move_west, self.move_east])()
            self.move_north()
            return "Out of bounds"
        else:
            self.y_coordinate -= self.speed

    def move_west(self):
        if (self.x_coordinate - self.speed) < 0:
            random.choice([self.move_north, self.move_south])()
            self.move_east()
            return "Out of bounds"
        else:
            self.x_coordinate -= self.speed

    def move_east(self):
        if (self.y_coordinate + self.speed) > self.world_object.x_dimension:
            random.choice([self.move_north, self.move_south])()
            self.move_west()
            return "Out of bounds"
        else:
            self.y_coordinate += self.speed

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


