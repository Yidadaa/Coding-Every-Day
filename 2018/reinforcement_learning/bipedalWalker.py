import gym
import numpy as np
import time

if __name__ == '__main__':
    env = gym.make('BipedalWalker-v2')
    env.reset()
    action = [0, 0, 0, 0]
    for i in range(100):
        time.sleep(0.01)
        action[0] = i / 100
        action[1] = i / 100
        print(action)
        env.step(action)
        env.render()
    env.close()
