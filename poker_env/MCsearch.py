class MonteCarloTreeSearch(object):

    def __init__(self, node):
        '''
        
        Args:
            node : poker_env.MCnode.RealtimeSearchMCTSNode

        '''
        self.root = node

    def best_action(self, node, simulations_number):
        '''
        Step forward

        Args:
            simulations_number (int): number of simulations performed to get the best action
        TODO: now return is node, it should be action
        Returns:
            (node): best child
        
        '''
        for _ in range(0, simulations_number):            
            v = self._tree_policy(node)
            reward = v.rollout()
            v.backpropagate(reward)
        # to select best child go for exploitation only
        return node.best_child(c_param=100.)

    def _tree_policy(self, current_node):
        '''
        selects node to run rollout/playout for

        Args:
            current_node : poker_env.MCnode.RealtimeSearchMCTSNode

        Returns:
            (node): best_uct_child if fully expand else 
        '''
        # current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
