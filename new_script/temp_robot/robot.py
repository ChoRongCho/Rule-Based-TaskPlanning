import random


class Robot:
    # Define skills
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions

        self.robot_handempty = True
        self.robot_now_holding = False
        self.robot_base_pose = True

        self.active_predicates_list = ["is_fragile",
                                       "is_rigid",
                                       "is_soft",
                                       "is_flexible",
                                       "is_foldable",
                                       "is_elastic"]

    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False

    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False

    # basic state
    def state_base(self):
        self.robot_base_pose = True

    # bin_packing, cooking
    def pick(self, obj):
        # make a preconditions for actions
        print(f"Pick {obj.name}")

    # bin_packing, cooking
    def place(self, obj, bins):
        # make a preconditions for actions
        print(f"Place {obj.name} in {bins.name}")

    # bin_packing
    def push(self, obj):
        # make a preconditions for actions
        print(f"Push {obj.name}")

    # bin_packing
    def fold(self, obj):
        # make a preconditions for actions
        print(f"Fold {obj.name}")

    def out(self, obj, bins):
        # make a preconditions for actions
        print(f"Out {obj.name} from {bins.name}")

    def random_predicates(self, obj_info):
        selected_predicates = random.sample(self.active_predicates_list, k=random.randint(1, 2))
        if 'is_rigid' in selected_predicates and 'is_soft' in selected_predicates:
            return self.random_predicates(obj_info)
        return selected_predicates

    def active_search(self, obj_info):
        selected_predicates = self.random_predicates(obj_info)
        return selected_predicates


def main():
    robot = Robot()

    result_dict = {}
    input_dict = {0: {'white box': [509, 210, 231, 323]},
                  1: {'blue object': [204, 220, 361, 247]},
                  2: {'yellow object': [83, 158, 135, 216]},
                  3: {'brown object': [257, 95, 139, 148]}}

    for key, value in input_dict.items():
        info = robot.active_search(value)
        result_dict.update({key: info})

    print(result_dict)

    tempt_list = list(result_dict.values())
    flattened_list = [item for sublist in tempt_list for item in sublist]
    unique_list = list(set(flattened_list))
    print(unique_list)


if __name__ == '__main__':
    main()
