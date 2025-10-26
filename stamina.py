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
    world.humans.append(human1)
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
    world.zombies.append(zombie1)
    return zombie1

def set_characters(num_humans, num_zombies):
    global world
    for i in range(num_humans):
        world.add_human()
    
    for i in range(num_zombies):
        world.add_zombie()

day = 0
dead = {}

def start_simulation():
    global day
    
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
                world.zombies.append(new_zombie)

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

        if len(world.humans) == 0 or len(world.zombies) == 0:
            break

        max_stamina = max(
            [h.stamina for h in world.humans] + 
            [z.stamina for z in world.zombies]
        )
        
        current_stamina_turn = 1
        while current_stamina_turn <= max_stamina:
            human_location, zombie_location = update_positions()
            seen_locations = []
            
            active_humans = [h for h in world.humans if h.stamina >= current_stamina_turn]
            active_zombies = [z for z in world.zombies if z.stamina >= current_stamina_turn]
            
            if not active_humans and not active_zombies:
                break
            
            human_active_locations = {i: human_location[i] for i, human in enumerate(world.humans) if human in active_humans}
            zombie_active_locations = {i: zombie_location[i] for i, zombie in enumerate(world.zombies) if zombie in active_zombies}
            
            seen = []
            for location in human_active_locations.values():
                if location in zombie_active_locations.values() and location not in seen:
                    human_objects, zombie_objects = [], []
                    for entity_id, loc in human_location.items():
                        if loc == location and entity_id < len(world.humans) and world.humans[entity_id] in active_humans:
                            human_objects.append(world.humans[entity_id])
                    for entity_id, loc in zombie_location.items():
                        if loc == location and entity_id < len(world.zombies) and world.zombies[entity_id] in active_zombies:
                            zombie_objects.append(world.zombies[entity_id])
                    seen.append(location)
                    if human_objects and zombie_objects:
                        action(human_objects, zombie_objects, current_stamina_turn)

            human_objects_market = []
            supermarket_positions = [supermarket.get_coordinates() for supermarket in world.supermarkets]

            for location in human_active_locations.values():
                 if location not in seen and location in supermarket_positions:
                    for entity_id, loc in human_location.items():
                        if loc == location and entity_id < len(world.humans) and world.humans[entity_id] in active_humans:
                            human_objects_market.append(world.humans[entity_id])
                    seen.append(location)
            if human_objects_market:
                market(human_objects_market, location, day%1, current_stamina_turn)

            human_lone_objects = []
            for entity_id, coords in human_active_locations.items():
                if coords not in seen and entity_id < len(world.humans) and world.humans[entity_id] in active_humans:
                    human_lone_objects.append(world.humans[entity_id])

            zombie_lone_objects = []
            for entity_id, coords in zombie_active_locations.items():
                if coords not in seen and entity_id < len(world.zombies) and world.zombies[entity_id] in active_zombies:
                    zombie_lone_objects.append(world.zombies[entity_id])
                    
            if human_lone_objects or zombie_lone_objects:
                movement(human_lone_objects, zombie_lone_objects, day%1, current_stamina_turn)

            current_stamina_turn += 1

        day += 0.5

        for human in world.humans:
            if human.hunger < 10:
                human.hunger += 1
    
        for zombie in world.zombies:
            if zombie.hunger < 10:
                zombie.hunger += 1

    return show_results()

def update_positions():
    human_location = {}
    zombie_location = {}
    
    for i, human in enumerate(world.humans):
        human_location[i] = human.get_coordinates()
     
    for j, zombie in enumerate(world.zombies):
        zombie_location[j] = zombie.get_coordinates()
    
    return human_location, zombie_location

def action(human_objects, zombie_objects, stamina_turn):
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
            hz_list = human_zombie(entity, add_chance, in_camp, zombie_objects)
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

def market(human_objects, market_location, day_night, stamina_turn):
    supermarket_obj = None
    for supermarket in world.supermarkets:
        if supermarket.get_coordinates() == market_location:
            supermarket_obj = supermarket
            break

    if supermarket_obj:
        sorted_humans = sorted(human_objects, key=lambda obj: obj.speed, reverse=True)
        for human in sorted_humans:
            human_market(human, supermarket_obj)

def human_market(human, supermarket):
    food_needed = human.hunger
    food_taken = min(food_needed, supermarket.food_available)
    human.hunger -= food_taken
    supermarket.food_available -= food_taken

def movement(human_lone_objects, zombie_lone_objects, day_night, stamina_turn):
    for human in human_lone_objects:
        human_move(human, day_night)
    for zombie in zombie_lone_objects:
        zombie_move(zombie, day_night)

def show_results():
    humans_won = len(world.humans) > 0
    
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