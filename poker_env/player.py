class NoLimitTexasHoldemPlayer:
    '''
    The Player class for No Limit Texas Hold'em Poker.
    '''
    def __init__(self, player_id, init_chips):
        '''
        Initialize a player class.

        Args:
            player_id (int): The id of the player
            init_chips (int): The number of chips the player has initially
        '''
        self.player_id = player_id
        self.init_chips = init_chips
        # The chips that this player has put in until now
        self.in_chips = 0

        self.hand = []
        # Status can be alive, folded, all-in
        self.status = 'alive'

    def get_player_id(self):
        '''
        Return the id of the player
        '''
        return self.player_id

    def get_remained_chips(self):
        '''
        Return the remained chips of the player
        '''
        return self.init_chips - self.in_chips

    def get_action(self, state):
        '''
        Return the available actions
        '''
        return state['legal_actions']
