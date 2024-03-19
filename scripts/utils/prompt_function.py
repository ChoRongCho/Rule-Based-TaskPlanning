from typing import List


class PromptSet:
    def __init__(self, task, task_description):
        self.task = task
        self.task_description = task_description

    def load_prompt_detect_object(self):
        prompt = f"We are now doing a {self.task} task. \n"
        prompt += "This is a first observation where I work in. \n"
        prompt += "What objects or tools are here? \n"
        return prompt

    def load_prompt_get_predicates(self, detected_object, detected_object_types, max_predicates):
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

    # {self.task} Predicates (max {max_predicates})\n"""
        prompt += "However, we cannot do complete planning with this dataclass predicate alone" + \
                  f" that means we have to add another predicates that fully describe the {self.task}."

        return prompt

    def load_prompt_robot_action(self,
                                 object_class_python_script,
                                 robot_action,
                                 task_instruction):
        prompt = f"We are now going to do a {self.task} task whose goal is packing all objects in the bin. \n"
        prompt += "We have a basic python structure describing the available robot actions. \n"
        prompt += f"""{object_class_python_script}\n\n"""
        prompt += """
class Robot:
    # Define skills
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    # bin_packing
    def pick(self, obj):
        # make a preconditions for actions
        print(f"Pick {obj.name}")
        
    # bin_packing
    def place(self, obj, bins):
        # make a preconditions for actions
        print(f"Place {obj.name} in {bins.name}")
    
    # bin_packing
    def push(self, obj):
        # make a preconditions for actions
        print(f"Push {obj.name}")
    
    # bin_packing
    def fold(self, obj):
        # make a preconditions for actions
        print(f"Fold {obj.name}")
    
    def out(self, obj, bins):
        # make a preconditions for actions
        print(f"Out {obj.name} from {obj.name}")\n\n"""

        prompt += "I want to modify the preconditions and effects of the robot actions based on the rules. \n"
        prompt += f"""
{robot_action}
{task_instruction}\n"""
        prompt += "Please make more action conditions and effect of the robot " + \
                  f"and objects state that used for {self.task}. \n"
        prompt += f"For example, if you place an object in hand, obj.in_bin=False. \n"
        prompt += "However, if there are predicates that are mentioned in the rules but not in the object class, " + \
                  "do not reflect those predictions in the rules."
        return prompt

    def load_prompt_init_state(self,
                               detected_object,
                               detected_object_types,
                               detected_object_predicates,
                               object_class_python_script):
        prompt = f"We are now making initial state of the {self.task}. We get these information from the observation. \n\n"
        prompt += f"{detected_object}\nNote! [cx: center of bbox, cy: center of bbox, w: bbox width, h: bbox height] \n"
        prompt += f"{detected_object_types}\n"
        prompt += f"{detected_object_predicates}\n\n"
        prompt += f"""{object_class_python_script}"""

        prompt += "\nUsing above information, fill all the object class. If there is no information of the predicate," + \
                  " assume it as a False. If the values of the predictions of an object overlap with the default, don't write them down."

        return prompt

    def load_prompt_planning(self,
                             object_class_python_script,
                             robot_class_python_script,
                             init_state_python_script,
                             init_state_table,
                             goal_state_table,
                             robot_action,
                             task_instruction):

        prompt = f"{object_class_python_script}\n\n"
        prompt += f"{robot_class_python_script}\n\n"
        prompt += f"{init_state_python_script}\n\n"

        prompt += "if __name__ == '__main__':\n\t# packing all object in the box\n\t# make a plan\n"

        # prompt += f"Your goal is {self.task_description}. \n"
        prompt += "You must follow the rule: \n"
        prompt += f"""
{robot_action}
{task_instruction}\n"""

        prompt += "Make a plan under the if __name__ == '__main__':. \nYou must make a correct order. \n"
        prompt += f"{init_state_table}\n\n{goal_state_table}\n"
        return prompt

    def load_prompt_action_feedback(self, python_script, planning_output):
        prompt = f"We made a plan for a {self.task} and our goal is {self.task_description}. \n"
        prompt += f"Below is the Python code for it. \n\n"
        prompt += python_script + " \n"

        prompt += "And this is a result. \n"
        prompt += planning_output + " \n"

        prompt += "We find that there is an error in the robot action part that describes the preconditions and " + \
                  "effects of the action. \n"
        prompt += "Please modify the action preconditions if they use preconditions that the Object class doesn't use. \n"
        return prompt

    def load_prompt_planner_feedback(self, python_script, planning_output, task_instruction, robot_action):
        prompt = f"We made a plan for a {self.task} and our goal is {self.task_description}. \n"
        prompt += f"Below is the Python code for it. \n\n"
        prompt += python_script + " \n"

        prompt += "And this is a result. \n"
        prompt += planning_output + " \n"

        prompt += "There are some planning errors in this code that is represented as Cannot. \n" + \
                  " Here are some rules for planning. \n"
        prompt += f"{task_instruction}\n"
        prompt += f"{robot_action}\n"

        prompt += "Please re-planning under the if __name__ == '__main__' part. \n"

        return prompt

    def load_prompt_gs_encoding(self, init_state_table, goal_instructions, task_instruction):
        prompt = f"{init_state_table}\n\n"
        prompt += f"This is an. initial state of {self.task} task. \n"
        prompt += "We are now doing a bin_packing and our goal is listed below. \n\n"
        prompt += f"{goal_instructions}\n\n"
        prompt += "And, this is rules that when you do actions. \n"
        prompt += f"{task_instruction}\n"
        prompt += f"Create and return a goal state of objects for {self.task}. \n"
        return prompt


class PromptSetPDDL:
    def __init__(self, task, task_description):
        self.task = task
        self.task_description = task_description

    def load_prompt_detect_object(self):
        prompt = f"We are now doing a {self.task} task. \n"
        prompt += "This is a first observation where I work in. \n"
        prompt += "What objects or tools are here? \n"
        return prompt

    def load_prompt_get_predicates(self, detected_object, detected_object_types, active_predicates: List or bool):
        prompt = f"Q. We are now going to do a {self.task} task whose goal is {self.task_description}"
        prompt += "There are many objects in this domain, " + \
                  "this is object information that comes from image observation. \n"
        prompt += f"1. {detected_object_types} \n2. {detected_object}\n"

        prompt += f"""\n(define (domain {self.task})
    (:requirements :strips :typing)
    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        ;define types of the task
    )
    (:predicates 
        ; general predicates

        ; robot predicates

        ; object property predicates

        ; result of object property after action
        
    )\n\n
"""
        if active_predicates:
            prompt += "Also you have to add predicates such as "
            for predicate in active_predicates:
                if predicate == active_predicates[-1]:
                    prompt += f"and {predicate}. \n"
                else:
                    prompt += predicate + ", "
        else:
            prompt += "We don't have to consider physical properties of the object."
        prompt += f"Add more predicates needed for {self.task}." + \
                  f"Don't add predicates that are not useful for {self.task} such as shape and color. \n"
        return prompt

    def load_prompt_ruled_predicates(self,
                                     original_pddl,
                                     robot_action,
                                     task_instruction):
        prompt = f"This is a front part of the domain.pddl of the {self.task} task. \n"
        prompt += f"{original_pddl}"
        prompt += f"Here are robot actions and rules for bin_packing task. \n" + \
                  f"{robot_action}\n{task_instruction}\n"
        prompt += "Please add or modify the pddl predicates that are needed to be used for rules and actions. \n"
        return prompt

    def load_prompt_robot_action(self,
                                 grounded_predicates,
                                 robot_action,
                                 task_instruction):
        prompt = ""
        return prompt


    def load_prompt_planning(self,
                             object_class_python_script,
                             robot_class_python_script,
                             init_state_python_script,
                             robot_action,
                             task_instruction):
        prompt = f"{object_class_python_script}\n\n"
        prompt += f"{robot_class_python_script}\n\n"
        prompt += f"{init_state_python_script}\n\n"
        prompt += "if __name__ == '__main__':\n\t# packing all object in the box\n\t# make a plan\n"

        prompt += f"Your goal is {self.task_description}. \n"
        prompt += "You must follow the rule: \n"
        prompt += f"""
{robot_action}
{task_instruction}\n"""

        prompt += "Make a plan under the if __name__ == '__main__':. \nYou must make a correct order. \n"
        return prompt

    def load_prompt_action_feedback(self, python_script, planning_output):
        prompt = f"We made a plan for a {self.task} and our goal is {self.task_description}. \n"
        prompt += f"Below is the Python code for it. \n\n"
        prompt += python_script + " \n"

        prompt += "And this is a result. \n"
        prompt += planning_output + " \n"

        prompt += "We find that there is an error in the robot action part that describes the preconditions and " + \
                  "effects of the action. \n"
        prompt += "Please modify the action preconditions if they use preconditions that the Object class doesn't use. \n"
        return prompt

    def load_prompt_planner_feedback(self, python_script, planning_output, task_instruction, robot_action):
        prompt = f"We made a plan for a {self.task} and our goal is {self.task_description}. \n"
        prompt += f"Below is the Python code for it. \n\n"
        prompt += python_script + " \n"

        prompt += "And this is a result. \n"
        prompt += planning_output + " \n"

        prompt += "There are some planning errors in this code that is represented as Cannot. \n" + \
                  " Here are some rules for planning. \n"
        prompt += f"{task_instruction}\n"
        prompt += f"{robot_action}\n"

        prompt += "Please re-planning under the if __name__ == '__main__' part. \n"

        return prompt
