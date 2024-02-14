import json
import os
import re
from datetime import datetime

from tabulate import tabulate
from groundingdino.util.inference import load_model
from script.gpt_model.gpt_prompt import GPTInterpreter
from script.database.database import Robot, Domain
from script.utils.utils import RobotKeyError

task_number_table = {
    0: "bin_packing",
    1: "hanoi",
    2: "blocksworld",
    3: "cooking"
}


class PDDLv2:
    def __init__(self,
                 args,
                 human_instruction: str):
        """
        Generating PDDL files

        :param args: arguments for making a problem.pddl and a domain.pddl
        :param human_instruction: perhaps
        input1: scene observation: problem을 만들기 위한 정보
        input2: env information: 환경에 관한 정보
        input3: task information: 하려는 task에 대한 정보
        input4: basic pddl information: pddl에 관한 정보
        input5: robot description: 로봇 정보
        """

        self.args = args
        self.human_instruction = human_instruction

        self.exp_name = args.name
        self.task_name = args.task_name
        self.predicates = None
        self.gpt4 = GPTInterpreter(
            api_json=args.api_json,
            prompt_json=args.prompt_json,
            result_dir=args.result_dir,
            version="pddl"
        )

        self.robot = Robot()

    def print_args(self):
        table = [["Project Time", datetime.now()],
                 ["Task", self.task_name],
                 ["Exp Name", self.exp_name],
                 ["Predicates", self.predicates],
                 ["Robot Actions", list(self.robot.actions.keys())],
                 ]
        print(tabulate(table))

    def get_robot_information(self):
        """

        :return:
        """
        robot_json_path = os.path.join(self.args.data_dir, self.exp_name, "robot_description.json")
        try:
            with open(robot_json_path, "r") as robot_json_file:
                robot_info = json.load(robot_json_file)
                try:
                    # save robot information
                    self.robot.name = robot_info["name"]
                    self.robot.goal = robot_info["goal"]
                    self.robot.actions = robot_info["actions"]
                except:
                    raise RobotKeyError(robot=self.robot)
            robot_json_file.close()
        except:
            raise FileNotFoundError(f"There is no file in {robot_json_path}")


class DomainGen:
    """
    Input:
    1. robot information,
    2. prompt examples
    """
    def __init__(self,
                 args,
                 robot: Robot):

        self.args = args
        self.robot = robot

        self.task_name = args.task_name
        self.mode: str = args.mode

        # initialize
        self.domain_info = Domain(types={},
                                  requirements="",
                                  predicates="",
                                  actions={})

        # Get prompt examples
        # self.args.data_dir = "/home/changmin/PycharmProjects/GPT_examples/data"
        self.prompt_file = os.path.join(self.args.data_dir, self.task_name, self.task_name + ".json")
        with open(self.prompt_file, "r") as file:
            self.prompt_text_data = json.load(file)

            self.task_description = self.prompt_text_data["script"]["task_description"]
            # self.vision_prompt = self.prompt_text_data["script"]["vision_prompt"]
            # self.behaviour_prompt = self.prompt_text_data["script"]["behaviour_prompt"]
            # self.action_prompt = self.prompt_text_data["script"]["action_prompt"]
            # self.pddl_prompt = self.prompt_text_data["script"]["pddl_prompt"]

            file.close()

        # Get domain info
        self.domain_info.actions = self.robot.actions

        # Get Visual Interpreter
        self.model_dir = "/home/changmin/PycharmProjects/research/GroundingDINO"
        self.gd_dir = os.path.join(self.model_dir, "groundingdino/config/GroundingDINO_SwinT_OGC.py")
        self.check_dir = os.path.join(self.model_dir, "weights/groundingdino_swint_ogc.pth")
        self.model = load_model(self.gd_dir, self.check_dir)
        self.BOX_THRESHOLD = 0.35
        self.TEXT_THRESHOLD = 0.25

        text_phrases = [
            "blue disk",
            "green disk",
            "yellow disk",
            "purple disk",
            "orange disk",
            "pink disk",
            "wooden stick",
        ]

        self.TEXT_PROMPT = "".join([
            phrase + " ."
            for phrase in text_phrases
        ])

        # GPT4
        self.gpt4 = GPTInterpreter(
            api_json=args.api_json,
            prompt_json=False,
            result_dir=args.result_dir,
            version="vision"
        )

    def visual_interpreter(self, image_urls: list or str):
        prompt = f"We are now doing a {self.task_name} task. \nThese are the observations where I'm going to work. \n"
        prompt += "What objects or tools are here? \n"

        self.gpt4.add_message_manual(role="user", content=prompt, image_url=image_urls)
        answer = self.gpt4.run_manual_prompt(name="", is_save=False)
        print(answer)

    def modify_text_prompt(self, text_prompt: str):
        self.TEXT_PROMPT = text_prompt

    def divide_object_types(self, objects_list, example_prompt: list):
        """

        :param example_prompt:
        :param objects_list: ["", "", "", ""]
        :return:self.domain_info.types

        """
        if self.mode.lower() == "llm":
            prompt = f"We are now going to do {self.task_name} which is {self.task_description}. \n"
            prompt += "There are many objects in interest such as "
            for obj in objects_list:
                if obj == objects_list[-1]:
                    prompt += "and " + "obj" + ". \n"
                else:
                    prompt += obj + ", "
            prompt += "Divide the character of the object according to the task. \n"
            self.gpt4.message = example_prompt
            self.gpt4.add_message_manual(role="user", content=prompt)
            answer = self.gpt4.run_manual_prompt(name="", is_save=False)

            def type_parser(type_answer: str, types: dict):
                pattern = re.compile(r'(\d+)\.\s*([\w\s]+):\s*([^\.]+)\.')
                matches = pattern.findall(type_answer)
                for match in matches:
                    index, type_name, type_val = match
                    type_name = type_name.lower().strip()
                    type_val = [value.strip() for value in type_val.split(',')]
                    types[type_name] = type_val
                return types
            self.domain_info.types = type_parser(answer, self.domain_info.types)

        elif self.mode.lower() == "manual":
            if self.task_name == "bin_packing":
                self.domain_info.types = {"bin": [], "object": []}
            elif self.task_name == "blocksworld":
                self.domain_info.types = {"block": [], "table": []}
            elif self.task_name == "hanoi":
                self.domain_info.types = {"disk": [], "peg": []}
            elif self.task_name == "cooking":
                self.domain_info.types = {"ingredient": [], "tool": [], "location": []}
            else:
                raise ValueError(f"Task name {self.task_name} is wrong. ")

        else:
            raise ValueError(f"Mode {self.mode} is wrong: LLM or manual. ")

    def define_actions(self, robot: Robot):
        pass

    def define_domain(self):

        pass


    def define_planning(self):
        pass


    def generate_domain(self):
        pass


class ProblemGen:
    def __init__(self, args):
        self.args = args

    def define_available_objects(self):
        pass

    def define_init_state(self):
        pass

    def define_goal_state(self):
        pass

    def run(self):
        pass
