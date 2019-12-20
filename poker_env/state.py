from poker_env.card import LookUpStr


class PokerState:
    '''
    The standard state of the decision point in a No Limit Texas Holdem Game.
    (a node in the game tree)

    Attributes:
        player_id (int): the id of the current player
        pot (list): each element corresponds to the total number of a player betting into the game
        hand_cards (list): a list of Card class
        public_cards (list): a list of Card class
        legal_actions (list): a list of Strings, each element corresponds to a legal action
    '''
    def __init__(self, player_id, pot, hand_cards, public_cards, legal_actions):
        '''
        Initialize a poker state.
        '''
        self.__player_id = player_id
        self.__pot = pot
        self.__hand_cards = hand_cards
        self.__public_cards = public_cards
        self.__legal_actions = legal_actions

    @property
    def player_id(self):
        return self.__player_id

    @property
    def pot(self):
        return self.__pot

    @property
    def hand_cards(self):
        return self.__hand_cards

    @property
    def public_cards(self):
        return self.__public_cards

    @property
    def legal_actions(self):
        return self.__legal_actions

    def get_bet_round(self):
        '''
        Get the current round of the game

        Returns:
            (int): 0 for pre-flop round
                   1 for flop round
                   2 for turn round
                   3 for river round
        '''
        return max(0, len(self.public_cards) - 2)

    def need_action_abstraction(self):
        '''
        Decide if need conduct action abstraction or not.

        Returns:
            (Boolean): True if need action abstraction
        '''
        # Do not conduct abstraction in Pre-flop / Flop round
        return self.get_bet_round() >= 1

    def get_information(self):
        '''
        Get information situation of the current player.
        "Information Situation" in a NLTH Poker game means "2 hand cards + all public cards".
        Generally, information situation need conduct abstraction into several buckets.

        Returns:
            (list): strings of cards' ranks and suits. First 2 are hand cards.
        '''
        return [card.get_index() for card in (self.hand_cards + self.public_cards)]

    def get_lossless_abstraction(self):
        '''
        Conduct lossless abstraction and return the result.
        (Remove the influence of suit.)

        Returns:
            (list): strings of cards' ranks and suits. First 2 are hand cards.
        '''
        # Sort cards through their ranks
        sorted_cards = sorted(self.hand_cards, key=lambda card: LookUpStr.RANK.index(card.rank), reverse=True) \
            + sorted(self.public_cards, key=lambda card: LookUpStr.RANK.index(card.rank), reverse=True)
        sorted_string = ''.join([card.get_index() for card in sorted_cards])

        # Special handling for Pair hand cards + public cards
        if sorted_cards[0].rank == sorted_cards[1].rank and len(sorted_cards) > 2:
            # Sort hand cards through flush counts
            suit_num = [sorted_string.count(card.suit) for card in sorted_cards[:2]]
            if suit_num[0] < suit_num[1]:
                sorted_cards = sorted_cards[1::-1] + sorted_cards[2:]
            elif suit_num[0] == suit_num[1] and suit_num[0] > 1:
                # Sort hand cards through flush rank
                max_rank = [sorted_string[sorted_string[4:].index(card.suit) + 3] for card in sorted_cards[:2]]
                if max_rank[0] < max_rank[1]:
                    sorted_cards = sorted_cards[1::-1] + sorted_cards[2:]
            sorted_string = ''.join([card.get_index() for card in sorted_cards])

        origin_suit_order = ''
        for suit in sorted_string[1::2]:
            if suit not in origin_suit_order:
                origin_suit_order += suit
        match_suit_order = LookUpStr.SUIT.value[0:len(origin_suit_order)]

        match_string = sorted_string.translate(str.maketrans(origin_suit_order, match_suit_order))

        return [match_string[i:i + 2] for i in range(0, len(match_string), 2)]
