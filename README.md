# RiskML
Reinforcement Learning Algorithm to play a text-based version of the board game Risk.
With Gymnasium

# Strategy
Consists of two agents, one that places troops, and one that chooses where to attack.
Both agents take in the game state as a list of 42 int values, negative values represent enemy troops while positive values represent friendly troops
The Troop Agent returns a list of 42 float values from [-1.0, 1.0], the indexes with the 3 highest values are chosen and their values relative to each other are used to determine how many troops are placed at each index/territory.
The Attack Agent returns 2 indexes that represent the territory to attack and the territory to attack from

# Training
Training games are between two bots, each consisting of a Troop Agent and an Attack Agent
Both agents in a bot are rewarded the same amount
Agents are rewarded heavily for winning a game, and slightly for positive actions like capturing territories and securing bonuses.
