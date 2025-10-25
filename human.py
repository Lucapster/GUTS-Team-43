import random

class Human(MovingEntity):
    def __init__(self, hp, stamina, speed, hunger, awareness_radius):
        super().__init__(hp, stamina, speed, hunger, awareness_radius, food_value)
    
    def consume_food(self, food_value):
        self.hunger += self.food_value
   
    def sleep(self):
        self.stamina = 100

    

