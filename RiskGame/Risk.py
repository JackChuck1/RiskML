import csv
import random
import math

class Player:
    def __init__(self):
        self.territories = []
        self.troopBonus = []
        self.index = -1
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
    gameIndexes = {}
    i = 0
    for line in gameInfo:
        if line[0] == "Territory":
            continue
        #Index 0: Name, Index 1: Continent, Index 2-End: Adjacent Tile Names
        game[line[0]] = Tile(line[1],line[2:])
        gameIndexes[i] = line[0]
        i += 1
    return game, gameIndexes

#returns an array of 2 player objects
def randomizeOwnership(seed, game, teams):
    teamMax = [42//teams] * teams
    players = [Player(), Player()]
    players[0].index = 0
    players[1].index = 1
    i = 0
    for tile in game:
        random.seed(seed + i)
        i += 1
        rand = random.randint(0,teams-1)
        while teamMax[rand] == 0:
            random.seed(seed + i)
            i += 1
            rand = random.randint(0,teams-1)
        teamMax[rand] -= 1
        game[tile].owner = rand
        game[tile].troops = 1
        players[rand].territories += [tile]
    return players

def randomizeTroops(seed, game, players):
    i = 0
    for player in players:
        
        #troops = 40 - amount already placed
        troops = 40 - 21
        while not troops == 0:
            random.seed(seed + i)
            game[player.territories[random.randint(0,20)]].troops += 1
            troops -= 1
            i += 1

#name1 attacks name2
def attackTerritory(game, name1, name2, players):
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
        return True
    return False

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
    print(game[name].troops)

#Utility method
def printGame(game):
    for tile in game:
        print(f"{tile}: {game[tile]}")

def findMoves(player, game):
    movesData = []
    moves = []
    for playerTile in game:
        if game[playerTile].owner == player:
            for enemyTile in game[playerTile].adjacent:
                if game[enemyTile].owner != player:
                    moves.append([playerTile, enemyTile])
                    movesData.append([game[playerTile].troops, game[enemyTile].troops])
    return [movesData, moves]

def sumFriendly(game, name):
    sum = 0
    for tile in game[name].adjacent:
        sum += game[tile].troops
    return sum

def sendData(game, player):
    with open("/workspaces/RiskML/RiskBot/GameData.txt", "w") as dataFile:
        for tile in game:
            if game[tile].owner == player.index:
                dataFile.write(f"{game[tile].troops}")
            else:
                dataFile.write(f"{game[tile].troops * -1}")
            if tile != "Western_Europe":
                dataFile.write("\n")

#Utility method
def countTroops(game):
    troops = [0,0]
    for tile in game:
        troops[game[tile].owner] += game[tile].troops
    return troops

def checkValid(game, name1, name2):
    if game[name1].owner == game[name2].owner:
        return False
    else:
        return True
    
def checkWin(player):
    if len(player.territories) == 42:
        return True
    return False

class Game():
    def __init__(self, seed):
        self.game, self.gameIndexes = readGameInfo(open("RiskGame/GameInfo.csv", "r"))
        self.players = randomizeOwnership(seed, self.game, 2)
        self.turn = 0
        randomizeTroops(seed, self.game, self.players)
        sendData(self.game, self.players[self.turn%2])
    
    def placeTroops(self, action, values):
        totalTroops = calculateBonus(self.game, self.players[self.turn%2])
        totalValues = values[0] + values[1] + values[2]
        normTroops = [round(totalTroops * (values[0]/totalValues)),
                      round(totalTroops * (values[1]/totalValues)),
                      round(totalTroops * (values[2]/totalValues))]
        print(f"{normTroops[0]}, {normTroops[1]}, {normTroops[2]}")
        if normTroops[0] + normTroops[1] + normTroops[2] < totalTroops:
            normTroops[0] += 1  #Adjust for rounding issues
        elif normTroops[0] + normTroops[1] + normTroops[2] > totalTroops:
            normTroops[0] -= 1  #Adjust for rounding issues
        print(f"{normTroops[0]}, {normTroops[1]}, {normTroops[2]}")
        placeTroops(self.game, self.gameIndexes[action[0]], normTroops[0])
        placeTroops(self.game, self.gameIndexes[action[1]], normTroops[1])
        placeTroops(self.game, self.gameIndexes[action[2]], normTroops[2])
        sendData(self.game, self.players[self.turn%2])

    def attack(self, action):
        if checkValid(self.game, self.gameIndexes[action[0]], self.gameIndexes[action[1]]):
            reward = -1
        elif attackTerritory(self.game, self.gameIndexes[action[0]], self.gameIndexes[action[1]], self.players):
            reward = 1
        else:
            reward = 0

        if checkWin(self.players[self.turn%2]):
            reward = 5
            terminated = True
        else:
            terminated = False
        sendData(self.game, self.players[self.turn%2])
        return reward, terminated

"""
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
"""
