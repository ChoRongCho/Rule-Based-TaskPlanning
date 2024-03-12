import json
import os
import subprocess
from datetime import datetime

import cv2
from openai import OpenAI
from tabulate import tabulate

from scripts.gpt_model.gpt_interface import GPTInterpreter
from scripts.temp_robot.robot_predicates_prove import RobotProve
from scripts.utils.prompt_function import PromptSet
from scripts.utils.utils import parse_input
from scripts.visual_interpreting.visual_interpreter import FindObjects


class ChangminPlanner:
    def __init__(self, args):
        self.args = args

        # task and experiment setting
        self.task = args.task_name
        self.exp_name = args.exp_name
        self.is_save = args.is_save
        self.max_predicates = args.max_predicates
        self.patience_repeat = 3
        self.planning_repeat = 0

        # basic path
        self.args = args
        self.json_dir = args.json_dir
        self.data_dir = args.data_dir

        # additional path
        self.result_dir = os.path.join(args.result_dir, self.exp_name)
        self.input_image = os.path.join(self.data_dir, self.task, args.input_image)

        # json_dir
        self.api_json = os.path.join(self.json_dir, args.api_json)
        self.example_json = os.path.join(self.json_dir, args.example_prompt_json)
        self.robot_json = os.path.join(self.json_dir, args.robot_json)
        self.task_json = os.path.join(self.json_dir, args.task_json)

        # read json data
        self.example_data = self.get_json_data(self.example_json)
        self.robot_data = self.get_json_data(self.robot_json)
        self.task_data = self.get_json_data(self.task_json)

        self.task_description = self.task_data["script"]["task_description"]
        self.api_key, self.setting = self.get_api_key()

        # Initialize Class for planning
        self.answer = []
        self.question = []
        self.table = []
        self.anno_image = False

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
        self.load_prompt = PromptSet(task=self.task, task_description=self.task_description)
        self.robot = RobotProve(name=self.robot_data["name"],
                                goal=self.robot_data["goal"],
                                actions=self.robot_data["actions"])
        self.print_args()

    def print_args(self):
        self.table = [["Project Time", datetime.now()],
                      ["Task", self.task],
                      ["Exp_Name", self.exp_name],
                      ["Input Image", self.args.input_image],
                      ["API JSON", self.args.api_json],
                      ["Example Prompt", self.args.example_prompt_json],
                      ["Max Predicates", self.args.max_predicates]]
        print(tabulate(self.table))

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

    def get_json_data(self, json_path):
        with open(json_path, "r") as file:
            data = json.load(file)
            data = data[self.task]
        return data

    def prompt_detect_object(self):
        self.gpt_interface_vision.reset_message()
        prompt = self.load_prompt.load_prompt_detect_object()
        self.gpt_interface_vision.add_example_prompt("observation_message")
        self.gpt_interface_vision.add_message(role="user", content=prompt, image_url=self.input_image)
        for i in range(self.patience_repeat):
            try:
                answer = self.gpt_interface_vision.run_prompt()
                result_dict, result_list = parse_input(answer=answer)

                self.question.append(prompt)
                self.answer.append(answer)
                # break
                return result_dict, result_list
            except:
                raise Exception("Making expected answer went wrong. ")
        # return result_dict, result_list

    def detect_object(self):
        """
        result_dict: {In_bin: ["obj1", "obj2"], Out_bin: ["obj3"], Bin: ["white box"]}
        result_list: [] for grounddino
        :return:
        """
        result_dict, result_list = self.prompt_detect_object()
        self.grounding_dino.modifying_text_prompt(result_list)
        detected_object, self.anno_image = self.grounding_dino.get_bbox(self.input_image, self.result_dir)
        return detected_object, result_dict

    def get_active_predicates(self, detected_object, random_mode=True):
        """
        random sampled active predicates
        
        :param random_mode:
        :param detected_object:
        input_dict = {0: {'white box': [509, 210, 231, 323]},
                      1: {'blue object': [204, 220, 361, 247]},
                      2: {'yellow object': [83, 158, 135, 216]},
                      3: {'brown object': [257, 95, 139, 148]}}
        :return: 
        active_predicates = ['is_fragile', 'is_foldable', 'is_soft', 'is_elastic', 'is_rigid']
        detected_object_predicates = {0: ['is_elastic'], 1: ['is_fragile', 'is_rigid'], 2: ['is_foldable'], 3: ['is_soft']}        
        """
        if random_mode:
            detected_object_predicates = {}
            for index, info in detected_object.items():
                info = self.robot.random_active_search(info)
                detected_object_predicates.update({index: info})

        else:  # Do robot active prove
            detected_object_predicates = {}
            for index, info in detected_object.items():
                info = self.robot.get_object_predicates(info)
                detected_object_predicates.update({index: info})

        # Removing duplicate predicates.
        tempt_list = list(detected_object_predicates.values())
        flattened_list = [item for sublist in tempt_list for item in sublist]
        active_predicates = list(set(flattened_list))

        return active_predicates, detected_object_predicates

    def get_predicates(self, detected_object, detected_object_types, active_predicates):
        """

        :param detected_object:
        :param detected_object_types:
        :param active_predicates:
        :return: answer object class data
        """
        self.gpt_interface_pddl.reset_message()
        prompt = self.load_prompt.load_prompt_get_predicates(detected_object=detected_object,
                                                             detected_object_types=detected_object_types,
                                                             max_predicates=self.max_predicates)

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

        self.gpt_interface_pddl.add_example_prompt("object_message")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        for i in range(self.patience_repeat):
            try:
                object_class_python_script = self.gpt_interface_pddl.run_prompt()
                self.question.append(prompt)
                self.answer.append(object_class_python_script)
                return object_class_python_script
            except:
                raise Exception("Making expected answer went wrong. ")

    def get_robot_action_conditions(self, object_class_python_script):
        self.gpt_interface_pddl.reset_message()
        prompt = self.load_prompt.load_prompt_robot_action(object_class_python_script=object_class_python_script,
                                                           robot_action=self.robot_data["actions"],
                                                           task_instruction=self.task_data["instructions"])

        self.gpt_interface_pddl.add_example_prompt("robot_action_message")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        # for i in range(self.patience_repeat):
        #     try:
        robot_class_python_script = self.gpt_interface_pddl.run_prompt()
        self.question.append(prompt)
        self.answer.append(robot_class_python_script)
        return robot_class_python_script
        # except:
        #     raise Exception("Making expected answer went wrong. ")

    def get_init_state(self,
                       detected_object,
                       detected_object_types,
                       detected_object_predicates,
                       object_class_python_script):
        self.gpt_interface_pddl.reset_message()
        prompt = self.load_prompt.load_prompt_init_state(detected_object=detected_object,
                                                         detected_object_types=detected_object_types,
                                                         detected_object_predicates=detected_object_predicates,
                                                         object_class_python_script=object_class_python_script)
        self.gpt_interface_pddl.add_example_prompt("init_state_message")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        # for i in range(self.patience_repeat):
        #     try:
        init_state_python_script = self.gpt_interface_pddl.run_prompt()
        self.question.append(prompt)
        self.answer.append(init_state_python_script)
        return init_state_python_script
        # except:
        #     raise Exception("Making expected answer went wrong. ")

    def planning_from_domain(self, object_class_python_script, robot_class_python_script, init_state_python_script):
        self.gpt_interface_pddl.reset_message()
        prompt = self.load_prompt.load_prompt_planning(object_class_python_script=object_class_python_script,
                                                       robot_class_python_script=robot_class_python_script,
                                                       init_state_python_script=init_state_python_script,
                                                       robot_action=self.robot_data["actions"],
                                                       task_instruction=self.task_data["instructions"])
        self.gpt_interface_pddl.add_example_prompt("domain_message")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        # for i in range(self.patience_repeat):
        #     try:
        planning_python_script = self.gpt_interface_pddl.run_prompt()
        self.question.append(prompt)
        self.answer.append(planning_python_script)
        return planning_python_script
        # except:
        #     raise Exception("Making expected answer went wrong. ")

    def make_plan(self):
        detected_object, detected_object_types = self.detect_object()
        active_predicates, detected_object_predicates = self.get_active_predicates(detected_object=detected_object)
        object_class_python_script = self.get_predicates(detected_object=detected_object,
                                                         detected_object_types=detected_object_types,
                                                         active_predicates=active_predicates)
        robot_class_python_script = self.get_robot_action_conditions(object_class_python_script)
        init_state_python_script = self.get_init_state(detected_object=detected_object,
                                                       detected_object_types=detected_object_types,
                                                       detected_object_predicates=detected_object_predicates,
                                                       object_class_python_script=object_class_python_script)
        planning_python_script = self.planning_from_domain(object_class_python_script=object_class_python_script,
                                                           robot_class_python_script=robot_class_python_script,
                                                           init_state_python_script=init_state_python_script)

        if self.is_save:
            self.log_answer()
            file_path = os.path.join(self.result_dir, "planning.py")
            with open(file_path, "w") as file:
                file.write(str(object_class_python_script) + "\n\n")
                file.write(str(robot_class_python_script) + "\n")
                file.write("    def dummy(self):\n        pass\n\n\n")
                file.write(str(init_state_python_script) + "\n\n")
                file.write(str(planning_python_script) + "\n")
                file.close()

    def log_answer(self):
        self.check_result_folder()
        cv2.imwrite(os.path.join(self.result_dir, "annotated_image.jpg"), self.anno_image)

        log_txt_path = os.path.join(self.result_dir, "prompt.txt")
        with open(log_txt_path, "w") as file:
            file.write(tabulate(self.table))
            file.write("\n")
            file.write("-" * 50 + "\n")
            for q, a in zip(self.question, self.answer):
                file.write(q + "\n\n")
                file.write(a + "\n")
                file.write("-" * 50 + "\n")
            file.close()

    def planning_feedback(self):

        # robot_actions = self.robot_data["actions"]
        # task_instructions = self.task_data["instructions"]

        if self.planning_repeat == 0:
            file_path = os.path.join(self.result_dir, "planning.py")
            self.planning_repeat += 1
        else:
            file_path = os.path.join(self.result_dir, f"planning_{self.planning_repeat}.py")
            self.planning_repeat += 1
        with open(file_path, "r") as file:
            content = file.read()
            file.close()

        # Get planning result
        process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:  # robot action re-definition
            planning_output = output.decode('utf-8') + "\n" + error.decode('utf-8')
            prompt, new_planning = self.robot_action_feedback(python_script=content, planning_output=planning_output)
            new_plan = self.replace_string(content, new_planning, "def")
            print(planning_output, "\n")
            print(new_planning)
            print("-"*90)

        else:
            planning_output = output.decode('utf-8') + "\n"
            prompt, new_planning = self.direct_planner_feedback(python_script=content, planning_output=planning_output)
            new_plan = new_planning
            print(new_plan)
            print("-" * 90)

        if self.is_save:
            new_file_path = os.path.join(self.result_dir, f"planning_{self.planning_repeat}.py")
            with open(new_file_path, "w") as file:
                file.write(str(new_plan) + "\n\n")
                file.close()

    def robot_action_feedback(self, python_script, planning_output):
        self.gpt_interface_pddl.reset_message()
        prompt = self.load_prompt.load_prompt_action_feedback(python_script=python_script,
                                                              planning_output=planning_output)
        self.gpt_interface_pddl.add_example_prompt("robot_feedback")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        robot_action_feedback = self.gpt_interface_pddl.run_prompt()
        return prompt, robot_action_feedback

    def direct_planner_feedback(self, python_script, planning_output):
        self.gpt_interface_pddl.reset_message()
        prompt = self.load_prompt.load_prompt_planner_feedback(python_script=python_script,
                                                               planning_output=planning_output,
                                                               robot_action=self.robot_data["actions"],
                                                               task_instruction=self.task_data["instructions"])
        # self.gpt_interface_pddl.add_example_prompt("planner_feedback")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        planner_feedback = self.gpt_interface_pddl.run_prompt()

        return prompt, planner_feedback

    @staticmethod
    def replace_string(content, replace_part, end_part):
        fline_index = replace_part.find("\n")
        replace_def = replace_part[:fline_index]

        start_index = content.find(replace_def)
        end_index = content.find(end_part, start_index + 1)
        if end_index == -1:
            end_index = len(content)

        before = content[:start_index]
        middle = replace_part
        after = content[end_index:]

        replaced_script = before + middle + "\n\n\t" + after
        return replaced_script

    def just_chat(self, message):

        self.gpt_interface_pddl.reset_message()
        self.gpt_interface_pddl.add_message(role="user", content=message, image_url=False)
        answer = self.gpt_interface_pddl.run_prompt()

        return answer

    def get_object_predicates(self, info):
        pass

    def goal_state_encoding(self, message):
        prompt = """# Object 1
bin1 = Object(
    index=0,
    name='white box',
    location=(516, 201),
    size=(238, 334),
    color='white',
    object_type='box',
    is_elastic=True,
    is_rigid=True,
    in_bin=True
)

# Object 2
object2 = Object(
    index=1,
    name='yellow object',
    location=(280, 134),
    size=(227, 221),
    color='yellow',
    object_type='object',
    is_foldable=True,
    out_bin=True
)

# Object 3
object3 = Object(
    index=2,
    name='black object',
    location=(79, 275),
    size=(151, 113),
    color='black',
    object_type='object',
    is_rigid=True,
    out_bin=True,
    is_black=True
)

# Object 4
object4 = Object(
    index=3,
    name='brown object',
    location=(503, 205),
    size=(147, 153),
    color='brown',
    object_type='object',
    is_rigid=True,
    is_elastic=True,
    in_bin=True
)

# Object 5
object5 = Object(
    index=4,
    name='blue object',
    location=(223, 209),
    size=(355, 244),
    color='blue',
    object_type='object',
    is_soft=True,
    out_bin=True
)\n
"""
        prompt += "This is a initial state of bin_packing task. \n"
        prompt += "We are now doing a bin_packing and our goal is listed below. \n\n"

        goal_prompt = self.task_data["goal"]
        prompt += str(goal_prompt)
        prompt += "\nUsing init state and natural instruction of goal, make a goal state represented as a python script. \n"
        print(prompt)
        self.gpt_interface_pddl.reset_message()
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        answer = self.gpt_interface_pddl.run_prompt()
        print("-"*90)
        print(answer)

    def init_state_encoding(self):
        pass



