import random

import numpy as np
from tabulate import tabulate
from scripts.predicates_prove.robot_database import Database


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

        self.def_table = [["Predicates List", "Definition"],
                          [self.active_predicates_list[0], "the fact of tending to break or be damaged easily"],
                          [self.active_predicates_list[1], "the fact of being very strict and difficult to change"],
                          [self.active_predicates_list[2], "the quality of changing shape easily when pressed"],
                          [self.active_predicates_list[3], "the ability to bend easily without breaking"],
                          [self.active_predicates_list[4], "the quality of returning to its original size and shape"]]

        self.database = Database(self.def_table)

    def print_definition_of_predicates(self):
        # print(tabulate(tabular_data=self.def_table, headers="firstrow", tablefmt="psql"))
        return tabulate(self.def_table)

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

    def random_active_search(self, obj_info):
        selected_predicates = self.random_predicates(obj_info)
        return selected_predicates

