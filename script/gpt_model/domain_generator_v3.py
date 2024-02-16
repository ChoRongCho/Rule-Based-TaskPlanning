import os

from script.gpt_model.gpt_prompt import GPTInterpreter


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
                 args):
        self.args = args
        self.task_name = args.task
        self.exp_name = args.name
        self.data_dir = args.data_dir
        self.is_save = args.is_save
        self.max_predicates = args.max_predicates

        self.all_answer = {
            "type_prompt": [],
            "object_prompt": [],
            "predicates_prompt": [],
            "action_prompt": [],
        }
        self.result_dir = os.path.join(args.result_dir, self.exp_name)
        self.gpt4 = GPTInterpreter(
            api_json=args.api_json,
            example_prompt_json=args.example_prompt_json,
            result_dir=self.result_dir,
            version="pddl"
        )

    def get_predicates(self, detected_object, detected_object_types, active_predicate: bool or list=False):
        """
        # after robot active search for object properties
        input: objects list
        output: object predicates
        """
        content = f"We are now going to do a {self.task_name} task whose goal is {task_description}"
        content += "There are many objects in this domain, " + \
                   "this is object information that comes from image observation. \n"
        content += f"1. {detected_object_types} \n2. {detected_object}\n"
        content += f"""from dataclasses import dataclass


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
    
    # {self.task_name} Predicates (max {self.max_predicates})
    
        """
        content += "However, we cannot do complete planning with this dataclass predicate alone" + \
                   f" that means we have to add another predicates that fully describe the {self.task_name}."
        if active_predicate:
            content += "Also you have to add predicates such as "
            for predicate in active_predicate:
                if predicate == active_predicate[-1]:
                    content += f"and {predicate}. \n"
                else:
                    content += predicate + ", "
        else:
            content += "We don't have to consider physical properties of the object."

        content += f"Add more predicates needed for {self.task_name} to class Object. "

        print(content)
        # self.gpt4.add_example_prompt("domain_message")
        # self.gpt4.add_message_manual(role="user", content=content, image_url=False)


    def active_predicates(self):
        pass

    def task_predicates(self):
        pass

    def get_action_conditions(self):
        pass

    def gen_domain(self):
        pass
