import random

class human(GridEntity):
    def __init__(self, stamina, speed, hunger, position, awareness):
        super().__init__(stamina, speed, hunger, position)
        self.awareness = awareness
    
    def consume_food(self, food):
        self.hunger += food
   
    def sleep(self):
        self.stamina = 100

    def hunger_damage(self):
        if self.hunger <= 0:
            self.hp -= 10

    def move(self):
        self.stamina -= self.speed

    

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
            
        
