import argparse


def parse_args_v2():
    parser = argparse.ArgumentParser()

    # task and experiment setting
    parser.add_argument("--task_name", type=str or int, default=None, help="domain name")
    parser.add_argument("--exp_name", type=str, default=None, help="Experiment name")
    parser.add_argument("--is_save", type=bool, default=True, help="save the response")
    parser.add_argument("--max_predicates", type=int, default=5, help="number of predicates you want to generate")

    # additional path
    parser.add_argument("--data_dir", type=str, default="/home/changmin/PycharmProjects/GPT_examples/data", help="")
    parser.add_argument("--json_dir", type=str, default="/home/changmin/PycharmProjects/GPT_examples/data/json", help="")
    parser.add_argument("--result_dir", type=str, default="/home/changmin/PycharmProjects/GPT_examples/result", help="")
    parser.add_argument("--input_image", type=str, default=None, help="image name from data_dir")

    # json_dir
    parser.add_argument("--api_json", type=str, default=None, help="")
    parser.add_argument("--example_prompt_json", type=str, default=None, help="")
    parser.add_argument("--robot_json", type=str, default=None, help="")
    parser.add_argument("--task_json", type=str, default=None, help="")

    # related to problem generation and refinement
    parser.add_argument("--seed", type=int, default=42, help="random seed")

    args = parser.parse_args()
    return args


def parse_input(answer):
    objects_out_box = []
    objects_in_box = []
    bin_content = ""

    lines = answer.split('\n')
    for line in lines:
        if line.startswith(" Objects_out_box:" or "Objects_out_box:"):
            objects_out_box = line.split(": ")[1].split(", ")
        elif line.startswith(" Objects_in_box:" or "Objects_in_box:"):
            objects_in_box = line.split(": ")[1].split(", ")
        elif line.startswith(" Bin:" or "Bin:"):
            bin_content = line.split(": ")[1].split(", ")

    unique_objects = list(set(objects_out_box + objects_in_box + bin_content))

    output_dict = {
        "Objects_out_box": objects_out_box,
        "Objects_in_box": objects_in_box,
        "Bin": bin_content
    }

    return output_dict, unique_objects
