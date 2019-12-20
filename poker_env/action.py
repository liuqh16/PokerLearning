from enum import Enum


class AbstractAction(Enum):
    '''
    A Enum that contains all availabel actions after abstraction
    '''
    FOLD = 0
    CHECK = 1
    CALL = 2
    RAISE_HALF_POT = 3
    RAISE_POT = 4
    RAISE_2POT = 5
    ALL_IN = 6

    def translate_from(self, state):
        '''
        Translate the abstract action into specific legal action in the state.

        Args:
            state (PokerState): the target state

        Returns:
            (str): specific legal action
        '''
        total_pot = sum(state.pot)
        legal_actions = state.legal_actions

        if self == AbstractAction.FOLD:
            action_str = 'fold'
        elif self == AbstractAction.CHECK:
            action_str = 'check'
        elif self == AbstractAction.CALL:
            action_str = 'call'
        elif self == AbstractAction.RAISE_HALF_POT:
            action_str = 'raise{}'.format(int(0.5 * total_pot))
        elif self == AbstractAction.RAISE_POT:
            action_str = 'raise{}'.format(int(total_pot))
        elif self == AbstractAction.RAISE_2POT:
            action_str = 'raise{}'.format(int(2 * total_pot))
        else:
            action_str = 'all-in'

        # fold, check, call, raise
        if action_str in legal_actions:
            return action_str
        # Do not have enough chips
        else:
            return 'all-in'


# from state import PokerState
# if __name__ == "__main__":
#     legal_actions = ['fold', 'call', 'all-in']
#     for i in range(4, 100):
#         legal_actions.append('raise{}'.format(i))
#     temp_state = PokerState(player_id=0,
#                             pot=[10 for _ in range(6)],
#                             hand_cards=[],
#                             public_cards=[],
#                             legal_actions=legal_actions)
#     a = [_ for _ in AbstractAction]
#     print(a[3])
#     print(a[3].translate_from(temp_state))
