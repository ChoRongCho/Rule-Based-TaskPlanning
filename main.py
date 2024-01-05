import time
import os
from script.gpt_model.gpt_prompt import GPTInterpreter


def main():
    api_json = "/home/changmin/PycharmProjects/GPT_examples/instructions/setting.json"
    prompt_json = "/home/changmin/PycharmProjects/GPT_examples/instructions/pddl_prompt.json"

    save_file_name = time.strftime("result_%y%m%d_%H%M%S", time.localtime(int(time.time()))) + ".json"
    save_path = os.path.join("/home/changmin/PycharmProjects/GPT_examples/response", save_file_name)
    gpt4 = GPTInterpreter(api_json=api_json,
                          prompt_json=prompt_json,
                          save_path=save_path)
    gpt4.run()


if __name__ == '__main__':
    main()
