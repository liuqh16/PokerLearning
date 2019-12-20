from poker_env.utils import init_52_deck
from poker_env.card import Card
from poker_env.state import PokerState
import random


def run_test():
    deck = init_52_deck()
    suit_list = ['s', 'c', 'd', 'h']
    legal_cards_num = [2, 5, 6, 7]
    wrong_count = 0
    for _ in range(100):
        cards = [card.get_index() for card in random.sample(deck, random.choice(legal_cards_num))]
        card_string = ''.join(cards)
        state = PokerState(player_id=0,
                           pot=[i for i in range(6)],
                           hand_cards=[Card(card[1], card[0]) for card in cards[:2]],
                           public_cards=[Card(card[1], card[0]) for card in cards[2:]],
                           legal_actions=['check', 'fold'])
        ini_abs = state.get_lossless_abstraction()
        for _ in range(100):
            random.shuffle(suit_list)
            random_suit = ''.join(suit_list)
            card_string = card_string.translate(str.maketrans('scdh', random_suit))
            new_cards = [card_string[i:i + 2] for i in range(0, len(card_string), 2)]
            new_state = PokerState(player_id=0,
                                   pot=[i for i in range(6)],
                                   hand_cards=[Card(card[1], card[0]) for card in new_cards[:2]],
                                   public_cards=[Card(card[1], card[0]) for card in new_cards[2:]],
                                   legal_actions=['check', 'fold'])
            new_abs = new_state.get_lossless_abstraction()
            if new_abs is ini_abs:
                wrong_count += 1
                break
        # print(ini_abs)
    print("wrong number: {}".format(wrong_count))
