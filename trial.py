import time 
import threading
import random as rd
from settings import g_func  # type: ignore
ss = g_func()

n = (rd.choice(list(ss.note.keys())))
nk = ss.note[n]
rv=list(ss.rooms.values())
sk = rd.sample(rv,3) # keys
sg = rd.sample(rv,3) # ghost
sp = rd.sample(rv,2) # potion
nt , nl= rd.choice(rv), rd.choice(rv) # note, password
while True: # takes care so that note doesn't fall in locked room
    if nt == nl:
        nt, ns= rd.choice(rv), rd.choice(rv)
    else:
        break
for a in sp:
    a.update({'item':'potion'})
for i in sk:
    i.update({'item':'key'})
for j in sg:
    j.update({'ghost':True,'attacked': False})
nt.update({'item': 'note'})
nl.update({'locked': True, 'password': str(n)})
print("note:",nt,"\nlocked:",nl,"\nghost:",sg)
ss.rooms.update({'Door': {'west': 'Foyer'}})
ss.rooms.update({'Hall': {'south': 'Hallway', 'east': 'Foyer', 'west': 'Library','north': 'Shrine'}})

inventory = {}
current_room = 'Hall'
health = 100
required_keys = 3
max_password_attempts = 5
time_up = False
time_limit = 301

print("""
                            TEXT-BASED ESCAPE GAME
    =====================================================================
     You are a student who recently moved into a house as a paying guest.
     In your stay, you find your Patron to act very strange. Before you
     can find anything , you are trapped inside the house. You have 10 
     minutes to escape , or you will be gunned down by the patron.
    ---------------------------------------------------------------------""")
time.sleep(3)
print("""\n    GAME OBJECTIVE:
    Find 3 keys, avoid the ghosts, and unlock the exit before to win!
    ----------------------------------------------------------------------  """, end='')
time.sleep(3)

print("""
    COMMANDS:
    'move [direction]' - move around (north, south, east, west)
    'collect [item]' - collect the item in the room
    'use potion' - heal yourself using a potion
    'read note' - reads the note you've collected
    'inventory' - see what you've collected
    'quit' - leave the game
""")
time.sleep(2)
def countdown_timer(): # for the timer
    global time_up
    start_time = time.time()
    while time.time() - start_time < time_limit:
        time.sleep(1)  # wait for 1 second
    time_up = True  # time is up

# start the countdown timer in a separate thread
timer_thread = threading.Thread(target=countdown_timer)

def status():  # for health and location
        time.sleep(1)
        print(f"Current location: {current_room}")
        print(f"Current health: {health}")
        if health <= 20:
            print("Warning: Your health is low!")
timer_thread.start()
#                                  GAME PLAY CODE                                GAME PLAY CODE
while not time_up:
    status()

    if ss.check_locked_room(current_room):
        continue

    if 'item' in ss.rooms[current_room]:
        print(f"You see a {ss.rooms[current_room]['item']} here.")
    
    if 'ghost' in ss.rooms[current_room] and not ss.rooms[current_room]['attacked']:
        if ss.ghost():
            break
        ss.rooms[current_room]['attacked'] = True  # mark the room as "ghost attacked"

    time.sleep(1)
    command = input("\nWhat's your move? ").lower().split()
    if len(command) < 1:
        if command[0] != 'inventory' and command[0] != 'quit':
            while len(command) < 2:
                print('Invalid command. Please enter a valid direction, item, or action.')
                time.sleep(1)
                command = input("What's your move? ").lower().split()
    if time_up:
        ss.f()
        break
    if command[0] == 'quit':
        time.sleep(1)
        print("You chose to die! May your soul be at peace.")
        time.sleep(1)
        break

    elif command[0] == 'inventory':
        time.sleep(1)
        potions_count = ss.inventory.get('potion', 0)
        potions_info = f"(Potions available: {potions_count})" if potions_count > 0 else ""
        keys_collected = f"(Keys collected: {ss.inventory['key']})" if 'key' in ss.inventory and ss.inventory['key']>0 else ""
        print(f"\nYour inventory: {ss.inventory} {keys_collected} {potions_info}")

    elif command[0] == 'move':
        time.sleep(1)
        if command[1] in ss.rooms[current_room]:
            # reset's the ghost attack status when leaving the current room
            if 'ghost' in ss.rooms[current_room]:
                ss.rooms[current_room]['attacked'] = False

            if (current_room == 'Foyer' and command[1] == 'east') and ss.inventory.get('key', 0) < ss.required_keys:
                print("\nThe Door won't open! You need all 3 keys.")
            else:
                current_room = ss.rooms[current_room][command[1]]
                print(f"You moved to the {current_room}.")
        else:
            print("You can't go that way!\n")

    elif command[0] == 'read':
        time.sleep(1)
        if command[1] == 'note':
            if 'note' in ss.inventory and ss.inventory['note'] > 0:
                print(f"The note reads: '{nk}'")
            else:
                print("You don't have a note.")
        else:
            print(f"You cannot read '{command[1]}'.")

    elif command[0] == 'collect':
        time.sleep(1)
        if 'item' in ss.rooms[current_room] and ss.rooms[current_room]['item'] == command[1]:
            if command[1] not in ss.inventory:
                ss.inventory.update({command[1]: 1})
            else:
                ss.inventory[command[1]] += 1
            print(f"You picked up a {command[1]}.")
            if command[1] == 'note':
                print(f"The note reads: '{nk}'")
            del ss.rooms[current_room]['item']
        else:
            print(f"There's no {command[1]} here.")


    elif command[0] == 'use' and command[1] == 'potion':
        ss.use_potion()

    else:
        time.sleep(1)
        print('Invalid command. Please enter a valid direction, item, or action.')

    if current_room == 'Door' and 'key' in ss.inventory:
        if ss.inventory['key'] == ss.required_keys:
            time.sleep(1)
            print("\nYou have made it to the exit and start to run. ", flush=True,end='')
            time.sleep(2)
            print('While you run, you start to think, ', flush=True,end='')
            time.sleep(2.5)
            print("'Why were there ghosts in the house?'", flush=True,end='') 
            time.sleep(2.5)
            print(" That's when you realize", flush=True,end='')
            time.sleep(1)
            print('.', flush=True,end='')
            time.sleep(1)
            print('.', flush=True,end='')
            time.sleep(1)
            print('.', flush=True,end='')
            time.sleep(1)
            print('')
            break
else:
    ss.f()