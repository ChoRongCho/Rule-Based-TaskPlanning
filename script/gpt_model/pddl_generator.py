import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List

from tabulate import tabulate

from script.gpt_model.gpt_prompt import GPTInterpreter
from ..utils.utils import create_folder, RobotKeyError, JsonFileContentError, DomainPredicate

task_number_table = {
    0: "bin_packing",
    1: "hanoi",
    2: "blocksworld",
    3: "cooking"
}


@dataclass
class Robot:
    name: str = "UR5"
    goal: str = None
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

        (task description + get predicates) 
        + (human_instruction + action set) 
        + (domain.pddl + problem.pddl) => new domain or problem.pddl

        needed args
        1. name
        2. result_dir for save a prompt and its answer.
        3. data_dir for get prompts
        4. task
        5. api_json
        6. example_prompt_json : false if used manual prompt
        7. domain, problem: True or False
        """
        # basic
        self.args = args
        self.predicates = predicates
        self.task_number_table = task_number_table

        # utils
        self.name = args.name
        self.result_dir = os.path.join(args.result_dir, args.name)
        create_folder(self.result_dir)

        # task definition
        domain = DomainPredicate(args.task)
        self.task = domain.task

        # GPT Client
        self.gpt4 = GPTInterpreter(api_json=args.api_json,
                                   example_prompt_json=args.prompt_json,
                                   result_dir=self.result_dir,
                                   version="pddl")

        # robot
        self.robot = Robot()
        self.get_robot_information()

        # pddl
        self.domain_prompt = self.get_example_pddl("domain")
        self.problem_prompt = self.get_example_pddl("problem")

        # human instruction
        self.human_instruction = self.get_human_instruction()

        # message
        self.prompt_predicates = ""
        self.prompt_instruction = ""
        self.prompt_pddl = ""

        self.message = []

    def print_args(self):
        table = [["Project Time", datetime.now()],
                 ["Task", self.task],
                 ["Name", self.name],
                 ["Predicates", self.predicates],
                 ["Robot Actions", list(self.robot.actions.keys())],
                 ]
        print(tabulate(table))

    def get_robot_information(self):
        """

        :return:
        """
        robot_json_path = os.path.join(self.args.data_dir, self.name, "robot_description.json")
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

    def get_human_instruction(self) -> str:

        hi_json_path = os.path.join(self.args.data_dir, self.name, "instruction.json")
        with open(hi_json_path, "r") as hi_json_file:
            hi_info = json.load(hi_json_file)
            content_list = []
            try:
                # add get info code
                human_prompt = sorted(hi_info["prompt"], key=lambda x: x['index'])
                for i in range(len(human_prompt)):
                    content_text = human_prompt[i]["content"] + "\n"
                    content_list.append(content_text)
                content = "".join(content_list)
                # print("\n\n---- Human Instruction ----")
                # print(content)
                # print("---- Human Instruction ----\n\n")
            except:
                raise JsonFileContentError

        hi_json_file.close()
        return content

    def get_example_pddl(self, pddl: str = "domain") -> List or bool:
        if pddl.lower() == "domain":
            if self.args.domain:
                pddl_path = os.path.join(self.args.data_dir, self.name, "domain.pddl")
                content = self.pddl_format(pddl_path, json_key="answer")

            else:
                content = False

        elif pddl.lower() == "problem":
            if self.args.problem:
                pddl_path = os.path.join(self.args.data_dir, self.name, "problem.pddl")
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
        self.intro_encoding()
        self.human_instruction_encoding()
        self.pddl_instruction_encoding()

    def intro_encoding(self):
        message = f"Hi, my name is {self.robot.name}, and I am a robot. \n"
        # Intro, inform GPT what will do.
        if self.task == "bin_packing":
            message += f"Our goal is {self.robot.goal}, which is called {self.task}. " + \
                       "In a problem instance, there is a box, a manipulator robot(it's me!), and objects set. \n" + \
                       f"I want to define a domain name as {self.task}."
            # Add predicates
            if len(self.predicates) == 0:
                message += "Given this goal, I want to make a domain.pddl. \n"
            else:
                message += "We want to consider physical properties of the objects such as "
                for predicate in self.predicates:
                    if predicate == self.predicates[-1]:
                        message += "and " + predicate + ". \n"
                    else:
                        message += predicate + ", "
                message += "Given this goal, I want to make a domain.pddl" + \
                           " considering the physical properties of the objects. " + \
                           f"The domain file is supposed to include predicates such as is_{self.predicates[0]}. "

            message += "Actions must consider the predicates in preconditions and effects. \n"

        elif self.task == "hanoi":
            message += f"Our goal is {self.robot.goal}, which is called {self.task}. " + \
                       "In a problem instance, there are disks, a manipulator robot(it's me!), and a tower. \n" + \
                       f"I want to define a domain name as {self.task}."
            message = self.task_prompt(message)

        elif self.task == "blocksworld":
            message += f"Our goal is {self.robot.goal}, which is called {self.task}. " + \
                       "In a problem instance, there are blocksworld and a manipulator robot(it's me!). \n" + \
                       f"I want to define a domain name as {self.task}."
            message = self.task_prompt(message)

        elif self.task == "cooking":
            message += f"Our goal is {self.robot.goal}, which is called {self.task}. " + \
                       "In a problem instance, there are vegetables, tools and a manipulator robot(it's me!). \n" + \
                       f"I want to define a domain name as {self.task}. \n"
            message = self.task_prompt(message)

        else:
            raise KeyError("0: bin packing, 1: hanoi, 2: blocksworld, 3: cooking")

        self.prompt_predicates = message

    def task_prompt(self, message):
        # Add predicates
        if len(self.predicates) == 0:
            message += "Given this goal, I want to make a domain.pddl. \n"
        else:
            message += "We want to consider the predicates such as "
            for predicate in self.predicates:
                if predicate == self.predicates[-1]:
                    message += "and " + predicate + ". \n"
                else:
                    message += predicate + ", "
            message += "Given this goal, I want to make a domain.pddl. \n"
        message += "Actions must consider the predicates in preconditions and effects. \n"
        return message

    def human_instruction_encoding(self):

        # Add Human instruction, message reset
        message = f"Now, I'm going to talk about precautions when doing {self.task}. \n"
        message += self.human_instruction

        # Add actions when making actions
        message += "The actions I can do are "
        for action in list(self.robot.actions.keys()):
            if action == list(self.robot.actions.keys())[-1]:
                message += "and " + action + ". \n"
            else:
                message += action + ", "
        message += "When you define action in domain.pddl, you must use that action set. " + \
                   "No other actions is permitted. \n"
        self.prompt_instruction = message

    def pddl_instruction_encoding(self):
        message = ""
        if self.problem_prompt:
            message += "Here is an example of a problem.pddl. \n"
            message += self.problem_prompt
            message += " \n" + \
                       "The initial state and goal state will be given like this. \n"

        if self.domain_prompt:
            message += "Here is an example of a domain.pddl. \n"
            message += self.domain_prompt
            message += " \n" + \
                       "Refer this pddl and modify this domain.pddl \n"
        message += "Please generate the only pddl without any explanation to return your answer to pddl file. \n" + \
                   "Never add your any word to pddl file. \n"
        self.prompt_pddl = message

    def log_prompt(self):
        result_dir_json = os.path.join(self.result_dir, self.name + "_prompt.json")
        result_dir_txt = os.path.join(self.result_dir, self.name + "_prompt.txt")
        data = {"name": self.name,
                "prompt": {
                    "predicates": self.prompt_predicates,
                    "instruction": self.prompt_instruction,
                    "pddl": self.prompt_pddl,
                }
                }
        json_object = json.dumps(data, indent=4)
        with open(result_dir_txt, "w") as save_file:
            save_file.write("--Predicate Prompt--\n" +
                            self.prompt_predicates + "Assistant: " +
                            self.assistant_prompt("predicates") +
                            "\n\n--Instruction Prompt--\n" +
                            self.prompt_instruction + "Assistant: " +
                            self.assistant_prompt("instruction"))

            save_file.write("\n\n--PDDL Prompt--\n" +
                            self.prompt_pddl + "Assistant: " +
                            self.assistant_prompt("pddl"))

            save_file.close()

        with open(result_dir_json, "w") as save_file:
            save_file.write(json_object)
            save_file.close()

    @staticmethod
    def assistant_prompt(mode: str):
        if mode == "predicates":
            prompt_answer = "Ok! I'll never change your given conditions such as actions and predicates. \n"
        elif mode == "instruction":
            prompt_answer = "Considering your request, I think I only need to consider the preconditions and effects" + \
                             " of the action part! \n" + \
                            "By the way, if you have a problem.pddl file, can you show me it? If so, I can do better! "
        elif mode == "pddl":
            prompt_answer = "Sure! I'll respond in only a pddl file! Here you are! \n"
        else:
            raise ValueError("Wrong prompt")
        return prompt_answer

    def run(self):
        self.prompt_encoding()
        self.log_prompt()
        print("--- Logging is done ---")
        # self.gpt4.add_text_message_manual(role="user", content="")

        self.gpt4.add_message_manual(role="system", content="you are a very smart assistant. ")
        self.gpt4.add_message_manual(role="user", content=self.prompt_predicates)
        self.gpt4.add_message_manual(role="assistant", content=self.assistant_prompt("predicates"))
        self.gpt4.add_message_manual(role="user", content=self.prompt_instruction)
        self.gpt4.add_message_manual(role="assistant", content=self.assistant_prompt("instruction"))
        self.gpt4.add_message_manual(role="user", content=self.prompt_pddl)
        self.gpt4.add_message_manual(role="assistant", content=self.assistant_prompt("pddl"))

        self.gpt4.run_manual_prompt(name=self.args.name, is_save=True)
