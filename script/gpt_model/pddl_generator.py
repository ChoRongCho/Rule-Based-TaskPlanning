import json
import os
import random
from dataclasses import dataclass
from typing import List
from gpt_prompt import GPTInterpreter

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


@dataclass
class Robot:
    name: str = "UR5"
    purpose: str = None
    actions: dict = None


class PDDL:
    def __init__(self,
                 args,
                 predicates: list
                 ):
        """
        1. robot description: there is an action set that the robot can do.
        2. domain_pddl: if None, make new domain.pddl else, add task
        3. problem_pddl: if None, make a new problem.pddl file from instruction, else, modifying problem.pddl
        4. human instruction: common sense

        get predicates + (human_instruction + action set) + (domain.pddl + problem.pddl) => new domain or problem.pddl


        """
        # basic
        self.args = args
        self.predicates = predicates

        # utils
        self.name = args.name
        self.save_path = args.save_path

        # task definition
        self.task = args.task

        # GPT Client
        self.gpt4 = GPTInterpreter(api_json=self.args.api_json,
                                   prompt_json=self.args.prompt_json,
                                   save_path=self.args.save_path)

        # robot
        self.robot = Robot()
        self.get_robot_information()

        # pddl
        self.domain = self.args.domain  # ture or false
        self.problem = self.args.problem  # ture or false
        self.domain_prompt = self.get_example_pddl(self.domain)
        self.problem_prompt = self.get_example_pddl(self.problem)

        # human instruction
        self.human_instruction = self.get_human_instruction()

        # message
        self.prompt_predicates = ""
        self.prompt_instruction = ""
        self.prompt_pddl = ""

        self.message = []

    def get_robot_information(self) -> Robot:
        """

        :return:
        """
        if self.task == "bin_packing" or self.task == 0:
            task = "bin_packing"
            robot_json_path = os.path.join(self.args.path, task, "robot_description.json")
            with open(robot_json_path, "r") as robot_json_file:
                robot_info = json.load(robot_json_file)
                try:
                    # save robot information
                    self.robot.name = robot_info["name"]
                    self.robot.purpose = robot_info["purpose"]
                    self.robot.actions = robot_info["actions"]
                except:
                    raise KeyError("Three below were not met: name, purpose, actions.")

            robot_json_file.close()

        # add your new task
        # elif task == "" or task == 1:
        #     pass

        else:
            raise ValueError("task Error: 0: Bin_Packing")

    def get_human_instruction(self) -> str:
        """

        :return:
        """
        if self.task == "bin_packing" or self.task == 0:
            task = "bin_packing"
            hi_json_path = os.path.join(self.args.path, task, "instructions.json")
            with open(hi_json_path, "r") as hi_json_file:
                hi_info = json.load(hi_json_file)
                content_list = []
                try:
                    # add get info code
                    human_prompt = sorted(hi_info["prompt"], key=lambda x: x['index'])
                    for i in range(len(human_prompt)):
                        content_text = human_prompt[i]["content"]
                        content_list.append(content_text)
                    content = "".join(content_list)
                    print("\n\n---- Human Instruction ----")
                    print(content)
                    print("---- Human Instruction ----\n\n")
                except:
                    raise KeyError("There is no content.")

            hi_json_file.close()
            return content

        # add your new task
        # elif task == "" or task == 1:
        #     pass

        else:
            raise ValueError("task Error: 0: Bin_Packing")

    def get_example_pddl(self, pddl: str = "domain") -> List or bool:
        """


        :param pddl:
        :return:
        """
        if self.task == "bin_packing" or self.task == 0:
            task = "bin_packing"
        else:
            raise ValueError("task Error: 0: Bin_Packing")

        if pddl.lower() == "domain":
            if self.domain:
                pddl_path = os.path.join(self.args.path, task, "domain.pddl")
                content = self.pddl_format(pddl_path, json_key="answer")

            else:
                content = False

        elif pddl.lower() == "problem":
            if self.problem:
                pddl_path = os.path.join(self.args.path, task, "problem.pddl")
                content = self.pddl_format(pddl_path, json_key="answer")
            else:
                content = False
        else:
            raise ValueError("Domain or Problem")

        return content

    @staticmethod
    def pddl_format(pddl_path: str, json_key: str) -> str:
        if pddl_path.lower().endswith('.json'):
            with open(pddl_path, "r") as file:
                pddl_info = json.load(file)
                content = "".join(list(pddl_info[json_key]))

        elif pddl_path.lower().endswith('.txt'):
            file = open(pddl_path, "r")
            lines = file.readlines()
            content = "".join(lines)

        elif pddl_path.lower().endswith('.pddl'):
            file = open(pddl_path, "r")
            lines = file.readlines()
            content = "".join(lines)
        else:
            raise TypeError("json, text or pddl extensions are needed.")

        file.close()
        return content

    def prompt_encoding(self):
        """
        make a prompt
        1. self.prompt_predicates: task_description + predicates
        2. self.prompt_instruction: human_instruction + given action set
        3. self.prompt_pddl: example pddl if existed

        :return: total prompt
        """
        """ ----------------------------------- """
        # Added instruction
        if self.task == "bin_packing" or 0:
            task = "bin packing"

            # Intro, inform GPT what will do.
            message = f"Hi, my name is {self.robot.name}, and I am a robot. \n"
            message += f"Our goal is to pack a set of objects into a box, which is called {task}. " + \
                       "In a problem instance, there is a box, a manipulator robot(it's me!), and objects set. \n"

            # Add predicates
            if len(self.predicates) == 0:
                message += "Actions must consider the predicates in preconditions and effects. \n"

            else:
                message += "We want to consider physical properties of the objects such as "
                for predicate in self.predicates:
                    if predicate == self.predicates[-1]:
                        message += "and " + predicate + ". \n"
                    else:
                        message += predicate + ", "

                message += "Given this goal, I want to make a domain.pddl" + \
                           " considering the physical properties of the objects. " + \
                           f"The domain file is supposed to include predicates such as is_{self.predicates[0]}. " + \
                           "Actions must consider the predicates in preconditions and effects. \n"
            self.prompt_predicates = message

            """ ----------------------------------- """
            # Add Human instruction, message reset
            message = "Now, I'm going to talk about precautions when doing bin packing. \n"
            message += self.human_instruction
            message += " \n"

            # Add actions when making actions
            message += "The actions I can do are "
            for action in self.robot.actions:
                if action == self.robot.actions[-1]:
                    message += "and " + action + ". \n"
                else:
                    message += action + ", "
            message += "When you define action in domain.pddl, you must use that action set. No other actions is permitted. \n"
            self.prompt_instruction = message

            """ ----------------------------------- """
            # Add example pddl if it existed, message reset
            if self.problem_prompt:
                message = "Here is an example of a problem.pddl. \n"
                message += self.problem_prompt
                message += " \n" + \
                           "The initial state and goal state will be given like this. \n"

            if self.domain_prompt:
                message += "Here is an example of a domain.pddl. \n"
                message += self.domain_prompt
                message += " \n" + \
                    "Refer to this pddl and make a new domain.pddl "
            self.prompt_pddl = message

    def save_prompt(self):
        save_path = os.path.join(self.save_path, self.name + "prompt.json")
        data = {"name": self.name,
                "prompt": {
                    "predicates": self.prompt_predicates,
                    "instruction": self.prompt_instruction,
                    "pddl": self.prompt_pddl,
                }
                }
        with open(save_path, "w") as save_file:
            json.dump(data, save_file, indent=4)

    def run(self):
        self.prompt_encoding()
        self.save_prompt()

        self.gpt4.add_text_message_manual(role="user", content=self.prompt_predicates)
        self.gpt4.add_text_message_manual(role="user", content=self.prompt_instruction)
        self.gpt4.add_text_message_manual(role="user", content=self.prompt_pddl)

        self.gpt4.run_manual_prompt()
