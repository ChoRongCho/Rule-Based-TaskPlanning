import random

from new_script.changmin_planner import ChangminPlanner
from new_script.utils.utils import parse_args_v2


def main():
    args = parse_args_v2()
    image_number = 8
    exp_number = 18
    args.exp_name = f"20240226_train_problem{image_number}_{exp_number}"
    args.input_image = f"train/problem{image_number}.jpg"
    args.max_predicates = random.randint(1, 6)

    planner = ChangminPlanner(args=args)
    planner.make_plan()
    # planner.planning_feedback()


if __name__ == '__main__':
    main()
