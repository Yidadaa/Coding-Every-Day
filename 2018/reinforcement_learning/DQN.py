'''
第一个增强学习算法
'''

import gym
import tensorflow as tf
import numpy as np
import random
from collections import deque

ENV_NAME = 'CartPole-v0'
EPISODE = 10000 # Episode limitation
STEP = 300 # Step limitation in an episode
TEST = 10 # 

# Hyper Parameters for DQN
GAMMA = 0.9 # dicount factor for target Q
INITIAL_EPSILON = 0.5 # starting value of epsilon
FINAL_EPSILON = 0.01 # final value of epsilon
REPLAY_SIZE = 10000
BATCH_SIZE = 32 # size of minibatch

def main():
    # 初始化OpenAI Gym 环境和 DQN Agent
    env = gym.make(ENV_NAME)
    agent = DQN(env)

    for episode in xrange(EPISODE):
        state = env.reset()
        for step in xrange(STEP):
            # agent产生一个动作
            action = agent.egreedy_action(state)
            # 将动作作用到环境中去，获取动作产生之后的状态
            next_state, reward, done, _ = env.step(action)
            # 定义reward
            reward_agent = -1 if done else 0.1
            # TODO: 搞懂reward的用法
            agent.perceive(state, action, reward, next_state, done)
            state = next_state
            if done:
                break
        # 每100次就评估一次算法
        if episode % 100 == 0:
            total_reward = 0
            for i in xrange(TEST):
                state = env.reset()
                for j in xrange(STEP):
                    env.render()
                    action = agent.action(state)
                    state, reward, done, _ = env.step(action)
                    total_reward += reward
                    if done: 
                        break
            aver_reward = total_reward / TEST
            print('episode: %d, evaluation average reward: %f'%(episode, aver_reward))
            if aver_reward >= 200:
                break

if __name__ == '__main__':
    main()


class DQN():
    '''
    DQN Agent
    '''
    def __init__(self, env):
        '''
        初始化DQN中的必要参数
        '''
        # 初始化经验回放
        self.reply_buffer = deque()
        self.time_step = 0
        self.epilon = INITIAL_EPSILON
        self.state_dim = env.observation_space.shape[0]
        self.action_dim = env.action_space.n

        self.create_Q_network()
        self.create_training_method()

        # 初始化tf session
        self.session = tf.InteractiveSession()
        self.session.run(tf.initialize_all_variables())

    def create_Q_network(self):
        '''
        创建Q网络

        Description: 
            创建一个简单的MLP网络，包含一个输入层，一个隐藏层
        '''
        # 初始化网络权重
        W1 = self.weight_variable([self.state_dim, 20])
        b1 = self.bias_variable([20])
        W2 = self.weight_variable([20, self.action_dim])
        b2 = self.bias_variable([self.action_dim])
        # 输入层
        self.state_input = tf.placeholder('float', [None, self.state_dim])
        # 隐藏层
        h_layer = tf.nn.relu(tf.matmul(self.state_input, W1) + b1)
        # Q Value层
        self.Q_value = tf.matmul(h_layer, W2) + b2

    def weight_variable(self, shape):
        '''
        权重构造函数
        '''
        initial = tf.truncated_normal(shape)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        '''
        偏置变量构造函数
        '''
        initial = tf.constant(0.01, shape=shape)
        return tf.Variable(initial)

    def perceive(self, state, action, reward, next_state, done):
        '''感知函数
        所谓的感知函数就是将当前环境的所有参数都保存起来，相当于记忆
        '''
        # 把action进行one-hot编码，保存在reply_buffer中
        one_hot_action = np.zeros(self.action_dim)
        one_hot_action[action] = 1
        self.reply_buffer.append((state, one_hot_action, reward, next_state, done))
        # reply_buffer是一个队列，满了之后要将最老的值剔除掉
        if len(self.reply_buffer) > REPLAY_SIZE:
            self.reply_buffer.popleft()
        # 一旦reply_buffer中的状态满足了一个Batch Size这么大，就开始进行训练
        if len(self.reply_buffer) > BATCH_SIZE:
            self.train_Q_network()

    def egreedy_action(self, state):
        '''action 输出函数
        有一定的几率是随机产生一个动作
        '''
        Q_value = self.Q_value.eval(feed_dict = {
            self.state_input: [state]
        })[0]
        # 通过self.epsilon来控制几率
        if random.random() <= self.epilon:
            return random.randint(0, self.action_dim - 1)
        else:
            return np.argmax(Q_value)

        self.epilon -= (INITIAL_EPSILON - FINAL_EPSILON) / 10000

    def action(self, state):
        '''action 输出函数
        根据神经网络的结果输出下一步动作
        '''
        return np.argmax(self.Q_value.eval(feed_dict = {
            self.state_input: [state]
        })[0])

    def create_training_method(self):
        '''定义cost函数以及优化方式
        '''
        self.action_input = tf.placeholder('float', [None, self.action_dim])
        self.y_input = tf.placeholder('float', [None])
        Q_action = tf.reduce_sum(tf.matmul(self.Q_value, self.action_input), reduction_indices=1)
        # 定义cost函数
        self.cost = tf.reduce_mean(tf.square(self.y_input - Q_action))
        # 然后使用adam优化器优化
        self.optimizer = tf.train.AdamOptimizer(0.0001).minimize(self.cost)

    def train_Q_network(self):
        '''训练Q网络
        TODO: 这个函数没搞懂
        '''
        self.time_step += 1
        # 1. 从replay memory中获得随机的minibatch
        minibatch = random.sample(self.reply_buffer, BATCH_SIZE)
        state_batch = [data[0] for data in minibatch]
        action_batch = [data[1] for data in minibatch]
        reward_batch = [data[2] for data in minibatch]
        next_state_batch = [data[3] for data in minibatch]

        # 2. 计算y
        y_batch = []
        Q_value_batch = self.Q_value.eval(feed_dict={
            self.state_input: next_state_batch
        })

        for i in range(BATCH_SIZE):
            done = minibatch[i][4]
            if done:
                y_batch.append(reward_batch[1])
            else:
                y_batch.append(reward_batch[i] + GAMMA * np.max(Q_value_batch[i]))
        
        self.optimizer.run(feed_dict={
            self.y_input: y_batch,
            self.action_input: action_batch,
            self.state_input: state_batch
        })