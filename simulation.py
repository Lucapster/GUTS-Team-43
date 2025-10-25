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
    day = 0
    human_location, zombie_location = {} , {}
    for i in world.humans().id:
        human_location[i] = i.position()
    for j in world.zombies().id:
        zombie_location[j] = j.position()

    #need the human and zombie list here- so values in the while can be gotten here
    while world.human_count() > 0 and world.zombie_count() > 0:
        #if at same location
        seen, action_list = [], []
        for i in human_location.values:
            if i in zombie_location.values and i not in seen :
                human_id, zombie_id = [], []
                for id, location in human_location.items():
                    if location == i:
                        human_id.append(id)
                for id, location in zombie_location.items():
                    if location == i:
                        zombie_id.append(id)
                #action in one grid
                action_list.append([human_id,zombie_id])
                seen.append(i)
        action(action_list)

        #if human at supermarket
        market_list = []
        for i in human_location.values:
             if position not in seen and position in supermarket.position():
                human_id = []
                for id, location in human_location.items():
                    if location == i:
                        human_id.append(id)
                market_list.append(human_id)
                seen.append(i)
        market(market_list)

        #if only humans or zombies
        human_list = []
        for id, val in human_location.values:
            if val not in seen:
                human_list.append(id)

        zombie_list = []
        for id, val in zombie_location.values:
            if val not in seen:
                zombie_list.append(id)

        movement(human_list, zombie_list)

        for i in world.humans():
            i.take_turn(day%1)

        for i in world.zombies():
            i.take_turn(day%1)
        
        #floor of float for day number
        #if day%1 == 0 -> day; if day%1 == 0.5 -> night
        day += 0.5

    
def action (action_list):
    #what happens with x humans and y zombies
    li = []# returns lists of lists with stats of each character
    return li

def market (market_list):
    #what happens with x humans and y zombies
    #end simulation when one side is eliminated
    li = []# returns lists of lists with stats of each human + store products
    return li

def movement (human_list, zombie_list):
    #same time movement from humans and zombies
    #independent unless they detect each other
    li = []# returns lists of lists with stats and positions of each human/zombie
    return li

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