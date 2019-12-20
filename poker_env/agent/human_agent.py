from poker_env.agent.base_agent import Agent


class HumanAgent(Agent):
    '''
    A Human agent.

    Attributes:
        agent_type (str): the type name of the agent
        player_id (str): the corresponding player id of the agent in a game
    '''
    def __init__(self):
        '''
        Initialize the random agent
        '''
        super().__init__(agent_type='HumanAgent')
        self._need_hint = True

    def step(self, state):
        '''
        Human Agent can not be trained.
        '''
        raise ValueError("Human Agent can not be trained for evaluation.")

    def eval_step(self, state):
        '''
        Given the legal actions for human choosing.

        Args:
            state (PokerState): the current state

        Returns:
            action (str): the action chosen by the human agent
        '''

        public_cards = state.public_cards

        # Current Round Name
        current_round = ''
        if len(public_cards) == 0:
            current_round = 'Pre-flop'
        elif len(public_cards) == 3:
            current_round = 'Flop'
        elif len(public_cards) == 4:
            current_round = 'Turn'
        elif len(public_cards) == 5:
            current_round = 'River'

        # Current State
        print(">>> Current Round:{} // Public Cards:{} // Pot:{}".format(
            current_round, public_cards, sum(state.pot)))
        print(">>> Your Hand:{}".format(state.hand_cards))

        # Input action
        legal_actions = state.legal_actions
        print_actions = []
        min_raise = sum(state.pot)
        max_raise = 0
        for action in legal_actions:
            if 'raise' in action:
                if 'raise' not in print_actions:
                    print_actions.append('raise')
                max_raise = max(max_raise, int(action[5:]))
                min_raise = min(min_raise, int(action[5:]))
            else:
                print_actions.append(action)

        if self._need_hint:
            print(
                ">>> Legal actions:{} // Action input must be a member of the legal actions"
                .format(print_actions))
            self._need_hint = False
        else:
            print(">>> Legal actions:{}".format(print_actions))

        action = input(">>> Choose action: ")
        while action not in print_actions:
            action = input("Wrong Input! Please input again:")

        if action == 'raise':
            raise_num = input(">>> Input raise amount({}~{}): ".format(
                min_raise, max_raise))
            action = 'raise{}'.format(raise_num)
            while action not in legal_actions:
                raise_num = input(
                    "Wrong Input! Please input correct raise amount:")
                action = 'raise{}'.format(raise_num)

        return action
