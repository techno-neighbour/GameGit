import time 
import threading
import random as rd
from settings import g_func  

ss = g_func()

n = rd.choice(list(ss.note.keys()))
nk = ss.note[n]
rv = list(ss.rooms.values())
sk, sg, sp = rd.sample(rv, 3), rd.sample(rv, 3), rd.sample(rv, 2)
nt, nl = rd.choice(rv), rd.choice(rv)

while nt == nl:
    nt, nl = rd.choice(rv), rd.choice(rv)

for room in sp:
    room['item'] = 'potion'
for room in sk:
    room['item'] = 'key'
for room in sg:
    room.update({'ghost': True, 'attacked': False})

nt['item'] = 'note'
nl.update({'locked': True, 'password': str(n)})

ss.rooms.update({
    'Door': {'west': 'Foyer'},
    'Hall': {'south': 'Hallway', 'east': 'Foyer', 'west': 'Library', 'north': 'Shrine'},
    'Hallway': {'north': 'Hall', 'east': 'Kitchen', 'south': 'Guestroom', 'west': 'Bedroom'}
})

inventory = {}
health = 100
time_up = False
time_limit = 301
print(nl)
print("""
                            TEXT-BASED ESCAPE GAME
    =====================================================================
     You are a student who recently moved into a house as a paying guest.
     During your stay, you find your patron acting very strangely. Before
     you can find anything, you are trapped inside the house. You have 10 
     minutes to escape, or else you will be gunned down by the patron.
    ---------------------------------------------------------------------""")
time.sleep(8)
print("""
    GAME OBJECTIVE:
    Find 3 keys, avoid the ghosts, and escape before the timer runs out!
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

def countdown_timer():
    global time_up
    start = time.time()
    while time.time() - start < time_limit:
        time.sleep(1)
    time_up = True

threading.Thread(target=countdown_timer, daemon=True).start()

def status():
    time.sleep(1)
    print(f"Current location: {ss.current_room}\nCurrent health: {ss.health}")
    if ss.health <= 20:
        print("Warning: Your health is low!")

while not time_up:
    status()

    if ss.check_locked_room(ss.current_room):
        continue

    room_data = ss.rooms[ss.current_room]

    if 'item' in room_data:
        print(f"You see a {room_data['item']} here.")

    if room_data.get('ghost') and not room_data['attacked']:
        if ss.ghost():
            break
        ss.health = ss.give_health()
        room_data['attacked'] = True

    time.sleep(1)
    command = input("\nWhat's your move? ").lower().split()
    if not command:
        continue

    if time_up:
        ss.f()
        break

    action = command[0]

    if action == 'quit':
        print("You chose to die! May your soul be at peace.")
        break

    elif action == 'inventory':
        potions = ss.inventory.get('potion', 0)
        keys = ss.inventory.get('key', 0)
        print(f"\nYour inventory: {ss.inventory} (Keys: {keys}) (Potions: {potions})")

    elif action == 'move' and len(command) > 1:
        direction = command[1]
        if direction in room_data:
            if 'ghost' in room_data:
                room_data['attacked'] = False

            if ss.current_room == 'Foyer' and direction == 'east' and ss.inventory.get('key', 0) < ss.required_keys:
                print("\nThe Door won't open! You need all 3 keys.")
            else:
                ss.current_room = room_data[direction]
                print(f"You moved to the {ss.current_room}.")
        else:
            print("You can't go that way!\n")

    elif action == 'read' and len(command) > 1 and command[1] == 'note':
        if ss.inventory.get('note', 0) > 0:
            print(f"The note reads: '{nk}'")
        else:
            print("You don't have a note.")

    elif action == 'collect' and len(command) > 1:
        item = command[1]
        if room_data.get('item') == item:
            ss.inventory[item] = ss.inventory.get(item, 0) + 1
            print(f"You picked up a {item}.")
            if item == 'note':
                print(f"The note reads: '{nk}'")
            del room_data['item']
        else:
            print(f"There's no {item} here.")

    elif action == 'use' and len(command) > 1 and command[1] == 'potion':
        ss.use_potion()

    else:
        print('Invalid command. Please enter a valid direction, item, or action.')

    if ss.current_room == 'Door' and ss.inventory.get('key', 0) == ss.required_keys:
        print("\nYou have made it to the exit and start to run. ", end='', flush=True)
        time.sleep(2)
        print('While you run, you start to think, ', end='', flush=True)
        time.sleep(2.5)
        print("'Why were there ghosts in the house?'", end='', flush=True)
        time.sleep(2.5)
        print(" That's when you realize...", flush=True)
        time.sleep(3)
        break
else:
    ss.f()
