from world import MovingEntity


class Zombie(MovingEntity):
    _counter = 0
    def __init__(self, hp, stamina, speed, hunger, awareness_radius, infection_probability, world):
        super().__init__(hp, stamina, speed, hunger, awareness_radius)
        self.infection_probability = infection_probability
        self.world = world
        self.id = "zombie" + _counter

    def get_id(self):
        return self.id

    def update_speed(self, Time_of_The_Day):
        if self.TypeOfZ=="DaysZombie" and Time_of_The_Day=="Night":
            self.speed=self.speed*0.5
        elif self.TypeOfZ=="NightZombie" and Time_of_The_Day=="Day":
            self.speed=self.speed*0.5



