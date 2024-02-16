import argparse
import base64
import os
import random
import cv2
import numpy as np
import torch

from PIL import Image
from io import BytesIO


class DomainPredicate:
    def __init__(self, task):
        try:
            self.task = int(task)
        except ValueError:
            self.task = task

        self.task_number = {
            0: "bin_packing",
            1: "hanoi",
            2: "blocksworld",
            3: "cooking"
        }
        self.domain_predicate = {
            "bin_packing": [],
            "hanoi": ["clear", "on", "smaller", "move"],
            "blocksworld": ["on", "ontable", "clear", "handempty", "handfull", "holding"],
            "cooking": ["available", "is-whole", "is-sliced", "free", "carry", "can-cut", "at", "is-workspace"]
        }

        try:
            self.task = int(task)
            try:
                self.task = self.task_number[self.task]
            except:
                raise TaskError(self.task)
        except ValueError:
            self.task = task.lower()

    def return_predicate(self):
        try:
            predicates = self.domain_predicate[self.task]
        except:
            raise TaskError(self.task)
        return predicates


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
                        default="/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/val",
                        help="")
    parser.add_argument("--result_dir", type=str,
                        default="/home/changmin/PycharmProjects/GPT_examples/response",
                        help="")

    parser.add_argument("--task", type=str or int, default=None, help="domain name")
    parser.add_argument("--name", type=str, default=None, help="Experiment name")
    parser.add_argument("--input_image", type=str, default=None, help="image name from data_dir")

    # data_dir
    parser.add_argument("--api_json", type=str, default=None, help="")
    parser.add_argument("--example_prompt_json", type=str, default=None, help="")
    # parser.add_argument("--domain", action="store_true", help="Whether using domain.pddl or not.")
    # parser.add_argument("--problem", action="store_true", help="Whether using problem.pddl or not.")

    # related to problem generation and refinement
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    args = parser.parse_args()
    return args


def parse_args_v2():
    parser = argparse.ArgumentParser()

    # for main.py and evaluate.py
    parser.add_argument("--data_dir", type=str, default="./instructions", help="")
    parser.add_argument("--result_dir", type=str, default="./response", help="")
    parser.add_argument("--exp_name", type=str, default=None, help="Experiment name")
    parser.add_argument("--task_name", type=str or int, default=None, help="task name")

    # data_dir
    parser.add_argument("--api_json", type=str, default=None, help="")
    parser.add_argument("--example_prompt_json", type=str, default="./data", help="")
    parser.add_argument("--robot_json", type=str, default="./data", help="")

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


def numpy2b64(ndarray):
    pil_image = Image.fromarray(ndarray.astype('uint8'))
    image_io = BytesIO()
    image_binary = image_io.getvalue()
    base64_image = base64.b64encode(image_binary).decode('utf-8')

    return base64.b64encode(ndarray)


def b642numpy(b64code, h=480, w=640, c=3):
    r = base64.decodebytes(b64code)
    numpy_r = np.frombuffer(r, dtype=np.float64)
    image = np.reshape(numpy_r, (h, w))
    return image


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


def crop_image(image, xywh):
    real_h = image.shape[0]
    real_w = image.shape[1]
    x, y, w, h = xywh

    if real_h > real_w:
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        real_h = image.shape[0]
        real_w = image.shape[1]
        pass

    if x + w > real_w:
        print("insert value under", real_w, ", input: ", w)
        raise ValueError
    if y + h > real_h:
        print("insert value under", real_h, ", input: ", h)
        raise ValueError

    cropped_image = image[y: y + h, x: x + w, :]
    return cropped_image
