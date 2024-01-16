from pddl_generator import Robot

task_number = {
    0: "bin_packing",
    1: "hanoi",
    2: "blocksworld",
    3: "cooking"
}


class PromptEncoding:
    def __init__(self,
                 task: str or int,
                 robot: Robot,
                 predicates,
                 ):
        """

        :param task:
        """
        self.task = task
        self.robot = robot
        self.predicates = predicates

        self.prompt_predicates = ""
        self.prompt_instruction = ""
        self.prompt_pddl = ""

    def intro_encoding(self):
        message = f"Hi, my name is {self.robot.name}, and I am a robot. \n"
        # Intro, inform GPT what will do.
        if self.task == 0 or "bin_packing":
            message += f"Our goal is {self.robot.goal}, which is called {self.task}. " + \
                       "In a problem instance, there is a box, a manipulator robot(it's me!), and objects set. \n"
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

        elif self.task == 1 or "hanoi":
            message += f"Our goal is {self.robot.goal}, which is called {self.task}. " + \
                       "In a problem instance, there are lings, a manipulator robot(it's me!), and a tower. \n"
            message = self.task_prompt(message)

        elif self.task == 2 or "blocksworld":
            message += f"Our goal is {self.robot.goal}, which is called {self.task}. " + \
                       "In a problem instance, there are blocks and a manipulator robot(it's me!). \n"
            message = self.task_prompt(message)

        elif self.task == 3 or "cooking":
            message += f"Our goal is {self.robot.goal}, which is called {self.task}. " + \
                       "In a problem instance, there are vegetables, tools and a manipulator robot(it's me!). \n"
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
            message += "Given this goal, I want to make a domain.pddl"
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
        message += "Please generate the only pddl without any explanation to return your answer to pddl file."
        self.prompt_pddl = message
