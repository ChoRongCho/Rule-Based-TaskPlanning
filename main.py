import time
import os
from script.gpt_model.pddl_generator import PDDL
from script.utils.utils import parse_args, seed_all_types


# def main2():
#     api_json = "/home/changmin/PycharmProjects/GPT_examples/instructions/setting.json"
#     prompt_json = "/home/changmin/PycharmProjects/GPT_examples/instructions/my_personal.json"
#
#     save_file_name = time.strftime("result_%y%m%d_%H%M%S", time.localtime(int(time.time()))) + ".json"
#     save_path = os.path.join("/home/changmin/PycharmProjects/GPT_examples/response", save_file_name)
#     gpt4 = GPTInterpreter(api_json=api_json,
#                           prompt_json=prompt_json,
#                           result_dir=save_path)
#     gpt4.run_json_prompt()
#

def main():
    args = parse_args()
    seed_all_types(args.seed)

    predicates = ["flexible", "rigid", "soft", "fragile"]
    pddl_gen = PDDL(args=args, predicates=predicates)
    pddl_gen.run()


if __name__ == '__main__':
    main()
