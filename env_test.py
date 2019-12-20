from poker_env.env import NoLimitTexasHoldemEnv
from poker_env.agent.random_agent import RandomAgent
from poker_env.agent.human_agent import HumanAgent
from poker_env.agent.cfr_agent import CFRAgent

env = NoLimitTexasHoldemEnv(num_players=6, allow_step_back=True, init_chips=10)
agent = CFRAgent(env=env)

for _ in range(10):
    agent.train()

print("finish training")