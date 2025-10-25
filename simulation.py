#get inputs from UI text fields
#UI calls my functions

#get grid size
def set_grid(row, col):
    #row = int(row_field.get_input())
    #col = int(column_field.get_input())
    world = world(row,  col)

#get apartment and supermarket counts
def set_buildings(num_apartments, num_supermarkets):
    #num_apartments = int(num_apartments_field.get_input())
    for i in range(num_apartments):
        world.add_apartment()

    #num_supermarkets = int(num_supermarkets_field.get_input())
    for i in range(num_supermarkets):
        world.add_supermarket()
   
#get human and zombie counts
#if only 1 param -> human and zombie functions need random adding up to 10
def set_characters(num_humans, num_zombies):
    #num_humans = int(num_humans_field.get_input())
    for i in range(2, num_humans + 1):
        world.add_human(id = i)
    
    #num_zombies = int(num_zombies_field.get_input())
    for i in range(2, num_zombies + 1):
        world.add_zombie(id = i)
   
#create custom human and zombie
def custom_human(hp, stamina, speed, awareness_radius):
    #hp = int(hp_field1.get_input())
    #stamina = int(stamina_field1.get_input())
    #speed = int(speed_field1.get_input())
    #awareness_radius = int(awareness_radius_field1.get_input())
    human1 = human(
        id = 1,
        hp = 10 + hp,
        stamina = 2 + stamina,
        speed = 1 + speed,
        awareness_radius = 1 + awareness_radius,
        hunger = 0
        )
    world.add_human(human1)

def custom_zombie(hp, stamina, speed, awareness_radius, infection):
    #hp = int(hp_field2.get_input())
    #stamina = int(stamina_field2.get_input())
    #speed = int(speed_field2.get_input())
    #awareness_radius = int(awareness_radius_field2.get_input())
    #infection = float(infection_field2.get_input())
    zombie1 = zombie(
        id = 1,
        hp = 10 + hp,
        stamina = 2 + stamina,
        speed = 1 + speed,
        awareness_radius = 1 + awareness_radius,
        infection = 5 + infection,
        hunger = 0
        )
    world.add_zombie(zombie1)

#start simulation with while loop (while humans > 0 and zombies > 0)
def start_simulation():
    while world.human_count() > 0 and world.zombie_count() > 0:
        #simulation code here
#end simulation when one side is eliminated

'''
base stats
hp = 10 #each stat increases hp by 1
stamina = 2 #each stat increases turns by 1
speed = 1 #each stat increases grid moved by 1 
awareness_radius = 1 #each stat increases detection radius by 1
hunger = 0 #can't increase; hunger 10 =  -1hp/round
#for zombies
infection = 5 #each stat increases infection rate by 0.5 (5%)
'''