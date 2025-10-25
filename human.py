import random
from world import MovingEntity, WorldGrid, GridEntity

class Human(MovingEntity):
    _counter = 0 #this is used to create the id, you can see it increments by 1 for each instance created
    def __init__(self, hp, stamina, speed, hunger, awareness_radius, world_object):
        super().__init__(hp, stamina, speed, hunger, awareness_radius, world_object)
        Human._counter += 1
        self.id = "human " + str(self._counter)
    
    def get_id(self):
        return self.id

    def consume_food(self, food_value):
        pass # this will be called when human arrives at a supermarket
        self.hunger += 1
   
    def sleep(self):
        self.stamina = 100

    def search_for_camp(self):
        human_coordinates = self.get_coordinates()
        camp_coordinates_list = get_all_camp_coordinates()
        self.get_shortest_path(human_coordinates, camp_coordinates_list)

    def search_for_supermarket(self):
        human_coordinates = self.get_coordinates()
        supermarket_coordinates_list = get_all_supermarket_coordinates()
        self.get_shortest_path(human_coordinates, supermarket_coordinates_list)

    def if_zombie_near(self):
        pass # human ai makes decision

    def run_away_from_zombie(self, zombie_object):
        while self.within_radius(point_a, zombie_object.get_coordinates(), self.awareness_radius):
            pass

    def attack_zombie(self, zombie_object, value):
        point_a = self.get_coordinates()
        if self.within_radius(point_a, zombie_object.get_coordinates(), self.awareness_radius):
            zombie_object.take_damage(value)




