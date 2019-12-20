import random
from poker_env.utils import init_52_deck


class NoLimitTexasHoldemDealer:
    '''
    The Dealer class for No Limit Texas Hold'em Poker
    '''
    def __init__(self):
        '''
        Initialize a dealer class.
        '''
        self.__deck = init_52_deck()
        self.shuffle()

    def shuffle(self):
        '''
        Shuffle the deck.
        '''
        random.shuffle(self.__deck)

    def deal_card(self):
        '''
        Deal one card from the deck.
        Returns:
            (Card): The drawn card from the deck
        '''
        return self.__deck.pop()
