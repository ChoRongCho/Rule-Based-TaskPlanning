import numpy as np


class PDDL:
    def __init__(self,
                 pddl_domain: str,
                 common_instruction: str):
        self.pddl_domain = pddl_domain
        self.available_action = None
        self.parse_agent()
        self.common_instruction = common_instruction

    def parse_agent(self):
        """ get available action """
        pass

    def type_generator(self):
        pass

    def predicate_generator(self):
        parameters = None
        return parameters

    def action_precondition(self):
        pass

    def action_effect(self):
        pass

    def generate_domain(self, old_pddl, state):
        return "test1_domain.pddl"

