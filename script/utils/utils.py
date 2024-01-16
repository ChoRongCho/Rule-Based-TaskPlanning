import argparse
import os
import random

import numpy as np
import torch


def seed_all_types(seed: int = 42):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True


def parse_args():
    parser = argparse.ArgumentParser()

    # for main.py and evaluate.py
    parser.add_argument("--data_dir", type=str,
                        default="/home/changmin/PycharmProjects/GPT_examples/instructions",
                        help="")
    parser.add_argument("--result_dir", type=str,
                        default="/home/changmin/PycharmProjects/GPT_examples/response",
                        help="")
    parser.add_argument("--name", type=str, default=None, help="")
    parser.add_argument("--task", type=str or int, default=None, help="domain name")

    # data_dir
    parser.add_argument("--api_json", type=str, default=None, help="")
    parser.add_argument("--prompt_json", type=str, default=None, help="")
    parser.add_argument("--domain", action="store_true", help="Whether using domain.pddl or not.")
    parser.add_argument("--problem", action="store_true", help="Whether using problem.pddl or not.")

    # related to problem generation and refinement
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    args = parser.parse_args()
    return args


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


class TaskError(Exception):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def __str__(self):
        return "{} is a invalid number or task, 0: bin packing, 1: hanoi, 2: blocksworld, 3: cooking".format(self.value)


class RobotKeyError(Exception):
    def __init__(self, robot):
        super().__init__(robot)
        self.robot = robot

    def __str__(self):
        return "Three below were not met: name, goal, actions."


class JsonFileContentError(Exception):
    def __init__(self, json_path):
        super().__init__(json_path)
        self.json_path = json_path

    def __str__(self):
        return f"There is no content in {self.json_path}. "

