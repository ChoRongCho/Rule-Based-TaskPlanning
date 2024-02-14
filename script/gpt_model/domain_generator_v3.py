import re

from script.database.database import Robot


class DomainGen:
    """

    def get_domain_from_observation(): == def get_objects_from_observation():
        input: images, task_information
        output: objects list, types
        1. for image in images
            add message with task description
            ask gpt what is here and what can be divided as a type
        3. after get types: modifying text_prompt of the ground_dino
        4. get bound_box(loc and size), color, object_types
        5. for all object return objects_list


    def get_predicate():
        # after robot active search for object properties
        input: objects list, types
        output: object predicates

    def get_action_conditions():
        input: object predicates, object list, robot action set
        output: conditioned robot action set

    def run():
        objects_list, objects_types = self.get_objects_from_observation(images, task_information)
        new_object_list, new_object_predicates = self.get_predicates(objects_list, new_predicates)
        new_robot_action_set = self.get_action_conditions(new_object_predicates, new_objects_list, robot_action_set)

        return new_object_list, new_object_predicates, new_robot_action_set

    """

    def __init__(self,
                 args,
                 robot: Robot,
                 task_prompt,
                 prompt_examples,
                 gpt4_vision,
                 gpt4_text):
        self.args = args
        self.task_name = self.args.task_name
        self.robot = robot

        self.task_prompt = task_prompt
        self.prompt_examples = prompt_examples

        self.gpt4_vision = gpt4_vision
        self.gpt4_text = gpt4_text

        self.all_answer = {
            "type_prompt": [],
            "object_prompt": [],
            "predicates_prompt": [],
            "action_prompt": [],
        }

    def get_objects_from_observations(self, images: list or str):
        """
        input: images, task_information
        output: objects list, types
        1. for image in images
            add message with task description
            ask gpt what is here and what can be divided as a type
        3. after get types: modifying text_prompt of the ground_dino
        4. get bound_box(loc and size), color, object_types
        5. for all object return objects_list

        :param images:
        :return:
        """
        task_info = self.task_prompt["task_description"]
        prompt = f"We are going to do a {self.task_name} task which is {task_info}. " + \
                 "\nThese are the observations where I'm going to work. \n"
        prompt += "What objects or tools are here? \n"

        self.gpt4_vision.add_message_manual(role="user", content=prompt, image_url=images)
        answer = self.gpt4_vision.run_manual_prompt(name="", is_save=False)
        self.all_answer["type_prompt"].append(answer)

        self.gpt4_vision.add_message_manual(role="assistant", content=answer, image_url=False)

        def type_parser(type_answer: str, types: dict):
            pattern = re.compile(r'(\d+)\.\s*([\w\s]+):\s*([^\.]+)\.')
            matches = pattern.findall(type_answer)
            for match in matches:
                index, type_name, type_val = match
                type_name = type_name.lower().strip()
                type_val = [value.strip() for value in type_val.split(',')]
                types[type_name] = type_val
            return types

        # # initialize the prompt
        # prompt += "There are many objects in interest such as "
        # for obj in objects_list:
        #     if obj == objects_list[-1]:
        #         prompt += "and " + "obj" + ". \n"
        #     else:
        #         prompt += obj + ", "
        prompt += "Divide the character of the object according to the task. \n"
        # prompt =

    def get_predicates(self, objects_list, robot_info):
        """
        # after robot active search for object properties
        input: objects list
        output: object predicates
        """
        prompt = f"""
        @dataclass
        class Objects
            # Basic dataclass
            index: int
            name: str
            location: tuple
            color: str or bool
            object_type: str        
        
        """
        rule = self.task_prompt

        pass

    def active_predicates(self):
        pass

    def task_predicates(self):
        pass

    def get_action_conditions(self):
        pass

    def gen_domain(self):
        pass
