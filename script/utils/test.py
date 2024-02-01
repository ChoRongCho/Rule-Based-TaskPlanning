import json
from dataclasses import dataclass


@dataclass
class Robot:
    name: str = "ur5"
    purpose: str = None
    actions: dict = None


def main():
    predicates = ["water", "rigidity", "flexibility", "deformability", "fragility"]
    task = "bin packing"

    # Intro
    message = f"Hi, my name is changmin, and I am a robot. \n"
    message += f"Our goal is to pack a set of objects into a box, which is called {task}. " + \
               "In a problem instance, there is a box, a manipulator robot(it's me!), and objects set. \n"

    # Add predicates
    if len(predicates) == 0:
        message += "Actions must consider the predicates in preconditions and effects. \n"

    else:
        message += "We want to consider physical properties of the objects such as "

        for predicate in predicates:
            if predicate == predicates[-1]:
                message += "and " + predicate + ". \n"
            else:
                message += predicate + ", "

        message += "Given this goal, I want to make a domain.pddl" + \
                   " considering the physical propoerties of the objects. " + \
                   f"The domain file is supposed to include predicates such as is_{predicates[0]}. " + \
                   "Actions must consider the predicates in preconditions and effects. "

        print(message)


if __name__ == '__main__':
    main()
