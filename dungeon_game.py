from __future__ import print_function

import logging
import os 
import random

logging.basicConfig(filename='game.log', level=logging.DEBUG)

dungeon_name = "DUNGEON OF DOOM!"

dungeon_height = 6
dungeon_width = 6

monster_sleep = 6

cells = []
rooms_visited = []

# Generate coordinates for dunction
dh = 0
while dh < dungeon_height:
    dw = 0
    while dw < dungeon_width:
        cells.append((dh, dw))
        dw += 1
    dh += 1


def clear_screen():
    os.system('clear')


def get_locations():
    rooms_to_place = cells[:]

    monster = random.choice(rooms_to_place)
    rooms_to_place.remove(monster)
    door = random.choice(rooms_to_place)
    rooms_to_place.remove(door)
    start = random.choice(rooms_to_place)  # Call start player externally
    rooms_to_place.remove(start)
    xpool = random.choice(rooms_to_place)
    rooms_to_place.remove(xpool)
    ypool = random.choice(rooms_to_place)

    return monster, door, start, xpool, ypool


def move_monster(player, monster):
    x, y = monster
    if player[0] < monster[0]:
        x = monster[0] - 1
    elif player[0] > monster[0]:
        x = monster[0] + 1
    elif player[1] < monster[1]:
        y = monster[1] - 1
    elif player[1] > monster[1]:
        y = monster[1] + 1

    return x, y


def move_player(player, move):
    x, y = player
    if move == 'LEFT':
        y -= 1
    elif move == 'RIGHT':
        y += 1
    elif move == 'UP':
        x -= 1
    elif move == 'DOWN':
        x += 1
    return x, y


def get_moves(player):
    moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']

    if player[0] == dungeon_height - 1:
        moves.remove('DOWN')

    if player[0] == 0:
        moves.remove('UP')

    if player[1] == dungeon_width - 1:
        moves.remove('RIGHT')

    if player[1] == 0:
        moves.remove('LEFT')

    return moves


def draw_map(player):
    clear_screen()
    print(dungeon_name)
    print("")

    print(' _' * dungeon_width)

    tile = '|{}'

    for idx, cell in enumerate(cells):
        # if idx in [0, 1, 3, 4, 6, 7]:
        if (idx + 1) % dungeon_width != 0:
            if cell == player:
                print(tile.format('X'), end='')
            else:
                if cell in rooms_visited:
                    print(tile.format('*'), end='')
                else:
                    print(tile.format('_'), end='')
        else:
            if cell == player:
                print(tile.format('X|'))
            else:
                if cell in rooms_visited:
                    print(tile.format('*|'))
                else:
                    print(tile.format('_|'))

    print('')
    print(message)
    print("")

monster, door, player, xpool, ypool = get_locations()
logging.info('monster: {}; door: {}; player: {};'.format(
  monster, door, player))

message = "Welcome to {}!".format(dungeon_name.upper())

# MAIN GAME LOOPS
while True:
    message = ""
    moves = get_moves(player)

    # If the player has moved to more room than the monster sleep,
    # the monster wakes up and will move 50% of the time!
    if monster_sleep < len(rooms_visited) and random.randint(0, 1) == 1:
        monster = move_monster(player, monster)
    elif monster_sleep == len(rooms_visited):
        message = "You hear something stirring in the distance..."

    if player not in rooms_visited:
        rooms_visited.append(player)

    draw_map(player)

    # TEMP
    # print(player)
    # print(monster)

    # Checks to see if the monster caught up with the player!
    if player == monster:
        message = "You were eaten by the Gru!"
        draw_map(player)
        break

    print("You can move {} or enter QUIT to quit".format(moves))

    move = input("> ")
    move = move.upper()

    if move == 'QUIT':
        break

    if move in moves:
        player = move_player(player, move)
    else:
        message = "** Walls are hard, stop walking into them! **"
        continue

    if player == door:
        message = "You escaped the {}!".format(dungeon_name)
        draw_map(player)
        break
    elif player == ypool:
        message = "A booming voice speaks! 'The exit lies somewhere"
        " in column {}'!.".format(door[1] + 1)
    elif player == xpool:
        message = "A soft voice whispers. 'The exit can be found"
        " in row {}'.".format(door[0] + 1)

    # If it's a good move, change the player's position
    # If it's a bad move, don't change anything
    # If the new player position is the door, they win!
    # If the new player position is the monster, they lose!
    # Otherwise, continue
