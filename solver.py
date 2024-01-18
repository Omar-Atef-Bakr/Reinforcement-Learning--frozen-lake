import math
import time

LEFT_INDEX = 0
UP_INDEX = 1
RIGHT_INDEX = 2
DOWN_INDEX = 3
PENALTY = -1
REWARD = 100
OBSTACLE_PENALTY = -100
STUCK_VALUE = -100
#ITERATIONS = 100

class Solver:
    def __init__(self, board):
        # flatten board
        self.BOARD = [cell for row in board for cell in row]
        # print(len(self.BOARD))
        self.size = len(board)
        self.ITERATIONS = int((self.size**2) * (2.5/3))

        self.policy = []
        self.value = []
        self.solvable = [False] * self.size**2

        # initialize policy and value functions
        # print("-" * 50)
        # print("AI initial state:")
        # print("Board: ", self.BOARD)
        # print("Policy: ", self.policy)
        # print("Value: ", self.value)
        # print("-" * 50)

    def initialize_policy_and_value_functions(self):
        self.policy = []
        self.value = []

        for i in range(len(self.BOARD)):
            # skip obstacles
            if self.BOARD[i] == 1:
                self.policy.append(None)
                self.value.append(None)
                continue

            # cell policy
            self.policy.append([0.25] * 4)  # left, up, right, down equal probabilities

            # cell value
            val = 0
            self.value.append(val)

    # Value Iteration Algorithm
    def value_iteration(self):
        # Initialize policy and value functions
        self.initialize_policy_and_value_functions()

        new_values = [0] * len(self.BOARD)

        # Value iteration loop
        iter = 0
        start_time = time.time()
        while True:
            if iter % 5 == 0:
                print("Value iteration: ", iter, ": ", self.value)
                print()
            iter += 1

            delta = 0
            for s in range(1, len(self.BOARD)):
                # skip obstacles
                if self.BOARD[s] == 1:
                    continue

                # old value
                v = self.value[s]

                # new value
                actions = self.get_actions(s)
                if len(actions) == 0:
                    new_values[s] = STUCK_VALUE
                else:
                    new_values[s] = max(self.get_q_value(s, a) for a in actions)

                # check for solvability
                if not self.solvable[s]:
                    for a in range(4):
                        ns = self.get_next_state(s, a)
                        if ns == 0 or self.solvable[ns]:
                            self.solvable[s] = True

                if self.solvable[s]:
                    delta = max(delta, abs(v - new_values[s]))

            # check for convergence
            self.value = new_values
            if delta < 1e-4:
                break
            delta = 0

        # Policy improvement
        self.policy_improvement()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time for value iteration: ", elapsed_time, " seconds")

        return self.value

    def get_actions(self, s):

        if s == 0:
            return []

        actions = []
        if s % self.size > 0 and self.BOARD[s - 1] != 1:
            actions.append(LEFT_INDEX)
        if s >= self.size and self.BOARD[s - self.size] != 1:
            actions.append(UP_INDEX)
        if s % self.size < self.size - 1 and self.BOARD[s + 1] != 1:
            actions.append(RIGHT_INDEX)
        if s < self.size * (self.size - 1) and self.BOARD[s + self.size] != 1:
            actions.append(DOWN_INDEX)

        return actions

    def get_q_value(self, s, a):
        # get next state
        next_state = self.get_next_state(s, a)

        # get reward
        reward = PENALTY

        # get value
        value = self.value[next_state]

        return reward + value

    def get_next_state(self, s, a):
        # get next state
        next_state = s
        if a == LEFT_INDEX:
            if s % self.size > 0:
                next_state = s - 1
        elif a == UP_INDEX:
            if s >= self.size:
                next_state = s - self.size
        elif a == RIGHT_INDEX:
            if s % self.size < self.size - 1:
                next_state = s + 1
        elif a == DOWN_INDEX:
            if s < self.size * (self.size - 1):
                next_state = s + self.size

        # if next state is blocked return current state
        if self.BOARD[next_state] == 1:
            return s

        return next_state

    def policy_improvement(self):
        policy_stable = True

        for s in range(len(self.BOARD)):
            # skip obstacles
            if self.BOARD[s] == 1:
                continue

            # old action
            old_policy = self.policy[s]

            # new action
            new_policy = self.get_best_policy(s)

            # update policy
            self.policy[s] = new_policy

            # check if policy is stable
            if self.solvable[s] and old_policy != new_policy:
                policy_stable = False

        # self.policy[0] = None
        return policy_stable

    def get_best_policy(self, s):
        best_values = [self.get_q_value(s, a) for a in range(4)]

        # policy = [-val/sum(best_values) for val in best_values]
        policy = [1 if val == max(best_values) else 0 for val in best_values]
        return policy

    # Policy Iteration Algorithm
    def policy_iteration(self):
        # Initialize policy and value functions
        self.initialize_policy_and_value_functions()

        # Policy iteration loop
        start_time = time.time()
        for i in range(self.ITERATIONS):
            if i%5 == 0:
                print(f"Policy Iteration {i}: values={self.value}")
                print()
            # Policy evaluation
            self.policy_evaluation()

            # Policy improvement
            if self.policy_improvement():
                break
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time for policy iteration: {elapsed_time} seconds")
        return self.value

    def policy_evaluation(self):
        new_values = [0] * len(self.BOARD)

        # Policy evaluation loop

        for s in range(1, len(self.BOARD)):
            # skip obstacles
            if self.BOARD[s] == 1:
                continue

            # old value
            v = self.value[s]

            if not self.solvable[s]:
                for a in range(4):
                    ns = self.get_next_state(s, a)
                    if ns == 0 or self.solvable[ns]:
                        self.solvable[s] = True

            # new value
            new_values[s] = sum([self.get_q_value(s, a) for a in range(4)]) / 4

        # check for convergence
        self.value = new_values

    def get_best_action(self, s):
        best_action = None
        best_value = -math.inf

        for a in range(4):
            q_value = self.get_q_value(s, a)
            if q_value > best_value:
                best_value = q_value
                best_action = a

        return best_action

    def policy_representation(self):
        policy = [None]
        map = {
            RIGHT_INDEX: 'R',
            LEFT_INDEX: 'L',
            UP_INDEX: 'U',
            DOWN_INDEX: 'D'
        }

        for i in range(1, len(self.policy)):
            if not self.solvable[i]:
                policy.append('S')
                continue

            if self.policy[i] is None:
                policy.append(None)
            else:
                index = self.policy[i].index(max(self.policy[i]))
                policy.append(map[index])

        return policy
