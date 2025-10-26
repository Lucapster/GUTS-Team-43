import math
from world import WorldGrid, Human, Zombie, Supermarket, HumanCamp

world = None

def set_grid(row, col):
    global world
    world = WorldGrid(row, col)
    return world

def set_buildings(num_camp, num_supermarkets):
    global world
    for i in range(num_camp):
        world.add_human_camp(capacity=10)

    for i in range(num_supermarkets):
        world.add_supermarket(food_available=100)
   
def custom_human(hp, stamina, speed, awareness_radius):
    global world
    human1 = Human(
        hp = 10 + hp,
        stamina = 2 + stamina,
        speed = 1 + speed,
        awareness_radius = 1 + awareness_radius,
        hunger = 0,
        world_object=world
    )
    world.add_ready_human(human1)
    return human1

def custom_zombie(hp, stamina, speed, awareness_radius, infection):
    global world
    zombie1 = Zombie(
        hp = 10 + hp,
        stamina = 2 + stamina,
        speed = 1 + speed,
        awareness_radius = 1 + awareness_radius,
        infection_probability=(50 + infection*5) / 100,
        hunger = 0,
        world_object=world
    )
    world.add_ready_zombie(zombie1)
    return zombie1

def set_characters(num_humans, num_zombies):
    global world
    for i in range(num_humans - 1):
        world.add_human()
    
    for i in range(num_zombies - 1):
        world.add_zombie()

day = 0
dead = {}

def start_simulation():
    global day
    human_location, zombie_location = {}, {}

    for i, human in enumerate(world.humans):
            human_location[i] = human.get_coordinates()
        
    for j, zombie in enumerate(world.zombies):
        zombie_location[j] = zombie.get_coordinates()

    while len(world.humans) > 0 and len(world.zombies) > 0:
        entities_to_remove = []
        
        for human in world.humans:
            if human.hunger >= 10:
                human.hp -= 1 
                if human.hp <= 0:
                    dead[f"human_{id(human)}"] = {
                        'day_of_death': math.floor(day),
                        'type': 'starved_to_death',
                        'final_stats': {
                            'hp': human.hp,
                            'stamina': human.stamina,
                            'speed': human.speed,
                            'hunger': human.hunger
                        },
                        'position': human.get_coordinates()
                    }
                    entities_to_remove.append(human)
        
        for zombie in world.zombies:
            if zombie.hunger >= 10:
                zombie.hp -= 1 
                if zombie.hp <= 0:
                    dead[f"zombie_{id(zombie)}"] = {
                        'day_of_death': math.floor(day),
                        'type': 'starved_to_death',
                        'final_stats': {
                            'hp': zombie.hp,
                            'stamina': zombie.stamina,
                            'speed': zombie.speed,
                            'hunger': zombie.hunger
                        },
                        'position': zombie.get_coordinates()
                    }
                    entities_to_remove.append(zombie)
        
        for entity in entities_to_remove:
            if entity in world.humans:
                world.humans.remove(entity)
            elif entity in world.zombies:
                world.zombies.remove(entity)
        
        if len(world.humans) == 0 or len(world.zombies) == 0:
            break
        
        #infected humans becomes zombies
        humans_to_remove = []
        for human in world.humans:
            if hasattr(human, 'is_infected') and human.is_infected:

                new_zombie = Zombie(
                    hp=human.hp, 
                    stamina=human.stamina, 
                    speed=human.speed, 
                    hunger=human.hunger,
                    awareness_radius=human.awareness_radius,
                    infection_probability=0.5,
                    world_object=world
                )

                world.add_ready_zombie(new_zombie)

                dead[f"human_{id(human)}"] = {
                    'day_of_death': math.floor(day),
                    'type': 'infected_turned_zombie',
                    'final_stats': {
                        'hp': human.hp,
                        'stamina': human.stamina,
                        'speed': human.speed,
                        'hunger': human.hunger,
                        'awareness_radius': human.awareness_radius
                    },
                    'position': human.get_coordinates(),
                    'turned_into_zombie_id': id(new_zombie)
                }
                    
                humans_to_remove.append(human)
        
        for human in humans_to_remove:
            world.humans.remove(human)

        human_location, zombie_location = update_positions()
        seen_locations = []
            
        #if at same location
        seen = []
        for i in human_location.values():
            if i in zombie_location.values() and i not in seen :
                human_objects, zombie_objects = [], []
                for id, location in human_location.items():
                    if location == i and id<len(world.humans):
                        human_objects.append(world.humans[id])
                for id, location in zombie_location.items():
                    if location == i and id<len(world.zombies):
                        zombie_objects.append(world.zombies[id])
                seen.append(i)
                action(human_objects, zombie_objects)

        #if human at supermarket
        human_objects_market = []
        supermarket_position = [supermarket.get_coordinates() for supermarket in world.supermarkets]

        for i in human_location.values():
             if i not in seen and i in supermarket_position:
                for id, location in human_location.items():
                    if location == i and id<len(world.humans):
                        human_objects_market.append(world.humans[id])
                seen.append(i)
        market(human_objects_market, i, day%1)

        #if only humans or zombies
        human_lone_objects = []
        for id, coords in human_location.items():
            if coords not in seen and id < len(world.humans):
                human_lone_objects.append(world.humans[id])

        zombie_lone_objects = []
        for id, coords in zombie_location.items():
            if coords not in seen  and id < len(world.zombies):
                zombie_lone_objects.append(world.zombies[id])
                
        movement(human_lone_objects, zombie_lone_objects, day%1)

        #floor of float for day number
        #if day%1 == 0 -> day; if day%1 == 0.5 -> night
        day += 0.5

        for human in world.humans:
            if human.hunger < 10:
                human.hunger += 1
    
        for zombie in world.zombies:
            if zombie.hunger < 10:
                zombie.hunger += 1

    show_results()

def update_positions():
    human_location = {}
    zombie_location = {}
    
    for i, human in enumerate(world.humans):
        human_location[i] = human.get_coordinates()
     
    for j, zombie in enumerate(world.zombies):
        zombie_location[j] = zombie.get_coordinates()
    
    return human_location, zombie_location

def action (human_objects, zombie_objects):
    objects = human_objects + zombie_objects
    sorted_objects = sorted(objects, key=lambda obj: obj.speed, reverse=True)

    camp_coords = [camp.get_coordinates() for camp in world.human_camps]
    in_camp = human_objects[0].get_coordinates() in camp_coords if human_objects else False
    add_chance = (len(human_objects)-len(zombie_objects))*5

    humans_to_remove = []
    zombies_to_remove = []

    for entity in sorted_objects:
        if entity in humans_to_remove or entity in zombies_to_remove:
            continue
        
        if isinstance(entity, Human):
            hz_list = human_zombie(entity, add_chance, in_camp, zombie_objects)#run away or attack; list of objects human and zombie(if attacked)
            entity = hz_list[0]
            if len(hz_list) == 2:
                fought_zombie = hz_list[1]
                if fought_zombie.hp <= 0:
                    dead[f"zombie_{id(fought_zombie)}"] = {
                        'day_of_death': math.floor(day),
                        'type': 'killed_by_human',
                        'final_stats': {
                            'hp': fought_zombie.hp,
                            'stamina': fought_zombie.stamina,
                            'speed': fought_zombie.speed
                        }
                    }
                    zombies_to_remove.append(fought_zombie)
                    if fought_zombie in zombie_objects:
                        zombie_objects.remove(fought_zombie)
        else:
            zh_list = zombie_human(entity, human_objects)
            entity = zh_list[0]
            if len(zh_list) == 2:
                attacked_human = zh_list[1]
                if attacked_human.hp <= 0:
                    if hasattr(attacked_human, 'is_infected') and attacked_human.is_infected:
                        # Human infected
                        dead[f"human_{id(attacked_human)}"] = {
                            'day_of_death': math.floor(day),
                            'type': 'infected_killed',
                            'final_stats': {
                                'hp': attacked_human.hp,
                                'stamina': attacked_human.stamina,
                                'speed': attacked_human.speed
                            }
                        }
                    else:
                        # Human not infected
                        dead[f"human_{id(attacked_human)}"] = {
                            'day_of_death': math.floor(day),
                            'type': 'killed_by_zombie',
                            'final_stats': {
                                'hp': attacked_human.hp,
                                'stamina': attacked_human.stamina,
                                'speed': attacked_human.speed
                            }
                        }
                    
                    humans_to_remove.append(attacked_human)
                    if attacked_human in human_objects:
                        human_objects.remove(attacked_human)

    for human in humans_to_remove:
        if human in world.humans:
            world.humans.remove(human)
    
    for zombie in zombies_to_remove:
        if zombie in world.zombies:
            world.zombies.remove(zombie)

    #human_zombie and zombie_human return the final results of the human and zombie in the action

def market (human_objects, market_location, day_night):
    supermarket_obj = None
    for supermarket in world.supermarkets:
        if supermarket.get_coordinates() == market_location:
            supermarket_obj = supermarket
            break

    sorted_humans = sorted(human_objects, key=lambda obj: obj.speed, reverse=True)

    for human in sorted_humans:
        human_market(human, supermarket_obj)


def movement(human_lone_objects, zombie_lone_objects, day_night):
    for human in human_lone_objects:
        human_move(human, day_night)

    for zombie in zombie_lone_objects:
        zombie_move(zombie, day_night)
    

def show_results():
    humans_won = len(world.humans) > 0
    
    # Separate dead by side with detailed info
    dead_humans = {}
    dead_zombies = {}
    
    for entity_id, death_info in dead.items():
        entity_data = {
            'day_of_death': death_info.get('day_of_death'),
            'type': death_info.get('type'),
            'final_stats': death_info.get('final_stats', {}),
            'position': death_info.get('position')
        }
        
        if 'human' in entity_id:
            dead_humans[entity_id] = entity_data
        elif 'zombie' in entity_id:
            dead_zombies[entity_id] = entity_data
    
    if humans_won:
        return {
            'alive': [{'id': f"human_{i}", 'object': human} for i, human in enumerate(world.humans)],
            'dead_winners': dead_humans,
            'dead_losers': dead_zombies
        }
    else:
        return {
            'alive': [{'id': f"zombie_{i}", 'object': zombie} for i, zombie in enumerate(world.zombies)],
            'dead_winners': dead_zombies,
            'dead_losers': dead_humans
        }

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