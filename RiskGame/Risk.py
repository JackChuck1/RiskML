import csv
import random
class Player:
    def __init__(self):
        self.territories = []
        self.troopBonus = []
class Tile:
    def __init__(self, continent, adjacent):
        self.continent = continent
        self.adjacent = adjacent
        self.owner = -1
        self.troops = 0
    def __str__(self):
        return f"Owned by: {self.owner}\nTroops Present: {self.troops}"

#loads a csv file of all territory relationships
#used for ease of access
def readGameInfo(file:__file__):
    gameInfo = csv.reader(file)
    game = {}
    for line in gameInfo:
        if line[0] == "Territory":
            continue
        #Index 0: Name, Index 1: Continent, Index 2-End: Adjacent Tile Names
        game[line[0]] = Tile(line[1],line[2:])
    return game

#returns an array of 2 player objects
def randomizeOwnership(game, teams):
    teamMax = [42//teams] * teams
    players = [Player(), Player()]
    for tile in game:
        rand = random.randint(0,teams-1)
        while teamMax[rand] == 0:
            rand = random.randint(0,teams-1)
        teamMax[rand] -= 1
        game[tile].owner = rand
        game[tile].troops = 1
        players[rand].territories += [tile]
    return players

def randomizeTroops(game, players):
    for player in players:
        #troops = 40 - amount already placed
        troops = 40 - 21
        while not troops == 0:
            game[player.territories[random.randint(0,20)]].troops += 1
            troops -= 1

#name1 attacks name2
def attackTerritory(game, name1, name2):
    if(name2 in game[name1].adjacent and game[name1].troops > 1):
        attackRolls = [random.randint(0,6), random.randint(0,6)]
        if game[name2].troops == 2:
            defenseRolls = [random.randint(0,6), random.randint(0,6)]
        else:
            defenseRolls = [random.randint(0,6), random.randint(0,6), random.randint(0,6)]
        while game[name2].troops > 0 and game[name1].troops > 1 and len(attackRolls) != 0:
            if max(attackRolls) > max(defenseRolls):
                game[name2].troops -= 1
                print(f"Attacker win: {game[name1].troops}, {game[name2].troops}")
            elif max(attackRolls) < max(defenseRolls):
                game[name1].troops -= 1
                print(f"Defender Win: {game[name1].troops}, {game[name2].troops}")
            else:
                game[name1].troops -= 1
                game[name2].troops -= 1
                print(f"Tie: {game[name1].troops}, {game[name2].troops}")
            attackRolls.remove(max(attackRolls))
            defenseRolls.remove(max(defenseRolls))
    if game[name2].troops == 0:
        game[name2].troops = game[name1].troops - 1
        game[name2].owner = game[name1].owner
        players[game[name1].owner].territories.append(name2)
        players[game[name2].owner].territories.remove(name2)
        game[name1]. troops = 1
        print(f"{name1} has beaten {name2}, {game[name2].troops} remain")

def calculateBonus(game, player):
    troops = len(player.territories)//3
    counts = [0, 0, 0, 0, 0, 0]
    for territory in player.territories:
        if game[territory].continent == "North_America":
            counts[0] += 1
        elif game[territory].continent == "South_America":
            counts[1] += 1
        elif game[territory].continent == "Africa":
            counts[2] += 1
        elif game[territory].continent == "Asia":
            counts[3] += 1
        elif game[territory].continent == "Oceania":
            counts[4] += 1
        elif game[territory].continent == "Europe":
            counts[5] += 1
    if counts[0] == 9:
        troops += 5
    elif counts[1] == 4:
        troops += 2
    elif counts[2] == 6:
        troops += 3
    elif counts[3] == 12:
        troops += 7
    elif counts[4] == 4:
        troops += 2
    elif counts[5] == 7:
        troops += 5
    return troops

def placeTroops(game, name, num):
    game[name].troops += num

#Utility method
def printGame(game):
    for tile in game:
        print(f"{tile}: {game[tile]}")

#Utility method
def countTroops(game):
    troops = [0,0]
    for tile in game:
        troops[game[tile].owner] += game[tile].troops
    return troops

game = readGameInfo(open("GameInfo.csv", "r"))
players = randomizeOwnership(game, 2)
randomizeTroops(game, players)
printGame(game)
print()
turn = 0
while len(players[0].territories) > 0 and len(players[1].territories) > 0:
    playerTurn = turn % 2
    troops = calculateBonus(game, players[playerTurn])
    name = input(f"You have {troops} troops, where would you like the place them")
    placeTroops(game, name, troops)
    print("Make your move")
    move = [input("Choose an attacking territory"), input("Choose a defending territory")]
    while move[0] != "DONE":
        if ".info" in move[0]:
            move[0].replace(".info", "")
            print(game[move[0]].troops, game[move[0]].owner)
        elif move[0] in players[playerTurn].territories and not move[1] in players[playerTurn].territories:
            attackTerritory(game, move[0], move[1])
        else:
            print("Invalid Move")
        move = [input("Choose an attacking territory"), input("Choose a defending territory")]
    turn += 1
