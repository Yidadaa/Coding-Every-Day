'''
使用PG完成cartpole任务
'''

import tensorflow as tf
import numpy as np
import random
import gym
import math
import matplotlib.pyplot as plt

def softmax(x):
    '''定义softmax函数
    '''
    e_x = np.exp(x - np.max(x))
    out = e_x / e_x.sum()
    return out

def policy_gradient():
    '''使用PG方法进行训练
    '''
    with tf.variable_scope('policy'):
        params = tf.get_variable('policy_parameters', [4, 2])
        state = tf.placeholder('float', [None, 4])
        actions = tf.placeholder('float', [None, 2])
        # TODO: advantages是啥
        advantages = tf.placeholder('float', [None, 1])
        linear = tf.matmul(state, params)
        # 输出的是所有动作的概率
        prob = tf.nn.softmax(linear)
        # TODO: good probabilities是啥
        good_prob = tf.reduce_sum(tf.multiply(prob, actions), reduction_indices=[1])
        eligibility = tf.log(good_prob) * advantages
        loss = -tf.reduce_sum(eligibility)
        optimizer = tf.train.AdamOptimizer(0.01).minimize(loss)
        return prob, state, actions, advantages, optimizer

def value_gradient():
    '''使用VG方法进行训练
    TODO: 与DQN的方法有何不同？
    '''
    with tf.variable_scope('value'):
        state = tf.placeholder('float', [None, 4])
        newvals = tf.placeholder('float', [None, 1])
        w1 = tf.get_variable('w1', [4, 10])
        b1 = tf.get_variable('b1', [10])
        h1 = tf.nn.relu(tf.matmul(state, w1) + b1)
        w2 = tf.get_variable('w2', [10, 1])
        b2 = tf.get_variable('b2', [1])
        calculated = tf.matmul(h1, w2) + b2
        diffs = calculated - newvals
        loss = tf.nn.l2_loss(diffs) # 定义l2距离为loss
        optimizer = tf.train.AdamOptimizer(0.01).minimize(loss)
        return calculated, state, newvals, optimizer, loss

def run_episode(env, policy_grad, value_grad, sess):
    '''执行训练
    '''
    pl_calculated, pl_state, pl_actions, pl_advantages, pl_optimizer = policy_grad
    vl_calculated, vl_state, vl_newvals, vl_optimizer, vl_loss = value_grad
    observation = env.reset()
    totalreward = 0
    states = []
    actions = []
    advantages = []
    transitions = []
    update_vals = []

    # env.render()

    # 以200步为一个episode
    for _ in range(200):
        # 计算策略
        obs_vector = np.expand_dims(observation, axis=0)
        probs = sess.run(pl_calculated, feed_dict={
            pl_state: obs_vector
        })
        action = 0 if random.uniform(0, 1) < probs[0][0] else 1
        # 记录信息
        states.append(observation)
        action_one_hot = np.zeros(2)
        action_one_hot[action] = 1
        actions.append(action_one_hot)
        # 将动作作用到环境
        old_observation = observation
        observation, reward, done, info = env.step(action)
        # 存储信息
        transitions.append((old_observation, action, reward))
        totalreward += reward

        if done:
            break

    for i, trans in enumerate(transitions):
        obs, action, reward = trans

        # 计算未来的reward
        future_reward = 0
        future_transitions = len(transitions) - i
        decrease = 1 # 衰减系数
        for j in range(future_transitions):
            future_reward += transitions[i + j][2] * decrease
            decrease = decrease * 0.97
        obs_vector = np.expand_dims(obs, axis=0)
        # TODO: 这里计算的是什么？为什么future_reward要减去它？
        currentval = sess.run(vl_calculated, feed_dict={
            vl_state: obs_vector
        })[0][0]

        # advantage: 当前action要比normal action好多少？
        advantages.append(future_reward - currentval)

        update_vals.append(future_reward)
    
    # 更新value function
    update_vals_vector = np.expand_dims(update_vals, axis=1)
    sess.run(vl_optimizer, feed_dict={
        vl_state: states,
        vl_newvals: update_vals_vector
    })

    advantages_vector = np.expand_dims(advantages, axis=1)
    sess.run(pl_optimizer, feed_dict={
        pl_state: states,
        pl_advantages: advantages_vector,
        pl_actions: actions
    })

    return totalreward

def train():
    '''执行训练
    '''
    env = gym.make('CartPole-v0')
    # env = gym.wrappers.Monitor(env, 'cartpole-hills/', force=True)
    policy_grad = policy_gradient()
    value_grad = value_gradient()
    sess = tf.InteractiveSession()
    sess.run(tf.initialize_all_variables())

    # 先进行训练
    for i in range(2000):
        reward = run_episode(env, policy_grad, value_grad, sess)
        if i % 50 == 0:
            print(i, reward)
        if reward >= 200:
            print('done', i, reward)
            break
    
    totalreward = 0
    # 然后进行评估
    for i in range(1000):
        reward = run_episode(env, policy_grad, value_grad, sess)
        totalreward += reward
        if i % 50 == 0:
            print(i, totalreward / (i + 1))

    print('Averavge reward: ', totalreward / 1000)

if __name__ == '__main__':
    train()