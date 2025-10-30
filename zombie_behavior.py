from entity_structure import MovingEntity
import random


class Zombie(MovingEntity):
    _counter = 0
    def __init__(self, hp, stamina, speed, hunger, awareness_radius, infection_probability, world_object):
        super().__init__(hp, stamina, speed, hunger, awareness_radius, world_object)
        self.infection_probability = infection_probability
        self.id = "zombie" + str(self._counter)

    def get_id(self):
        return self.id

    def get_nearest_human_position(self):
        tree, coordinate_list = self.world_object.get_all_human_coordinates()
        distance, index = tree.query(self.get_coordinates())
        human = self.world_object.humans[index]
        return human, coordinate_list[index]

    
    def human_nearby(self):
        human, human_coords = self.get_nearest_human_position()
        if human is None:
            return False
        if self.within_radius(self.get_coordinates(), human_coords, self.awareness_radius):
            return True

    def update_behavior(self):
        if self.hp <= 0:
            self.world_object.delete_zombie(self)
            return

        human, human_coords = self.get_nearest_human_position()
        if human and self.within_radius(self.get_coordinates(), human_coords, self.awareness_radius):
            if self.get_coordinates() == human_coords:
                human.take_damage(20)
            else:
                direction = self.calculate_compass_direction(self.get_coordinates(), human_coords)
                self.move(direction)
        else:
            random_direction = random.choice(["N","S","W","E","NW","NE","SW","SE"])
            self.move(random_direction)


