import gymnasium as gym
import numpy as np

#This env is used to train the bot that places troops
class PlaceEnv(gym.Env):
    
    def __init__(self, troopCounts: np.array):
        #Instance variables
        self.troop_counts = troopCounts

        #Spaces
        self.observation_space = gym.spaces.Discrete(42)
        self.action_space = gym.spaces.Discrete(42)
    
    def get_game_data(self):
        return
        #Implement grabbing data from GameData.txt (After data is in proper format)

    def reset(self):
        return
        #Implement call to Risk.py to reset game

    def step(self, action: int):
        return
        #Implement call to Risk.py to update game and get reward