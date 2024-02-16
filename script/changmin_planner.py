import json
from utils.utils import parse_args
import os

from database.database import Robot
from gpt_model.gpt_prompt import GPTInterpreter
from visual_interpreting.visual_interpreting import FindObjects
from groundingdino.util.inference import load_model


class ChangminPlanner:
    def __init__(self, args):
        # basic setting
        self.args = args
        self.task_info = self.get_json_data(os.path.join("/home/changmin/PycharmProjects/GPT_examples", "task_instruction.json"))[args.task]
        print(self.task_info)
        # self.object_detection = FindObjects(args=args)

    def run_planner(self):
        detected_object, detected_object_types = self.object_detection.run_find_obj()
        print(detected_object)
        print(detected_object_types)


    @staticmethod
    def get_json_data(json_path):
        with open(json_path, "r") as file:
            data = json.load(file)
        return data


def main():
    args = parse_args()
    planner = ChangminPlanner(args=args)


if __name__ == '__main__':
    main()
