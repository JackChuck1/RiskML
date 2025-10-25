import gymnasium as gym
import numpy as np
import sys
sys.path.append("/workspaces/RiskML/")
from RiskGame.Risk import Game

#This env is used to train the bot that places troops
class PlaceEnv(gym.Env):
    
    def __init__(self, troopCounts: np.array):
        #Instance variables
        self.env = Game()
        self.troop_counts = troopCounts

        #Spaces
        self.observation_space = gym.spaces.Discrete(42)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(42,), dtype=np.float32)
    
    def _get_game_data(self):
        dataFile = open("/workspaces/RiskML/RiskBot/GameData.txt", "r")
        obs = np.array([int(line) for line in dataFile])
        return obs
        #Implement grabbing data from GameData.txt (After data is in proper format)

    def reset(self):
        self.env = Game()
        obs = self._get_game_data()
        return obs
        #Implement call to Risk.py to reset game

    def step(self, action):
        indexes = [-2,-2,-2]
        i = 0
        for value in action:
            if value > action[indexes[0]]:
                indexes[2] = indexes[1]
                indexes[1] = indexes[0]
                indexes[0] = i
            elif value > action[indexes[1]]:
                indexes[2] = indexes[1]
                indexes[1] = i
            elif value > action[indexes[2]]:
                indexes[2]
            i += 1

        values = (action[indexes[0]], action[indexes[1]], action[indexes[2]])
        self.env.placeTroops(indexes, values)

        obs = self._get_game_data
        return obs
        #Implement call to Risk.py to update game and get reward
        
env = PlaceEnv(np.zeros)
env.step( np.random.uniform(low=-1.0, high=1.0, size=(42,)).astype(np.float32))