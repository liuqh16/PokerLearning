import numpy as np
import random

from poker_env.game import NoLimitTexasHoldemGame as Game
from poker_env.agent.base_agent import Agent


class NoLimitTexasHoldemEnv:
    '''
    No Limit Texas Holdem Environment

    Attributes:
        allow_step_back (boolean): allow game step back or not(Default=False).
        num_players (int): the number of players participating in the game(Default=2).
        small_blind (int): the number of Small Blind(SB) chips of the game(Default=1).
        big_blind (int): the number of Big Blind(BB) chips of the game(Default=2).
        init_chips (int or list): chips that each player holds when game starts. Int means that each player hold the same chips, while list means initializing each players' chips individually.
    '''

    def __init__(self, allow_step_back=False, num_players=2, small_blind=1, big_blind=2, init_chips=100):
        '''
        Initialize the Nolimitholdem environment
        '''
        self.__game = Game(allow_step_back=allow_step_back,
                           num_players=num_players,
                           small_blind=small_blind,
                           big_blind=big_blind,
                           init_chips=init_chips)
        self.__allow_step_back = allow_step_back
        self.__player_num = self.__game.get_player_num()
        self.__action_space = self.get_action_space()
        self.__agents = []

        # A counter for the timesteps
        self.__timestep = 0

        # Modes
        self._has_human_agent = False

    @property
    def allow_step_back(self):
        return self.__allow_step_back

    @property
    def player_num(self):
        return self.__player_num

    @property
    def action_space(self):
        return self.__action_space

    @property
    def agents(self):
        return self.__agents
        # for i, agent in enumerate(self.__agents):
        #     if isinstance(agent, Agent):
        #         print("id_{}:{}".format(i, agent.agent_type))

    def init_game(self):
        '''
        Start a new game

        Returns:
            (tuple): Tuple containing:
                (PokerState): The begining state of the game
                (int): The begining player
        '''
        state, player_id = self.__game.init_game()
        return state, player_id

    def step(self, action):
        '''
        Step forward

        Args:
            action (str): the action taken by the current player

        Returns:
            (tuple): Tuple containing:
                (PokerState): The next state
                (int): The ID of the next player
        '''
        self.__timestep += 1
        next_state, player_id = self.__game.step(action)
        return next_state, player_id

    def step_back(self):
        '''
        Take one step backward.

        Returns:
            (tuple): Tuple containing:
                (PokerState): The previous state
                (int): The ID of the previous player

        Note: Error will be raised if step back from the root node.
        '''
        if not self.allow_step_back:
            raise Exception('Step back is off. To use step_back, please set allow_step_back=True in the env')
        if not self.__game.step_back():
            return False
        player_id = self.get_player_id()
        state = self.get_state()
        return state, player_id

    def get_state(self):
        '''
        Get the state of the current player

        Returns:
            (PokerState): The observed state of the current player
        '''
        return self.__game.get_state()

    def set_agents(self, agents):
        '''
        Set the agents that will interact with the environment

        Args:
            agents (list): List of Agent classes
        '''
        for index, agent in enumerate(agents):
            if not isinstance(agent, Agent):
                raise TypeError("Agents must be subclasses of Agent class!")
            if agent.agent_type == 'HumanAgent':
                self._has_human_agent = True
            agent.set_player_id(index)
            self.__agents.append(agent)

        if len(self.__agents) != self.__player_num:
            raise ValueError("Agents number should be equal to the player number")

    def run(self, is_training=False, seed=None):
        '''
        Run a complete game, either for evaluation or training RL agent.

        Args:
            is_training (boolean): True if for training purpose.
            seed (int): A seed for running the game.

        Returns:
            (tuple) Tuple containing:
                (list): A list of trajectories generated from the environment.
                (list): A list payoffs. Each entry corresponds to one player.
        '''
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        trajectories = [[] for _ in range(self.player_num)]
        state, player_id = self.init_game()

        # Loop to play the game
        while not self.is_over():
            # Save state
            trajectories[player_id].append(state)
            # Agent plays
            if not is_training:
                action = self.__agents[player_id].eval_step(state)
            else:
                action = self.__agents[player_id].step(state)
            if self._has_human_agent:
                if self.__agents[player_id].agent_type == 'HumanAgent':
                    print("Human Player{} Choose {}".format(player_id, action))
                else:
                    print("Computer Player{} Choose {}".format(player_id, action))
            # Save action
            trajectories[player_id].append(action)
            # Environment steps
            next_state, next_player_id = self.step(action)
            # Set the state and player
            state = next_state
            player_id = next_player_id

        # Payoffs
        payoffs = self.get_payoffs()

        return trajectories, payoffs

    def is_over(self):
        '''
        Check whether the current game is over

        Returns:
            (boolean): True is current game is over
        '''
        return self.__game.is_over()

    def get_player_id(self):
        '''
        Get the current player id

        Returns:
            (int): the id of the current player
        '''
        return self.__game.get_player_id()

    def get_payoffs(self):
        '''
        Get the payoff of a game

        Returns:
           payoffs (list): list of payoffs
        '''
        return self.__game.get_payoffs()

    def get_legal_actions(self):
        '''
        Get all leagal actions

        Returns:
            encoded_action_list (list): return encoded legal action list (from str to int)
        '''
        return self.__game.get_legal_actions()

    def get_action_space(self):
        '''
        Get action space of the game.

        Returns:
            (list): each element (str) represent a possible action
        '''
        min_raise = self.__game.big_blind
        max_raise = self.__game.init_chips if isinstance(self.__game.init_chips, int) else max(self.__game.init_chips)
        action_space = ['fold', 'check', 'call']
        for i in range(min_raise, max_raise):
            action_space.append('raise{}'.format(i))
        action_space.append('all-in')
        return action_space

    def get_game_tree(self):
        '''
        Return the action sequence of the game
        '''
        return self.__game.game_tree
