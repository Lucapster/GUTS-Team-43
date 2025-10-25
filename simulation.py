import math

def set_grid(row, col):
    world = world(row, col)

def set_buildings(num_camp, num_supermarkets):
    for i in range(num_camp):
        world.add_camp()

    for i in range(num_supermarkets):
        world.add_supermarket()
   
def custom_human(hp, stamina, speed, awareness_radius):
    human1 = human(
        hp = 10 + hp,
        stamina = 2 + stamina,
        speed = 1 + speed,
        awareness_radius = 1 + awareness_radius,
        hunger = 0
        )
    world.add_human(human1)

def custom_zombie(hp, stamina, speed, awareness_radius, infection):
    zombie1 = zombie(
        hp = 10 + hp,
        stamina = 2 + stamina,
        speed = 1 + speed,
        awareness_radius = 1 + awareness_radius,
        infection = 5 + infection,
        hunger = 0
        )
    world.add_zombie(zombie1)

def set_characters(num_humans, num_zombies):
    for i in range(num_humans - 1):
        world.add_human()
    
    for i in range(num_zombies - 1):
        world.add_zombie()

day = 0
dead = {}

def start_simulation():
    human_location, zombie_location = {} , {}
    for i in world.humans().id:
        human_location[i] = i.position()
    for j in world.zombies().id:
        zombie_location[j] = j.position()

    #need the human and zombie list here- so values in the while can be gotten here
    while world.human_count() > 0 and world.zombie_count() > 0:
        for infected in world.humans():
            if infected.is_infected == True
                world.add_zombie(infected) #adds new zombie from human
                world.deactivate_human(infected) #deactivates human based on id
        #if at same location
        seen = []
        for i in human_location.values:
            if i in zombie_location.values and i not in seen :
                human_id, zombie_id = [], []
                for id, location in human_location.items():
                    if location == i:
                        human_id.append(id)
                for id, location in zombie_location.items():
                    if location == i:
                        zombie_id.append(id)
                seen.append(i)
        action(human_id, zombie_id) #returns lists of id position pairs; the stat values are gonna be changed globally?

        #if human at supermarket
        market_list = []
        for i in human_location.values:
             if i not in seen and i in supermarket.position():
                human_id = []
                for id, location in human_location.items():
                    if location == i:
                        human_id.append(id)
                market_list.append(human_id)
                seen.append(i)
        #takes values from outer variables in the div
        market(market_list, day%1)

        #if only humans or zombies
        human_list = []
        for id, val in human_location.items():
            if val not in seen:
                human_list.append(id)

        zombie_list = []
        for id, val in zombie_location.items():
            if val not in seen:
                zombie_list.append(id)
        #takes values from outer variables in the div
        movement(human_list, zombie_list, day%1) 

        #floor of float for day number
        #if day%1 == 0 -> day; if day%1 == 0.5 -> night
        day += 0.5
    show_results()

def action (human_id, zombie_id):
    human_objects = [humans[id] for id in human_id]
    zombie_objects = [zombies[id] for id in zombie_id]

    entities = human_id + zombie_id
    sorted_entities = sorted(entities, key=lambda id: (
        humans.get(id).speed if id in human_id else zombies.get(id).speed
    ), reverse = True)
    
    sorted_objects = [
    humans[id] if id in human_id else zombies[id]
    for id in sorted_entities
    ]

    in_camp = True if human_location[human_id[1]] in camp.getid() else False
    add_chance = (len(human_id)-len(zombie_id))*5

    for entity in sorted_objects:
        if isinstance(entity, humans):
            hz_list = human_zombie(entity, add_chance, in_camp, zombie_objects)#run away or attack; list of objects human and zombie(if attacked)
            entity = hz_list[0]
            if len(hz_list)>0 and hz_list[1].hp>0:
                zombies[hz_list.getid()] = hz_list[1] #change global object zombie with id "id of zombie from list" to zombie object from list
            else:
                dead[hz_list.getid()] = math.floor(day) #id and day of death of zombie
                world.dactivate_zombie(hz_list.getid()) #deactivate zombie based on id
        else:
            zh_list = zombie_human(entity, human_objects)#what zombie do
            entity = zh_list[0]
            if len(zh_list)>0 and zh_list[1].hp>0:
                humans[zh_list.getid()] = zh_list[1]
            else:
                dead[zh_list.getid()] = math.floor(day)
                if (zh_list[1].infected == True):
                    world.add_zombie(zh_list[1]) #adds new zombie from human
                world.deactivate_human(zh_list[1]) #deactivates human based on id


def market (market_list, day_night):
    humans, zombies = market_list[0], market_list[1]
    #what happens with x humans and y zombies
    #end simulation when one side is eliminated
    li = []# returns lists of lists with stats of each human + store products
    return li

def movement (human_list, zombie_list, day_night):
    #same time movement from humans and zombies
    #independent unless they detect each other
    li = []# returns lists of lists with stats and positions of each human/zombie
    return li

def show_results():
    return

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