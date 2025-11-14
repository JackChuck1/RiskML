import RiskEnv
import random
from RiskEnv import PlaceEnv, AttackEnv
place_model = None
attack_model = None
place_env = PlaceEnv()
attack_env = AttackEnv(place_env)
def runTurn(place_env, attack_env, epsilon=0.0):
    
    initial_obs, info = place_env.reset()
    obs = initial_obs
    

    if random.randrange(0,1) < epsilon:
       place_action = place_env.action_space.sample()
    else:
        place_action = -1
       #place_action = place_model.predict(obs)
    obs = place_env.step(place_action)[0]

    actions = [place_action]
    reward = 0
    while True:
        if random.randrange(0,1) < epsilon:
           attack_action = attack_env.action_space.sample()
        else:
            attack_action = -1
            #attack_action = attack_model.predict(obs)'
        if check_done(attack_action):
            break

        actions.append(attack_action)
        obs, temp, terminated = attack_env.step(attack_action)[:3]
        reward += temp
    return reward, initial_obs, actions, terminated

def check_done(action):
    for i in action:
        if i[0] > 0:
            return False
    return True
def format_reward(reward, action):
        highFriendly = (-2, 43)
        highEnemy = (-2, 43)
        index = 0
        for i in action:
            if i[0] > highFriendly[0]:
                highFriendly = (i[0], index)
            if i[1] > highFriendly[1]:
                highEnemy = (i[1], index)
            index += 1
        action[highFriendly[1]][0] = reward
        action[highEnemy[1]][1] = reward
        return action

def train(episodes=100, epsilon_i = 1.0, decay = 0.995):
    epsilon = epsilon_i

    for episode in range(episodes):
        reward, initial_obs, actions, new_game = runTurn(place_env, attack_env, epsilon)
        #place_model.train(initial_obs, format_reward(reward, actions[0]))
        for i in range(1,len(actions)):
            pass
            #attack_model.train(initial_obs, format_reward(reward, actions[i]))
        if new_game:
            place_env.reset(random.randint(0,10000))
            continue

        epsilon *= decay
        place_env.game.turn += 1
    print(f"Episode {episode+1}/{episodes} - Reward: {reward} - Epsilon: {epsilon:.4f}")