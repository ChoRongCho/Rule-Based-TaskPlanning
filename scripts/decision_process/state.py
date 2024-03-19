import numpy as np


class MDP:
    def __init__(self):
        # initial state
        self.update_v = np.zeros(np.array([4, 4]))
        self.old_v = np.zeros(np.array([4, 4]))

        # iteration sweep
        self.prob = 1 / 4
        self.reward = -1

        # Hyperparameter
        self.gamma = 0.99
        self.reward_size = -1
        self.grid_size = 4
        self.num_iter = 1000

        self.termination_state = [[0, 0], [self.grid_size - 1, self.grid_size - 1]]
        self.actions = [[-1, 0],
                        [1, 0],
                        [0, 1],
                        [0, -1]]

    def action_reward(self, init_state, action):
        if init_state in self.termination_state:
            return init_state, 0

        reward = self.reward_size

        # 각 action 에 대하여 state update
        final_state = np.array(init_state) + np.array(action)
        if -1 in final_state or 4 in final_state:
            final_state = init_state
        return final_state, reward

    def run(self):
        value_map = np.zeros((self.grid_size, self.grid_size))

        # generate possible state
        states = [[i, j] for i in range(self.grid_size) for j in range(self.grid_size)]

        deltas = []
        for iters in range(self.num_iter):
            copy_value_map = np.copy(value_map)
            delta_state = []

            for state in states:
                weighted_rewards = 0
                for action in self.actions:
                    final_state, reward = self.action_reward(state, action)
                    weighted_rewards += (1 / len(self.actions)) * (
                                reward + (self.gamma * value_map[final_state[0], final_state[0]]))

                delta_state.append(np.abs(copy_value_map[state[0], state[1]] - weighted_rewards))
                copy_value_map[state[0], state[1]] = weighted_rewards

            deltas.append(delta_state)
            value_map = copy_value_map

            if iters in [0, 1, 2, 9, 99, self.num_iter - 1]:
                print(f"Iteration {iters + 1}")
                print(value_map)
                print("")


def main():
    mdp = MDP()
    mdp.run()


if __name__ == '__main__':
    main()
