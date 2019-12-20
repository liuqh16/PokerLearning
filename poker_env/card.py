from enum import Enum


class LookUpStr(Enum):
    '''
    A Enum that contains all strings of order for looking up
    '''

    RANK = "23456789TJKQA"
    SUIT = "scdh"

    def __init__(self, string):
        if isinstance(string, str):
            self.__value = string
        else:
            raise TypeError("Value of LookUpStr must be a string.")

    @property
    def value(self):
        return self.__value

    def index(self, char):
        '''
        Return the lowest index in look-up string where char is found.

        Args:
            char (str): single char
        Raises:
            ValueError: when the char is not found.
        '''
        return self.__value.index(char)


class Card():
    '''
    Card stores the suit and rank of a single card

    Note:
        The suit variable in a standard card game should be one of [s, c, d, h] meaning [Spade, Clubs, Diamond, Heart]
        Similarly the rank variable should be one of [A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K]
    '''

    def __init__(self, suit, rank):
        '''
        Initialize the suit and rank of a card
        Args:
            suit: string, suit of the card, should be one of valid_suit
            rank: string, rank of the card, should be one of valid_rank
        '''
        self.__suit = suit
        self.__rank = rank

    @property
    def suit(self):
        return self.__suit

    @property
    def rank(self):
        return self.__rank

    def get_index(self):
        '''
        Get index of a card.
        Returns:
            string: the combination of rank and suit of a card. Eg: 1s, 2h, Ad, BJ, RJ...
        '''
        return self.rank + self.suit
