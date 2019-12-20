import numpy as np
from copy import deepcopy
from poker_env.dealer import NoLimitTexasHoldemDealer as Dealer
from poker_env.player import NoLimitTexasHoldemPlayer as Player
from poker_env.judger import NoLimitTexasHoldemJudger as Judger
from poker_env.round import NoLimitTexasHoldemRound as Round
from poker_env.state import PokerState


class NoLimitTexasHoldemGame:
    '''
    The Game class for No Limit Texas Hold'em Poker

    Attributes:
        allow_step_back (boolean): allow game step back or not(Default=False).
        num_players (int): the number of players participating in the game(Default=2).
        small_blind (int): the number of Small Blind(SB) chips of the game(Default=1).
        big_blind (int): the number of Big Blind(BB) chips of the game(Default=2).
        init_chips (int or list): chips that each player holds when game starts. Int means that each player hold the same chips, while list means initializing each players' chips individually.
    '''

    def __init__(self, allow_step_back=False, num_players=2, small_blind=1, big_blind=2, init_chips=100):
        '''
        Initialize the settings of No Limit Texas Hold'em Game Class
        '''
        self.allow_step_back = allow_step_back
        self.num_players = num_players
        self.init_chips = init_chips
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.allow_hint_info_shown = False

    def init_game(self, button=None):
        '''
        Initialize the objects of No Limit Texas Hold'em Game Class.

        Deal 2 cards to each players and start the first round. (pre-flop)

        Args:
            button (int): the position of the button(Default=None, which means random).
        Returns:
            Returns:
            (tuple): Tuple containing:
                (PokerState): The first state of the game
                (int): Current player's id
        '''
        # Initialize a judger class which will decide who wins in the end
        self.judger = Judger()
        # Initialize a dealer that can deal cards
        self.dealer = Dealer()
        # Initialize a round class which will proceed the game
        self.round = Round(self.num_players, self.big_blind)
        # Count the round. There are 4 rounds in each game.
        self.round_counter = 0
        # Initialize several players to play the game
        if isinstance(self.init_chips, int):
            self.players = [Player(i, self.init_chips) for i in range(self.num_players)]
        elif isinstance(self.init_chips, list):
            if len(self.init_chips) != self.num_players:
                raise ValueError("Length of init_chips must equal to num_players.")
            self.players = [Player(i, chips) for i, chips in enumerate(self.init_chips)]
        self.game_pointer = 0
        # Initialize public cards
        self.public_cards = []

        # Save the history for stepping back to the last state.
        self.history = []

        # Save the action sequence
        self.game_tree = []

        # Set position
        if button is not None and button >= self.num_players:
            raise ValueError("button is out of ranges")
        # Button
        self.button = np.random.randint(0, self.num_players) if button is None else button
        # SB
        sb = (self.button + 1) % self.num_players
        # BB
        bb = (sb + 1) % self.num_players
        self.players[sb].in_chips = self.small_blind
        self.players[bb].in_chips = self.big_blind
        # The first player to action in pre-flop round is the UTG
        self.game_pointer = (bb + 1) % self.num_players
        # Pre-Flop round
        for i in range(2 * self.num_players):
            self.players[i % self.num_players].hand.append(self.dealer.deal_card())
        self.round.start_new_round(game_pointer=self.game_pointer, raised=[p.in_chips for p in self.players])

        # Save chance's deal action
        for i in range(1, self.num_players + 1):
            position = (self.button + i) % self.num_players
            deal_card = [card.get_index() for card in self.players[position].hand]
            self.game_tree.append(('c', 'deal_{}:{}'.format(position, deal_card)))

        state = self.get_state()
        return state, self.game_pointer

    def step(self, action):
        '''
        Get the next state

        Args:
            action (str or int): a specific action. (call, fold, check or raise(int))

        Ruturns:
            (tuple): Tuple containing:
                (PokerState): next player's state
                (int): next plater's id
        '''
        # If allowed, snapshot the current state
        if self.allow_step_back:
            r = deepcopy(self.round)
            b = deepcopy(self.game_pointer)
            r_c = deepcopy(self.round_counter)
            d = deepcopy(self.dealer)
            p = deepcopy(self.public_cards)
            ps = deepcopy(self.players)
            tr = deepcopy(self.game_tree)
            self.history.append((r, b, r_c, d, p, ps, tr))

        # Save the player's action
        self.game_tree.append((self.game_pointer, action))

        # Then proceed the action and get to the next state
        self.game_pointer = self.round.proceed_round(self.players, action)

        # If a round is over, we deal more public cards
        if self.round.is_over():
            # For the first round, we deal 3 cards
            if self.round_counter == 0:
                for _ in range(3):
                    self.public_cards.append(self.dealer.deal_card())
                self.game_tree.append(('c', 'deal_public:{}'.format([card.get_index() for card in self.public_cards])))

            # For the following rounds, we deal only 1 card
            elif self.round_counter <= 2:
                card = self.dealer.deal_card()
                self.public_cards.append(card)
                self.game_tree.append(('c', 'deal_public:{}'.format(card.get_index())))
            self.round_counter += 1
            # The first player to action in flop, turn, and river round is SB(if is alive).
            self.game_pointer = (self.button + 1) % self.num_players
            i = 1
            while self.players[self.game_pointer].status != 'alive':
                i += 1
                self.game_pointer = (self.game_pointer + 1) % self.num_players
                # No player is in status 'alive', game over or several players choose to all-in
                if i == self.num_players:
                    if not self.is_over():
                        # All Players choose all-in, deal remaining public cards and Showdown
                        self.round_counter = 4
                        deal_card = []
                        for _ in range(len(self.public_cards), 5):
                            self.public_cards.append(self.dealer.deal_card())
                            deal_card.append(self.public_cards[-1].get_index())
                        self.game_tree.append(('c', 'deal_public:{}'.format(deal_card)))

                    return {}, self.game_pointer
            self.round.start_new_round(self.game_pointer, raised=self.round.raised)
            # self.show_hint_info()

        state = self.get_state()
        return state, self.game_pointer

    def is_over(self):
        '''
        Check if the game is over

        Returns:
            (boolean): True if the game is over
        '''
        # only one player left
        alive_players = [1 if p.status != 'folded' else 0 for p in self.players]
        if sum(alive_players) == 1:
            return True
        # 4 round finished
        if self.round_counter >= 4:
            return True
        return False

    def step_back(self):
        '''
        Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        if len(self.history) > 0:
            self.round, self.game_pointer, self.round_counter, self.dealer, self.public_cards, self.players, self.game_tree = self.history.pop()
            return True
        return False

    def get_player_num(self):
        '''
        Return the number of players in the game

        Returns:
            (int): The number of players in the game
        '''
        return self.num_players

    def get_action_num(self):
        '''
        Return the number of possible actions in the game

        Returns:
            (int): The number of possible actions in the game
        '''
        if isinstance(self.init_chips, int):
            return self.init_chips + 3
        else:
            return max(self.init_chips) + 3

    def get_player_id(self):
        '''
        Return the current player's id

        Returns:
            (int): current player's id
        '''
        return self.game_pointer

    def get_state(self):
        '''
        Return the current player's state

        Returns:
            (PokerState): The observable state of the current player
        '''
        current_player = self.round.game_pointer
        state = PokerState(player_id=current_player,
                           pot=[p.in_chips for p in self.players],
                           hand_cards=self.players[current_player].hand,
                           public_cards=self.public_cards,
                           legal_actions=self.get_legal_actions())
        return state

    def get_final_state(self, player_id):
        '''
        Return the final state of specific player

        Returns:
            (dict): The observable state of the specific player
        '''
        current_player = self.round.game_pointer
        state = PokerState(player_id=current_player,
                           pot=[p.in_chips for p in self.players],
                           hand_cards=self.players[current_player].hand,
                           public_cards=self.public_cards,
                           legal_actions=[])
        return state

    def get_legal_actions(self):
        '''
        Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        '''
        return self.round.get_legal_actions(self.players)

    def get_payoffs(self):
        '''
        Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        # self.show_hint_info()
        # for p in self.players:
        #     if p.status != 'folded':
        #         print("Player{}'s hand:{}".format(p.get_player_id(), [card.get_index() for card in p.hand]))
        hands = [p.hand + self.public_cards if p.status != 'folded' else None for p in self.players]
        payoffs = self.judger.judge_game(self.players, hands)
        # payoffs = np.array(payoffs) / self.big_blind
        return payoffs

    def show_hint_info(self):
        '''
        Show hint infomation of the current game
        '''
        if not self.allow_hint_info_shown:
            return
        if self.round_counter == 0:
            round_name = 'Pre-Flop'
        elif self.round_counter == 1:
            round_name = 'Flop'
        elif self.round_counter == 2:
            round_name = 'Turn'
        elif self.round_counter == 3:
            round_name = 'River'
        else:
            round_name = 'Showdown'
        public_cards_str = [card.get_index() for card in self.public_cards]
        pot_chips = sum(self.round.raised)
        print("*** Current Round: {} // Public Cards: {} // Pot: {} ***".format(round_name, public_cards_str, pot_chips))

# test
# if __name__ == "__main__":
#     game = NoLimitTexasHoldemGame(num_players=6, init_chips=100)

#     while True:
#         print("New Game")
#         state, game_pointer = game.init_game(button=0)

#         while not game.is_over():
#             legal_actions = game.get_legal_actions()
#             action = random.choice(legal_actions)
#             print("Player{} choose {}".format(game_pointer, action))
#             state, game_pointer = game.step(action)

#         payoffs = game.get_payoffs()
#         print(payoffs)
#         print("Game ends")
