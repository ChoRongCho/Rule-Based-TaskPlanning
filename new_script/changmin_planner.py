import json
import os
from datetime import datetime

from openai import OpenAI
from tabulate import tabulate

from new_script.gpt_model.gpt_interface import GPTInterpreter
from new_script.utils.utils import parse_input
from new_script.visual_interpreting.visual_interpreter import FindObjects


class ChangminPlanner:
    def __init__(self, args):
        self.args = args

        # task and experiment setting
        self.task = args.task_name
        self.exp_name = args.exp_name
        self.is_save = args.is_save
        self.max_predicates = args.max_predicates
        self.patience_repeat = 3

        # basic path
        self.args = args
        self.json_dir = args.json_dir
        self.data_dir = args.data_dir

        # additional path
        self.result_dir = os.path.join(args.result_dir, self.exp_name)
        self.input_image = os.path.join(self.data_dir, self.task, args.input_image)

        # json
        self.api_json = os.path.join(self.json_dir, args.api_json)
        self.example_json = os.path.join(self.json_dir, args.example_prompt_json)
        self.robot_json = os.path.join(self.json_dir, args.robot_json)
        self.task_json = os.path.join(self.json_dir, args.task_json)

        # read json data
        self.check_result_folder()
        self.example_data = self.get_json_data(self.example_json)
        self.robot_data = self.get_json_data(self.robot_json)
        self.task_data = self.get_json_data(self.task)
        self.task_description = self.task_data[self.task]["script"]["task_description"]
        self.api_key, self.setting = self.get_api_key()

        # Initialize Class for planning
        self.answer = []
        self.question = []

        # GPT setting
        self.client = OpenAI(api_key=self.api_key)
        self.gpt_interface_vision = GPTInterpreter(api_key=self.api_key,
                                                   example_data=self.example_data,
                                                   setting=self.setting,
                                                   version="vision")
        self.gpt_interface_pddl = GPTInterpreter(api_key=self.api_key,
                                                 example_data=self.example_data,
                                                 setting=self.setting,
                                                 version="pddl")
        self.grounding_dino = FindObjects(is_save=self.is_save)

    # GPT
    def print_args(self):
        table = [["Project Time", datetime.now()],
                 ["Task", self.task],
                 ["Exp_Name", self.exp_name],
                 ["Input Image", self.args.input_image],
                 ["API JSON", self.args.api_json],
                 ["Example Prompt", self.args.example_prompt_json]]
        print(tabulate(table))

    def check_result_folder(self):
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
            print(f"Directory '{self.result_dir}' created successfully.")
        else:
            print(f"Directory '{self.result_dir}' already exists.")

    def get_api_key(self):
        with open(self.api_json, "r") as file:
            setting = json.load(file)
            api_key = setting["api_key"]
            file.close()
            return api_key, setting

    @staticmethod
    def get_json_data(json_path):
        with open(json_path, "r") as file:
            data = json.load(file)
        return data

    def log_answer(self, answer, name=""):
        result_dir_json = os.path.join(self.result_dir, name + "_result.json")
        result_dir_txt = os.path.join(self.result_dir, name + "_result.pddl")

        json_object = {"name": name, "answer": answer}
        json_object = json.dumps(json_object, indent=4)

        with open(result_dir_json, "w") as f:
            f.write(json_object)
            f.close()

        with open(result_dir_txt, "w") as f:
            f.write(answer)
            f.close()

    def prompt_detect_object(self):
        prompt = f"We are now doing a {self.task} task which is {self.task_description}. \n"
        prompt += "This is a first observation where I work in. \n"

        prompt += "What objects or tools are here? \n"

        self.gpt_interface_vision.add_example_prompt("init_state_message")
        self.gpt_interface_vision.add_message(role="user", content=prompt, image_url=self.input_image)
        for i in range(self.patience_repeat):
            print(f"Start {i}")
            try:
                answer = self.gpt_interface_vision.run_prompt()
                result_dict, result_list = parse_input(answer=answer)
                break
            except:
                raise Exception("Making expected answer went wrong. ")
        return result_dict, result_list

    def detect_object(self):
        """
        result_dict: {In_bin: ["obj1", "obj2"], Out_bin: ["obj3"], Bin: ["white box"]}
        result_list: [] for grounddino
        :return:
        """
        result_dict, result_list = self.prompt_detect_object()
        self.grounding_dino.modifying_text_prompt(result_list)
        detected_object = self.grounding_dino.get_bbox(self.input_image, self.result_dir)
        return detected_object, result_dict

    def run_all(self):
        detected_object, detected_object_types = self.detect_object()
        active_predicates = self.get_active_predicates(detected_object=detected_object)
        object_class_python_cript = self.get_predicates(detected_object=detected_object,
                                                        detected_object_types=detected_object_types,
                                                        active_predicates=active_predicates)



    def get_predicates(self, detected_object, detected_object_types, active_predicates):
        """

        :param detected_object:
        :param detected_object_types:
        :param active_predicates:
        :return: answer object class data
        """
        prompt = f"We are now going to do a {self.task} task whose goal is {self.task_description}"
        prompt += "There are many objects in this domain, " + \
                  "this is object information that comes from image observation. \n"
        prompt += f"1. {detected_object_types} \n2. {detected_object}\n"
        prompt += f"""from dataclasses import dataclass
            
    
@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    location: tuple
    size: tuple
    color: str or bool
    object_type: str
    
    # Object physical properties predicates
    
    # {self.task} Predicates (max {self.max_predicates})
        
            """
        prompt += "However, we cannot do complete planning with this dataclass predicate alone" + \
                  f" that means we have to add another predicates that fully describe the {self.task}."
        if active_predicates:
            prompt += "Also you have to add predicates such as "
            for predicate in active_predicates:
                if predicate == active_predicates[-1]:
                    prompt += f"and {predicate}. \n"
                else:
                    prompt += predicate + ", "
        else:
            prompt += "We don't have to consider physical properties of the object."

        prompt += f"Add more predicates needed for {self.task} to class Object. "

        self.gpt_interface_pddl.add_example_prompt("domain_message")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        for i in range(self.patience_repeat):
            print(f"Start {i}")
            try:
                object_class_python_script = self.gpt_interface_pddl.run_prompt()
                break
            except:
                raise Exception("Making expected answer went wrong. ")

        return object_class_python_script

    def get_active_predicates(self, detected_object):
        print(detected_object)
        print("Start robot active search")
        active_predicates = ["is_rigid", "is_flexible", "is_soft", "is_foldable"]
        return active_predicates

    def generate_init_state(self):
        pass