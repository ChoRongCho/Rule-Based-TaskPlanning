import random

from new_script.changmin_planner import ChangminPlanner
from new_script.pddl_planner import PDDLPlanner
from new_script.utils.utils import parse_args_v2


def main():
    args = parse_args_v2()
    image_number = 8
    exp_number = 20
    args.exp_name = f"20240228_train_problem{image_number}_{exp_number}"
    args.input_image = f"train/problem{image_number}.jpg"
    args.max_predicates = random.randint(1, 6)

    planner = ChangminPlanner(args=args)
    # planner.make_plan()
    planner.planning_feedback()

    message = "how to get nagelkerke R-squared in stata using logistic regression?"
    answer = planner.just_chat(message=message)
    print(answer)


def just_chatting():
    args = parse_args_v2()

    # experiment setting
    image_number = 7
    args.input_image = f"train/problem{image_number}.jpg"

    planner = PDDLPlanner(args=args)
    # planner.make_plan()
#     message = "This is a front part of the domain.pddl of the bin_packing task. \n"
#     message += """(define (domain bin_packing)
#     (:requirements :strips :typing)
#     (:types object box robot)
#     (:predicates
#         ; general predicates
#         (in ?x - object ?y - box) ; object x is in the box y
#         (out ?x - object ?y - box) ; object x is out of the box y
#
#         ; robot predicates
#         (handempty ?x - robot) ; robot_hand is empty.
#         (handfull ?x - robot) ; robot hand is full, that means, robot is now holding something.
#         (holding ?x - object) ; robot is holding object x
#
#         ; object property predicates
#         (is_soft ?x - object) ; object x is soft
#         (is_foldable ?x - object) ; object x is foldable
#         (is_elastic ?x - object) ; object x is elastic
#         (is_fragile ?x - object) ; object x is fragile
#
#         ; add other predicates if you need. I'll leave this part to your imagination.
#     )
# )
# \n"""
#     actions = {'pick': 'pick an {object} which is not in the {bin}',
#                'place': 'place an {object} anywhere',
#                'push': 'push an {object} downward in the bin, hand must be empty when pushing',
#                'fold': 'fold an {object}, hand must be empty when folding',
#                'out': 'pick an {object} in {bin}'}
#     rules = {'rule0': 'you should never pick and place a box',
#              'rule1': 'when place a fragile objects, the soft objects must be in the bin',
#              'rule2': 'when fold a object, the object must be foldable',
#              'rule3': 'when push a object, neither fragile and rigid objects are permitted, but only soft objects dose',
#              'rule4': 'you must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object'}
#     message += f"Here are available robot actions and rules for bin_packing task. \n" + \
#                f"{actions}\n{rules}\n"
#     message += "Please add or modify the pddl predicates and define actions using only available actions. \n"
    message = "나는 domain.pddl과 problem.pddl을 가지고 있어. 나는 이것을 python script로 자동 실행하고 싶어. python library에" + \
        "이것을 실행시켜주는 planner tool이 있어? \n"

    answer = planner.just_chat(message=message)
    print(message)
    print("-"*90)
    print(answer)


if __name__ == '__main__':
    just_chatting()
