import collections
from poker_env.agent.base_agent import Agent
from poker_env.env import NoLimitTexasHoldemEnv as Env


class PluribusAgent(Agent):
    '''TODO:
    A Implementation of Pluribus, a poker AI.

    Key Algorithm: MCCFR with Negative-Regret Pruning

    Attributes:
        iterations (int): the number of iterations in training
    '''
    def __init__(self, env):
        '''
        Initialize the random agent

        Args:
            env (Env): Env instance for training agent
        '''
        super().__init__(agent_type='PluribusAgent')
        if isinstance(env, Env):
            self.env = env
        else:
            raise TypeError("Env must be a instance of NoLimitTexasHoldemEnv!")

        self.policy = collections.defaultdict(list)

        self.iterations = 0

    def calculate_strategy(self, state_str, regret):
        '''
        Calculate the strategy based on regrets.

        Args:
            state_str (str): the interpret string of the current state
            regret (numpy.ndarray): the correspond regrets of the current state
        '''
        pass

    def train(self):
        '''
        Conduct External-Sampling Monte Carlo CFR with Pruning.
        '''
        self.iterations += 1
