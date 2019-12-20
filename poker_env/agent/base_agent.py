class Agent:
    '''
    The base Agent class

    Attributes:
        agent_type (str): the type name of the agent
        player_id (str): the corresponding player id of the agent in a game
    '''
    def __init__(self, agent_type='BaseAgent'):
        '''
        Initialize the agent
        '''
        self._type = agent_type
        self._player_id = None

    @property
    def player_id(self):
        return self._player_id

    def set_player_id(self, player_id):
        self._player_id = player_id

    @property
    def agent_type(self):
        return self._type

    def step(self, state):
        '''
        Need to be Implemented.
        Predict the action given the current state in gerenerating training data.

        Args:
            state (PokerState): the current state

        Returns:
            action (str): the action predicted by the agent
        '''
        raise NotImplementedError

    def eval_step(self, state):
        '''
        Need to be Implemented.
        Predict the action given the current state for evaluation.

        Args:
            state (PokerState): the current state

        Returns:
            action (str): the action predicted by the agent
        '''
        raise NotImplementedError
