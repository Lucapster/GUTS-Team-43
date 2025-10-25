class Zombie(MovingEntity):
    def __init__(self,hp,infection_probability):
        super().__init__(self,stamina,speed,hunger,awareness_radius)
        self.hp = hp
        self.infection_probability=infection_probability

    def move(self, direction):
        if direction == "up":
            self.position[0] += self.speed
        elif direction == "down":
            self.position[0] -= self.speed
        elif direction == "left":
            self.position[1] -= self.speed
        elif direction == "right":
            self.position[1] += self.speed
        return self.position

self.awareness_radius_Z=10
self.aggression=self.strength*self.speed

adam=Zombie("NightZombie",100,3,8,100,10,self.aggression,self.selfawareness_radius)

Shamir=Zombie("NightZombie",100,3,8,100,10,self.aggression,self.awareness_radius)


Charlie=Zombie("DaysZombie",100,3,8,100,10,self.aggression,self.awareness_radius)

#Change of speed depending on time
Time_of_The_Day=""
        def update_speed(self, Time_of_The_Day):
            if self.TypeOfZ=="DaysZombie" and Time_of_The_Day=="Night":
                self.speed=self.speed*0.5
            elif self.TypeOfZ=="NightZombie" and Time_of_The_Day=="Day":
                self.speed=self.speed*0.5



