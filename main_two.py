from new_script.changmin_planner import ChangminPlanner
from new_script.utils.utils import parse_args_v2


def main():
    args = parse_args_v2()
    args.exp_name = "20240220_final_test_4"
    planner = ChangminPlanner(args=args)
    planner.run_all()


if __name__ == '__main__':
    main()
