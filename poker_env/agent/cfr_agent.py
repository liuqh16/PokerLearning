import numpy as np
import collections
from poker_env.agent.base_agent import Agent
from poker_env.env import NoLimitTexasHoldemEnv as Env
from poker_env.action import AbstractAction


class CFRAgent(Agent):
    '''
    A CFR agent (using CounterFactual Regret Minimization algorithm).

    Attributes:
        agent_type (str): the type name of the agent

    '''
    def __init__(self, env):
        '''
        Initialize the random agent

        Args:
            env (Env): Env instance for training agent
        '''
        super().__init__(agent_type='CFRAgent')
        if isinstance(env, Env):
            self.env = env
        else:
            raise TypeError("Env must be a instance of NoLimitTexasHoldemEnv!")
        self.__policy = collections.defaultdict(list)
        self.__average_policy = collections.defaultdict(np.array)
        self.__regrets = collections.defaultdict(np.array)
        self.__action_space = env.get_action_space()
        self.__abstract_action_space = [_ for _ in AbstractAction]
        self.iterations = 0

    @property
    def policy(self):
        return self.__policy

    @property
    def average_policy(self):
        return self.__average_policy

    @property
    def regrets(self):
        return self.__regrets

    @property
    def action_num(self):
        return len(self.__action_space)

    @property
    def abs_action_num(self):
        return len(self.__abstract_action_space)

    def train(self):
        '''
        Do one iteration of CFR
        '''
        self.iterations += 1
        for player_id in range(self.env.player_num):
            self.env.init_game()
            # The reach probability of the root node for every player is 1
            probs = np.ones(self.env.player_num)
            self.traverse_tree(probs, player_id)
        self.update_policy()

    def traverse_tree(self, probs, player_id):
        '''
        Traverse the game tree, update the regrets.

        Args:
            probs (numpy.ndarray): The reach probability of the current state/node
            player_id (int): The traverser to update the value

        Returns:
            state_utilities (numpy.ndarray): The expected utilities for all the players
        '''
        if self.env.is_over():
            return np.array(self.env.get_payoffs())

        current_player = self.env.get_player_id()

        action_utilities = {}
        state_utility = np.zeros(self.env.player_num)

        state = self.env.get_state()
        encode_state = self.encode_state(state)
        legal_actions = self.encode_action(state)
        # Self-play: All player share the same policy, along with the same action probs
        action_probs = self.get_action_probs(
            policy=self.policy,
            state=encode_state,
            legal_actions=legal_actions,
            length=self.abs_action_num
            if state.need_action_abstraction() else 0)
        # traverse every legal action
        for action in legal_actions:
            action_prob = action_probs[action]
            # calculate the reach probability of the next state
            new_probs = probs.copy()
            new_probs[current_player] *= action_prob
            # keep traversing the child state
            self.env.step(self.decode_action(action, self.env.get_state()))
            action_utility = self.traverse_tree(new_probs, player_id)
            action_utilities[action] = action_utility
            # state utility is the expectation of action utility
            state_utility += action_prob * action_utility
            self.env.step_back()

        if not current_player == player_id:
            return state_utility

        # If is current player, record the policy and compute regret
        player_prob = probs[current_player]
        counterfactual_prob = np.prod(probs) / player_prob
        player_state_utility = state_utility[current_player]

        if encode_state not in self.regrets:
            self.regrets[encode_state] = np.zeros(self.action_num)
        if encode_state not in self.average_policy:
            self.average_policy[encode_state] = np.zeros(self.action_num)
        for action in legal_actions:
            action_prob = action_probs[action]
            regret = counterfactual_prob * (
                action_utilities[action][current_player] -
                player_state_utility)
            self.regrets[encode_state][action] += regret
            self.average_policy[encode_state][
                action] += self.iterations * player_prob * action_prob
        return state_utility

    def update_policy(self):
        '''
        Update policy based on the current regrets
        '''
        for encode_state, regret in self.regrets.items():
            positive_regret_sum = np.sum(np.maximum(regret, 0))
            if positive_regret_sum > 0:
                action_probs = np.maximum(regret, 0) / positive_regret_sum
            else:
                action_probs = np.ones(regret.shape) / len(regret)
            self.policy[encode_state] = action_probs

    def get_action_probs(self, policy, state, legal_actions, length=0):
        '''
        Get the action probabilities of the current state.

        Args:
            policy (dict): select which policy to use
            state (str): key in policy dictionary which represent the information of state
            legal_actions (list): indices of legal actions
            [optional] length (int): length of action probabilities vector. Default is the length of env action space

        Returns:
            (numpy.ndarray): the action probabilities
        '''
        action_length = length if length != 0 else self.action_num
        if state not in policy:
            action_probs = np.array(
                [1.0 / action_length for _ in range(action_length)])
            policy[state] = action_probs
        else:
            action_probs = policy[state]
        # Remove illegal actions
        legal_probs = np.zeros(action_probs.shape)
        legal_probs[legal_actions] = action_probs[legal_actions]
        # Normalization
        if np.sum(legal_probs) == 0:
            legal_probs[legal_actions] = 1 / len(legal_actions)
        else:
            legal_probs /= np.sum(legal_probs)
        return legal_probs

    def encode_state(self, state):
        '''
        Conduct infomation abstraction and Encode observable state to specific string.

        Args:
            state (PokerState): the state of the game

        Returns:
            (str): represent the information of the state
        '''
        lossless_info = state.get_lossless_abstraction()
        # TODO: lossy information abstraction
        abstract_info = ''.join(lossless_info)
        return abstract_info

    def encode_action(self, state):
        '''
        Encode legal actions if need abstraction or not.

        Args:
            state (PokerState): the state of the game

        Returns:
            (list): Indices of legal actions(Abstract or not).
        '''
        encode_actions = []
        legal_actions = state.legal_actions

        if not state.need_action_abstraction():
            for action in legal_actions:
                encode_actions.append(self.__action_space.index(action))
        else:
            total_pot = sum(state.pot)
            max_raise = 0
            for action in legal_actions:
                if action == 'fold':
                    encode_actions.append(AbstractAction.FOLD.value)
                elif action == 'check':
                    encode_actions.append(AbstractAction.CHECK.value)
                elif action == 'call':
                    encode_actions.append(AbstractAction.CALL.value)
                elif action == 'all-in':
                    encode_actions.append(AbstractAction.ALL_IN.value)
                elif 'raise' in action:
                    raise_amount = int(action[5:])
                    max_raise = max(max_raise, raise_amount)
            if max_raise > 0.5 * total_pot:
                encode_actions.append(AbstractAction.RAISE_HALF_POT.value)
            if max_raise > total_pot:
                encode_actions.append(AbstractAction.RAISE_POT.value)
            if max_raise > 2 * total_pot:
                encode_actions.append(AbstractAction.RAISE_2POT.value)

        return encode_actions

    def decode_action(self, action, state):
        '''
        Decode the action according to current state

        Args:
            action (int): index of action in (abstract) action space
            state (PokerState): current state

        Returns:
            (str): legal action string for the state
        '''
        if state.need_action_abstraction():
            return self.__abstract_action_space[action].translate_from(state)
        else:
            return self.__action_space[action]

    def step(self, state):
        '''
        Predict the action given the current state.

        Args:
            state (PokerState): the current state

        Returns:
            action (str): random action based on the action probability vector
        '''
        action_probs = self.get_action_probs(
            policy=self.policy,
            state=self.encode_state(state),
            legal_actions=self.encode_action(state),
            length=self.abs_action_num
            if state.need_action_abstraction() else 0)
        action = np.random.choice(len(action_probs), p=action_probs)
        return self.decode_action(action, state)

    def eval_step(self, state):
        '''
        Given a state, predict the best action based on average policy

        Args:
            state (PokerState): the current state

        Returns:
            action (str): best action based on policy
        '''
        action_probs = self.get_action_probs(
            policy=self.average_policy,
            state=self.encode_state(state),
            legal_actions=self.encode_action(state),
            length=self.abs_action_num
            if state.need_action_abstraction() else 0)
        action = np.argmax(action_probs)
        return self.decode_action(action, state)
