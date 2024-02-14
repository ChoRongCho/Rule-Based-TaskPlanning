import json
import os
from database.database import Robot
from gpt_model.gpt_prompt import GPTInterpreter
from groundingdino.util.inference import load_model


class ChangminPlanner:
    def __init__(self, args):
        # basic setting
        self.args = args
        self.task_name = args.task_name
        self.exp_name = args.name

        # json path
        self.robot_json_path = os.path.join(args.robot_json, "robot.json")
        self.prompt_example_path = os.path.join(args.prompt_json, "prompt_examples.json")
        self.task_prompt_path = os.path.join(args.prompt_json, self.task_name, self.task_name + ".json")

        # get robot_information from json_file
        robot_data = self.get_json_data(self.robot_json_path)
        robot_data = robot_data[self.task_name]
        self.robot = Robot(name=robot_data["name"],
                           goal=robot_data["goal"],
                           actions=robot_data["actions"])

        # get prompt_examples
        self.prompt_examples = self.get_json_data(self.prompt_example_path)
        self.task_prompt = self.get_json_data(self.task_prompt_path)

        # gpt4 initialize
        self.gpt4_vision = GPTInterpreter(
            api_json=args.api_json,
            prompt_json=False,
            result_dir=args.result_dir,
            version="vision"
        )

        self.gpt4_text = GPTInterpreter(
            api_json=args.api_json,
            prompt_json=False,
            result_dir=args.result_dir,
            version="pddl"
        )

        # Get Visual Interpreter
        self.model_dir = "/home/changmin/PycharmProjects/research/GroundingDINO"
        self.gd_dir = os.path.join(self.model_dir, "groundingdino/config/GroundingDINO_SwinT_OGC.py")
        self.check_dir = os.path.join(self.model_dir, "weights/groundingdino_swint_ogc.pth")
        self.model = load_model(self.gd_dir, self.check_dir)
        self.BOX_THRESHOLD = 0.35
        self.TEXT_THRESHOLD = 0.25

        self.TEXT_PROMPT = "".join([
            phrase + " ."
            for phrase in text_phrases
        ])

        # Domain Generator


    @staticmethod
    def get_json_data(json_path):
        with open(json_path, "r") as file:
            data = json.load(file)
        return data
