from sklearn.neural_network import MLPClassifier

bot1 = neural_network.MLPClassifier(early_stopping=False)
bot2 = neural_network.MLPClassifier(early_stopping=False)

bot1 = bot1.fit([[10, 1, 0]],[1])
bot2 = bot2.fit([[10, 1, 0]],[1])

reader = open("/workspaces/RiskML/RiskBot/GameData.txt", "r")
turn = int(reader.readline())
for line in reader:
    print(reader.readline())

def calculateScores(bot, data):
    scores = []
    for move in data:
        scores.append(bot.predict(move))
    return scores
#X values: [FriendlyTroops, EnemyTroops, TotalAdjacentEnemy]