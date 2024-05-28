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
from scripts.utils.models import WorldDomain


class ChangminPlanner:
    def __init__(self, args):

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
        self.domain_image = os.path.join(self.data_dir, self.task, args.input_image)

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

        # init state, goal state, def_table
        self.world_model = WorldDomain
        self.state = {}
        self.print_args()

    def print_args(self):
        self.table = [["Project Time", datetime.now()],
                      ["Task", self.task],
                      ["Exp_Name", self.exp_name],
                      ["Input Image", self.args.input_image],
                      ["API JSON", self.args.api_json],
                      ["Example Prompt", self.args.example_prompt_json],
                      ["Max Predicates", self.args.max_predicates]]
        # print(tabulate(self.table))
        self.robot.print_definition_of_predicates()

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
        self.gpt_interface_vision.add_message(role="user", content=prompt, image_url=self.domain_image)
        for i in range(self.patience_repeat):
            try:
                answer = self.gpt_interface_vision.run_prompt()
                print(answer)
                result_dict, result_list = parse_input(answer=answer)

                self.question.append(prompt)
                self.answer.append(answer)
                # break
                return result_dict, result_list
            except:
                raise Exception("Making expected answer went wrong. ")

    def detect_object(self):
        """
        result_dict: {In_bin: ["obj1", "obj2"], Out_bin: ["obj3"], Bin: ["white box"]}
        result_list: [] for grounddino
        :return:
        """
        result_dict, result_list = self.prompt_detect_object()
        self.grounding_dino.modifying_text_prompt(result_list)
        detected_object, self.anno_image = self.grounding_dino.get_bbox(self.domain_image, self.result_dir)
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
            for index, info in detected_object.items():  # info: {'white box': [509, 210, 231, 323]}
                info = self.robot.get_object_predicates(info)
                detected_object_predicates.update({index: info})
        # final return: {0: ['is_elastic'], 1: ['is_fragile', 'is_rigid'], 2: ['is_foldable'], 3: ['is_soft']}

        # Removing duplicate predicates.
        tempt_list = list(detected_object_predicates.values())
        flattened_list = [item for sublist in tempt_list for item in sublist]
        active_predicates = list(set(flattened_list))

        return active_predicates, detected_object_predicates

    def temp_get_obj_predicates(self):
        push_img, fold_img, pull_img = self.robot.identifying_properties()
        self.gpt_interface_vision.add_message(role="system", content=self.robot.database.system_message)
        self.gpt_interface_vision.add_message(role="user")


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
                       do_types,
                       do_predicates,
                       oc_python_script):
        self.gpt_interface_pddl.reset_message()
        prompt = self.load_prompt.load_prompt_init_state(detected_object=detected_object,
                                                         detected_object_types=do_types,
                                                         detected_object_predicates=do_predicates,
                                                         object_class_python_script=oc_python_script)
        self.gpt_interface_pddl.add_example_prompt("init_state_message")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)

        # run prompt
        init_state_script = self.gpt_interface_pddl.run_prompt()
        self.question.append(prompt)
        self.answer.append(init_state_script)

        # split a text
        init_state_python_code, init_state_table = init_state_script.split("Table")
        init_state_python_code = init_state_python_code.replace("Python Code", "").strip()
        init_state_table = init_state_table.strip()

        return init_state_python_code, init_state_table

    def get_goal_state(self, init_state_table):
        self.gpt_interface_pddl.reset_message()

        # get example message1
        prompt = self.load_prompt.load_prompt_gs_encoding(init_state_table,
                                                          self.task_data["goal"],
                                                          self.task_data["instructions"])

        # add example and prompt
        self.gpt_interface_pddl.add_example_prompt("goal_message")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)

        # run prompt
        goal_state = self.gpt_interface_pddl.run_prompt()
        self.question.append(prompt)
        self.answer.append(goal_state)

        # split a text
        goal_state_description, goal_state_table = goal_state.split("Table")
        return goal_state_description, goal_state_table

    def planning_from_domain(self,
                             object_class_python_script,
                             robot_class_python_script,
                             init_state_python_script,
                             init_state_table,
                             goal_state_table):

        self.gpt_interface_pddl.reset_message()
        prompt = self.load_prompt.load_prompt_planning(object_class_python_script=object_class_python_script,
                                                       robot_class_python_script=robot_class_python_script,
                                                       init_state_python_script=init_state_python_script,
                                                       init_state_table=init_state_table,
                                                       goal_state_table=goal_state_table,
                                                       robot_action=self.robot_data["actions"],
                                                       task_instruction=self.task_data["instructions"])

        self.gpt_interface_pddl.add_example_prompt("domain_message")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)

        planning_python_script = self.gpt_interface_pddl.run_prompt()
        self.question.append(prompt)
        self.answer.append(planning_python_script)
        return planning_python_script

    def make_plan(self):
        # first, load domain model

        # Detect Object and make action predicates for objects
        detected_object, detected_object_types = self.detect_object()
        active_predicates, detected_object_predicates = self.get_active_predicates(detected_object=detected_object)

        # integrate objects physical predicates to other predicates
        object_class_python_script = self.get_predicates(detected_object=detected_object,
                                                         detected_object_types=detected_object_types,
                                                         active_predicates=active_predicates)
        # make robot action conditions
        robot_class_python_script = self.get_robot_action_conditions(object_class_python_script)
        init_state_python_script, init_state_table = self.get_init_state(detected_object=detected_object,
                                                                         do_types=detected_object_types,
                                                                         do_predicates=detected_object_predicates,
                                                                         oc_python_script=object_class_python_script)
        # simple goal state description
        _, goal_state_table = self.get_goal_state(init_state_table=init_state_table)
        
        # All result
        planning_python_script = self.planning_from_domain(object_class_python_script=object_class_python_script,
                                                           robot_class_python_script=robot_class_python_script,
                                                           init_state_python_script=init_state_python_script,
                                                           init_state_table=init_state_table,
                                                           goal_state_table=goal_state_table)
        # world model + init model
        if self.is_save:
            self.log_answer()
            self.state_parsing(init_state_table, goal_state_table)
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
                file.write("Q: ")
                file.write(q + "\n\n")
                file.write("A: \n")
                file.write(a + "\n")
                file.write("--" * 50 + "\n\n")
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
            new_planning = self.robot_action_feedback(python_script=content, planning_output=planning_output)
            new_plan = self.replace_string(content, new_planning, "def")

        else:
            planning_output = output.decode('utf-8') + "\n"
            new_planning = self.direct_planner_feedback(python_script=content, planning_output=planning_output)
            """
            1. No error in syntax
            2. goal state error in this part
            
            use python planner validator
            """
            new_plan = new_planning

        if self.is_save:
            new_file_path = os.path.join(self.result_dir, f"planning_{self.planning_repeat}.py")
            planning_result_path = os.path.join(self.result_dir, f"planning_result_{self.planning_repeat}.txt")
            with open(new_file_path, "w") as file:
                file.write(str(new_plan) + "\n\n")
                file.close()
            with open(planning_result_path, "w") as file:
                file.write(planning_output)
                file.close()

    def robot_action_feedback(self, python_script, planning_output):
        self.gpt_interface_pddl.reset_message()
        prompt = self.load_prompt.load_prompt_action_feedback(python_script=python_script,
                                                              planning_output=planning_output)
        self.gpt_interface_pddl.add_example_prompt("robot_feedback")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        robot_action_feedback = self.gpt_interface_pddl.run_prompt()
        return robot_action_feedback

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

        replaced_script = before + middle + "\n\n    " + after
        return replaced_script

    def just_chat(self, message, role="user", image_url=False):
        if not image_url:
            self.gpt_interface_pddl.reset_message()
            self.gpt_interface_pddl.add_message(role=role, content=message, image_url=False)
            answer = self.gpt_interface_pddl.run_prompt()
            return answer
        else:
            self.gpt_interface_vision.reset_message()
            self.gpt_interface_vision.add_message(role=role, content=message, image_url=image_url)
            answer = self.gpt_interface_vision.run_prompt()
            return answer

    def append_chat(self, message, role="user", is_reset=False):
        if is_reset:
            self.gpt_interface_pddl.reset_message()
        self.gpt_interface_pddl.add_message(role=role, content=message, image_url=False)

    def run_chat(self):
        answer = self.gpt_interface_pddl.run_prompt()
        return answer

    def state_parsing(self, init_state_table, goal_state_table):
        json_state_path = os.path.join(self.result_dir, "state.json")

        def parse_state(state_str):
            state_dict = {}
            lines = state_str.strip().split('\n')
            header = [x.strip() for x in lines[1].strip('|').split('|')]

            for line in lines[3:]:
                data = [x.strip() for x in line.strip('|').split('|')]
                item_name = data[header.index('item')].strip()
                if "--" in item_name:
                    break
                state_dict[item_name] = {}
                for i, field in enumerate(header):
                    if field != 'item':
                        state_dict[item_name][field] = data[i].strip()
            return state_dict

        init_state = parse_state(init_state_table)
        goal_state = parse_state(goal_state_table)

        self.state = {
            "init_state": init_state,
            "goal_state": goal_state
        }

        with open(json_state_path, "w") as file:
            json.dump(self.state, file, indent=4)
            file.close()
