from poker_env.card import Card, LookUpStr
from poker_env.hand import compare_2_hands


def init_52_deck():
    '''
    Initialize a standard deck of 52 cards.
    Returns:
        (list): A list of Card object
    '''
    return [Card(suit, rank) for suit in LookUpStr.SUIT.value for rank in LookUpStr.RANK.value]


def compare_all_hands(hands):
    '''
    Compare all palyer's all seven cards.

    Args:
        hands(list) : seven cards of all players
    Returns:
        [0, ... , i, ... , 0]: player i wins
    '''
    winner = []
    winner_hand = None
    for i, hand in enumerate(hands):
        result = compare_2_hands(winner_hand, hand)
        if result == [0, 1]:
            winner = [i]
            winner_hand = hand
        elif result == [1, 1]:
            winner.append(i)
    result = [1 if (i in winner) else 0 for i in range(len(hands))]
    return result
