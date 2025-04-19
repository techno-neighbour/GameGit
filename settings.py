import time
import random as rd

class g_func:
    def __init__(self):
        self.rooms = {
            'Foyer': {'north': 'Sunroom', 'east': 'Door', 'west': 'Hall', 'south': 'Kitchen'},
            'Garden': {'north': 'Backyard', 'west': 'Washroom'},
            'Kitchen': {'west': 'Hallway', 'east': 'Pantry', 'south': 'Dining', 'north': 'Foyer'},
            'Dining': {'north': 'Kitchen', 'east': 'Fireplace', 'south': 'Basement'},
            'Hallway': {'north': 'Hall', 'east': 'Kitchen', 'south': 'Guestroom', 'west': 'Bedroom'},
            'Bedroom': {'east': 'Hallway', 'south': 'Tavern', 'north': 'Library'},
            'Fireplace': {'north': 'Pantry', 'west': 'Dining', 'east': 'Backyard', 'south': 'Washroom'},
            'Washroom': {'east': 'Garden', 'west': 'Basement'},
            'Tavern': {'east': 'Guestroom', 'north': 'Bedroom'},
            'Guestroom': {'north': 'Hallway', 'west': 'Tavern'},
            'Sunroom': {'south': 'Foyer', 'west': 'Shrine'},
            'Library': {'north': 'Observatory', 'east': 'Hall', 'south': 'Bedroom'},
            'Observatory': {'south': 'Library', 'east': 'Shrine'},
            'Pantry': {'west': 'Kitchen', 'south': 'Fireplace'},
            'Shrine': {'south': 'Hall', 'west': 'Observatory'},
            'Basement': {'north': 'Dining', 'east': 'Washroom'},
            'Backyard': {'south': 'Garden', 'west': 'Fireplace'}
        }

        self.note = {
            '1234': 'The way you count, is the way you go out.',
            '2020': 'The year that locked the world down, may unlock your door.',
            '1357': 'The oddity of time is the key to unlocking the unknown.',
            '3141': 'Follow the circle to your path of freedom, but with a constant effort.',
            '1711': "A journey marked one the first and last, but with a week's effort in.",
            '8080': 'Infinity repeats, with and without a belt, but within it, lies your finite path.',
            '3333': 'Infinity divided into pieces, make your choice with thesis.',
            '1010': 'A decade in the dual-bit system, is your algorithm.',
            '2357': 'Small, yet indivisible forces stand in your way to freedom.',
            '9101': 'Everyone can have nine dreams and ten paths but only one destination.',
            '2468': 'Even in multiples, the path is yours to take.',
            '5678': 'Five moves forward, eight steps closer.',
            '4812': "A Cube's character, can decide your fate.",
            '4242': 'The answer lies collinear with the answer to the universe and everything.'
        }

        self.inventory = {}
        self.current_room = 'Hall'
        self.health = 100
        self.required_keys = 3
        self.max_password_attempts = 5
        self.time_up = False

    def f(self):
        print("\nOh no! The patron has found you.", flush=True, end='')
        time.sleep(4)
        print(" He fires three bullet's from his pistol,", flush=True, end='')
        time.sleep(2)
        print(' you manage to dodge two ,', flush=True, end='')
        time.sleep(2)
        print(" but the last one passes through your head.", flush=True, end='')
        time.sleep(2)
        print("\nYou slowly start to black out,", flush=True, end='')
        time.sleep(2)
        print(" as the patron stares at your lifeless body", flush=True, end='')
        time.sleep(2)
        print(", with a wild grin", flush=True, end='')
        time.sleep(2)
        print('.', flush=True, end='')
        time.sleep(1)

    def check_locked_room(self, room, attempts=0):
        if 'locked' in self.rooms[room] and self.rooms[room]['locked']:
            print(f"The {room} is locked.")
            while attempts < self.max_password_attempts:
                password = input(f"Enter the Pin (----): ")
                if password == self.rooms[room].get('password', ''):
                    time.sleep(1)
                    print(f"You've unlocked the {room}!")
                    self.rooms[room]['locked'] = False
                    return False  # Room is now unlocked
                else:
                    time.sleep(1)
                    attempts += 1
                    print(f"Wrong password. {self.max_password_attempts - attempts} attempts left.")
            s = rd.choice(['north', 'south', 'east', 'west'])
            while True:
                if s not in self.rooms[self.current_room]:
                    s = rd.choice(['north', 'south', 'east', 'west'])
                    break
                else:
                    break
            print(f"Too many wrong attempts. You're being sent {s}.")
            current_room = self.rooms[self.current_room][s]
            return True  # Make player do nothing
        return False

    def ghost(self):  # For ghost
        time.sleep(1)
        print('Oh no! A Ghost!')
        print("The ghost attacks!")
        d = {'strong': 40, 'N': 30, 'weak': 10}
        s = rd.choice(list(d.keys()))
        s1 = f' {s} ' if s != 'N' else ' '
        self.health -= d[s]
        health = self.health
        if self.health <= 0:
            print("The ghost has defeated you! You died...")
            return True
        else:
            print(f"You were attacked by a{s1}ghost.\nYour health is now {self.health}.")
        return False

    def use_potion(self):  # For health potion
        time.sleep(1)
        d = {'Super': 40, 'Normal': 30, 'Weak': 10}
        s = rd.choice(list(d.keys()))
        potions_count = self.inventory.get('potion', 0)
        if potions_count > 0 and self.health < 100:
            healing_amount = min(d[s], 100 - self.health)
            self.health += healing_amount
            self.inventory['potion'] -= 1
            s1 = f' {s} ' if s != 'Normal' else ' '
            print(f"You used a{s1}potion. Your health is now {self.health}.")
        elif self.health == 100:
            print("Your health is already full. You can't use a potion now.")
        elif potions_count == 0:
            print("No potions in your inventory!")
