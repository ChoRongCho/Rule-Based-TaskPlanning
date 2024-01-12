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
    parser.add_argument("--task", type=str, default="bin_packing", help="domain name (bin_packing)")

    # data_dir
    parser.add_argument("--api_json", type=str, default=None, help="")
    parser.add_argument("--prompt_json", type=str, default=None, help="")
    parser.add_argument("--domain", type=bool, default=False, help="Whether using domain.pddl or not.")
    parser.add_argument("--problem", type=bool, default=False, help="Whether using problem.pddl or not.")

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

