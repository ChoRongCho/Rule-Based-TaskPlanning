from new_script.changmin_planner import ChangminPlanner
from new_script.utils.prompt_function import PromptSetPDDL


class PDDLPlanner(ChangminPlanner):
    def __init__(self, args):
        super().__init__(args=args)
        self.args = args
        self.load_prompt = PromptSetPDDL(task=self.task, task_description=self.task_description)

    def get_predicates1(self, detected_object, detected_object_types, active_predicates):
        """
        return a basic predicates structure
        """
        prompt = self.load_prompt.load_prompt_get_predicates(detected_object, detected_object_types, active_predicates)
        self.gpt_interface_pddl.reset_message()
        self.gpt_interface_pddl.add_example_prompt("predicates1_message")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        try:
            answer = self.gpt_interface_pddl.run_prompt()
            self.question.append(prompt)
            self.answer.append(answer)
            return answer
        except:
            raise Exception("Making expected answer went wrong. ")

    def get_predicates2(self, predicates_pddl):
        """
        return a rule_grounded predicates structure
        """
        prompt = self.load_prompt.load_prompt_ruled_predicates(original_pddl=predicates_pddl,
                                                               robot_action=self.robot_data["actions"],
                                                               task_instruction=self.task_data["instructions"])
        self.gpt_interface_pddl.add_example_prompt("predicates2_message")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        try:
            answer = self.gpt_interface_pddl.run_prompt()
            self.question.append(prompt)
            self.answer.append(answer)
            return answer
        except:
            raise Exception("Making expected answer went wrong. ")

    def get_robot_action_conditions(self, grounded_predicates):
        prompt = self.load_prompt.load_prompt_robot_action(grounded_predicates=grounded_predicates,
                                                           robot_action=self.robot_data["actions"],
                                                           task_instruction=self.task_data["instructions"])
        self.gpt_interface_pddl.add_example_prompt("robot_action_message")
        self.gpt_interface_pddl.add_message(role="user", content=prompt, image_url=False)
        try:
            answer = self.gpt_interface_pddl.run_prompt()
            self.question.append(prompt)
            self.answer.append(answer)
            return answer
        except:
            raise Exception("Making expected answer went wrong. ")

    def get_init_state(self,
                       detected_object,
                       detected_object_types,
                       detected_object_predicates,
                       object_class_python_script):
        pass

    def planning_from_domain(self, object_class_python_script, robot_class_python_script, init_state_python_script):
        pass

    def generate_domain_pddl(self):
        # object detection
        detected_object, detected_object_types = self.detect_object()

        # get active predicates
        active_predicates, detected_object_predicates = self.get_active_predicates(detected_object=detected_object)

        # get structured pddl predicates
        predicates_pddl = self.get_predicates1(detected_object=detected_object,
                                               detected_object_types=detected_object_types,
                                               active_predicates=active_predicates)
        grounded_predicates = self.get_predicates2(predicates_pddl=predicates_pddl)
        print(grounded_predicates)

        # get robot action pddl
        domain_pddl = self.get_robot_action_conditions(grounded_predicates=grounded_predicates)
        return domain_pddl


    def generate_problem_pddl(self, domain_pddl):
        # generate problem.pddl using generated pddl
        # object2pddl
        # init_state
        # goal_state
        # gen_problem.pddl
        problem_pddl = ""

        return problem_pddl

    

