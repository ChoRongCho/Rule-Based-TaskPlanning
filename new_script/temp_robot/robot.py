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
        elif "is_soft" in selected_predicates and "is_fragile" in selected_predicates:
            return self.random_predicates(obj_info)
        return selected_predicates

    def active_search(self, obj_info):
        selected_predicates = self.random_predicates(obj_info)
        return selected_predicates

