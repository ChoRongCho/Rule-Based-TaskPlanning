import random

# from scripts.pddl_planner import PDDLPlanner
from scripts.python_planner import PythonPlanner
from scripts.utils.utils import parse_args_v2


def main():
    args = parse_args_v2()
    image_number = 12
    exp_number = 2
    args.exp_name = f"20240311_val_problem{image_number}_{exp_number}"
    args.input_image = f"val/problem{image_number}.jpg"
    args.max_predicates = random.randint(1, 6)

    # planner = PDDLPlanner(args=args)
    # planner.generate_domain_pddl()

    planner = PythonPlanner(args=args)
    # planner.plan_and_run()
    # planner.feedback()
    planner.goal_state_encoding(message=False)


if __name__ == '__main__':
    main()
