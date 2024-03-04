import random

from new_script.changmin_planner import ChangminPlanner
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
    planner = ChangminPlanner(args=args)

    message = ""

    answer = planner.just_chat(message=message)
    print(answer)


if __name__ == '__main__':
    main()
