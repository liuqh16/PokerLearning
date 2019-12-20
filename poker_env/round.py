class NoLimitTexasHoldemRound:
    '''
    The Round class for No Limit Texas Hold'em Poker.
    Round can call other Classes' functions to keep the game running.
    '''
    def __init__(self, num_players=6, init_raise_amount=2):
        '''
        Initialize a round class.

        Args:
            num_players (int): The number of players
            init_raise_amount (int): The min raise amount when every round starts
        '''
        self.game_pointer = None
        self.num_players = num_players
        self.init_raise_amount = init_raise_amount
        self.current_raise_amount = self.init_raise_amount

        # Count the number without raise
        # If every alive player agree to not raise, the round is over.
        self.not_raise_num = 0
        self.all_in_player_num = 0
        self.alive_player_num = self.num_players

        # Raised amount for each player
        self.raised = [0 for _ in range(self.num_players)]

        # Save the history for stepping back to the last state.
        # self.history = []

    def start_new_round(self, game_pointer, raised=None):
        '''
        Start a new bidding round

        Args:
            game_pointer (int): The index of the current player.
            raised (list): Initialize the chips for each player

        Note: For the first round of the game, we need to setup the big/small blind
        '''
        self.game_pointer = game_pointer
        self.not_raise_num = 0
        self.current_raise_amount = self.init_raise_amount
        if raised:
            self.raised = raised
        else:
            self.raised = [0 for _ in range(self.num_players)]

    def proceed_round(self, players, action):
        '''
        Call other Classes' functions to keep one round running

        Args:
            players (list): The list of players that play the game
            action (str): An legal action taken by the player

        Returns:
            (int): The game_pointer that indicates the next player
        '''
        if 'raise' in action:
            rebet_amount = int(action[5:])
            call_amount = max(self.raised) - self.raised[self.game_pointer]
            self.raised[self.game_pointer] += rebet_amount
            players[self.game_pointer].in_chips += rebet_amount
            self.not_raise_num = 1
            self.current_raise_amount = rebet_amount - call_amount

        elif action == 'call':
            call_amount = max(self.raised) - self.raised[self.game_pointer]
            self.raised[self.game_pointer] += call_amount
            players[self.game_pointer].in_chips += call_amount
            self.not_raise_num += 1

        elif action == 'fold':
            players[self.game_pointer].status = 'folded'
            self.alive_player_num -= 1

        elif action == 'check':
            self.not_raise_num += 1

        elif action == 'all-in':
            call_amount = max(self.raised) - self.raised[self.game_pointer]
            all_in_amount = players[
                self.game_pointer].init_chips - self.raised[self.game_pointer]
            self.raised[self.game_pointer] += all_in_amount
            players[self.game_pointer].in_chips += all_in_amount
            players[self.game_pointer].status = 'all-in'
            self.all_in_player_num += 1
            if all_in_amount > call_amount:
                self.not_raise_num = 0
            self.current_raise_amount = max(all_in_amount - call_amount,
                                            self.current_raise_amount)

        # game over
        if self.all_in_player_num == self.alive_player_num:
            return -1

        self.game_pointer = (self.game_pointer + 1) % self.num_players
        # Skip the folded players and the all_in players
        while players[self.game_pointer].status != 'alive':
            self.game_pointer = (self.game_pointer + 1) % self.num_players
        return self.game_pointer

    # Deprecated!
    # def step_back(self, players, player_id, action):
    #     '''
    #     ()
    #     Restore the round before the specified action happens

    #     Args:
    #         players (list): The list of players that play the game
    #         player_id (int): The id of the player whose action need to be restored
    #         action (str or int): An legal action has been taken by the player
    #     '''
    #     pass

    def get_legal_actions(self, players):
        '''
        Obtain the legal actions for the current player

        Args:
            players (list): The players in the game

        Returns:
           (list):  A list of legal actions
        '''
        full_actions = ['fold']
        call_amount = max(self.raised) - self.raised[self.game_pointer]
        remained_chips = players[self.game_pointer].get_remained_chips()

        # If the current player has put in the chips that are more than others, he can check.
        if call_amount == 0:
            full_actions.append('check')
        # If the current player cannot provide call amount, he has to all-in or fold.
        elif call_amount >= remained_chips:
            return ['fold', 'all-in']
        # If the current chips are less than that of the highest one in the round, he can call.
        elif call_amount > 0:
            full_actions.append('call')

        # Append available raise amount to the action list
        min_raise_amount = call_amount + self.current_raise_amount
        # If the current player cannot provide min raise amount, he has to all-in or fold.
        if min_raise_amount >= remained_chips:
            full_actions.append('all-in')
        else:
            for available_raise_amount in range(min_raise_amount,
                                                remained_chips):
                full_actions.append('raise{}'.format(available_raise_amount))
            full_actions.append('all-in')

        return full_actions

    def is_over(self):
        '''
        Check whether the round is over.

        Returns:
            (boolean): True if the current round is over
        '''
        if self.not_raise_num == (self.alive_player_num -
                                  self.all_in_player_num):
            return True
        else:
            return False

    def get_action_player_num(self):
        '''
        Return the number of players who can action

        Returns:
            (int): the result number
        '''
        return self.alive_player_num - self.alive_player_num


# # test
# import numpy as np
# import random
# from player import NoLimitTexasHoldemPlayer as Player

# if __name__ == "__main__":
#     num_players = 2
#     big_blind = 2
#     small_blind = 1

#     players = [Player(i, 15) for i in range(num_players)]
#     s = 1
#     b = 0
#     players[s].in_chips = small_blind
#     players[b].in_chips = big_blind

#     game_pointer = 1
#     r = NoLimitTexasHoldemRound(num_players=num_players, init_raise_amount=big_blind)
#     r.start_new_round(game_pointer=game_pointer, raised=[p.in_chips for p in players])

#     # r.proceed_round(players, 3)
#     # r.proceed_round(players, 6)
#     # r.proceed_round(players, 8)
#     # r.proceed_round(players, 'call')
#     # r.proceed_round(players, 'check')
#     # r.proceed_round(players, 'check')

#     while not r.is_over():
#         legal_actions = r.get_legal_actions(players)
#         action = random.choice(legal_actions)
#         if isinstance(action, int):
#             print(game_pointer, 'raise{}'.format(action))
#         else:
#             print(game_pointer, action)
#         game_pointer = r.proceed_round(players, action)
#         print(r.raised, '{}/{}'.format(r.not_raise_num+r.all_in_player_num, r.alive_player_num))
