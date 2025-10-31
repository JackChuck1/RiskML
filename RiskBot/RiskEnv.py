import gymnasium as gym
from gymnasium.utils.env_checker import check_env
import numpy as np
import sys

sys.path.append("/workspaces/RiskML/")
from RiskGame.Risk import Game
gym.register(
    id="PlaceEnv-v0",
    entry_point="RiskBot.RiskEnv:PlaceEnv",
)
#This env is used to train the bot that places troops
class PlaceEnv(gym.Env):
    
    def __init__(self, seed = 123):
        #Instance variables
        self.game = Game(seed)

        #Spaces
        self.observation_space = gym.spaces.Box(low=np.inf, high=np.inf, shape=(42,), dtype=np.int32)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(42,), dtype=np.float32)
    
    #returns every territory represented by the number of troops on it (positive is friendly)
    def _get_game_data(self) -> np.array:
        dataFile = open("/workspaces/RiskML/RiskBot/GameData.txt", "r")
        obs = np.array([np.int32(line) for line in dataFile])
        return obs
        
    #Resets env to a new random state, returns initial observations
    def reset(self, seed=123, options=None):
        super().reset(seed=seed)
        self.game = Game(seed)

        info = {}
        obs = self._get_game_data()
        return obs, info

    def step(self, action):
        indexes = [0, 1, 2]
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
                indexes[2] = i
            i += 1

        values = (action[indexes[0]], action[indexes[1]], action[indexes[2]])
        self.game.placeTroops(indexes, values)
        
        info = {}
        obs = self._get_game_data
        return obs, 0, False, False, info
        #Implement call to Risk.py to update game and get reward

gym.register(
    id="AttackEnv-v0",
    entry_point="RiskBot.RiskEnv:AttackEnv",
)
class AttackEnv(gym.Env):

    def __init__(self, placeEnv: PlaceEnv):
        #Instance variables
        self.placeEnv = placeEnv
        #Spaces
        self.observation_space = gym.spaces.Box(low=np.inf, high=np.inf, shape=(42,), dtype=np.int32)
        self.action_space = gym.spaces.Box(low=0, high=42, shape=(2,), dtype=np.int32)
    
    def _get_game_data(self):
        dataFile = open("/workspaces/RiskML/RiskBot/GameData.txt", "r")
        obs = np.array([np.int32(line) for line in dataFile])
        return obs
        #Implement grabbing data from GameData.txt (After data is in proper format)
    
    #I'm never gonna call this I just don't think gym will like it if I don't have it
    def reset(self,seed=123, options=None):
        super().reset(seed=seed)
        self.placeEnv.game = Game(seed)

        info = {}
        obs = self._get_game_data()
        return obs, info
        #Implement call to Risk.py to reset game

    def step(self, action):
        reward, terminated = self.placeEnv.game.attack(action)
        
        info = {}
        obs = self._get_game_data
        return obs, reward, terminated, False, info
        #Implement call to Risk.py to update game and get reward

if __name__ == "__main__":
    print("Program crashing after ts ----------------------------------------")
    placeEnv = gym.make("PlaceEnv-v0", seed=123)
    attackEnv = gym.make("AttackEnv-v0", placeEnv=placeEnv)
    check_env(placeEnv.unwrapped)
    check_env(attackEnv.unwrapped)

    obs = placeEnv.reset(seed=123)[0]

    for i in range(10):
        print(f"Place: {placeEnv.action_space.sample()}")
        print(f"Attack: {attackEnv.action_space.sample()}")