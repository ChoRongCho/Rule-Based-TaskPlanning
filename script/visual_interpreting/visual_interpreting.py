import os
from datetime import datetime

from groundingdino.util.inference import load_model
from tabulate import tabulate

from script.gpt_model.gpt_prompt import GPTInterpreter
from script.utils.utils import parse_args


class FindObjects:
    def __init__(self, args):
        self.args = args
        self.task_name = args.task
        self.exp_name = args.name

        # Get Visual Interpreter
        self.model_dir = "/home/changmin/PycharmProjects/research/GroundingDINO"
        self.gd_dir = os.path.join(self.model_dir, "groundingdino/config/GroundingDINO_SwinT_OGC.py")
        self.check_dir = os.path.join(self.model_dir, "weights/groundingdino_swint_ogc.pth")
        self.model = load_model(self.gd_dir, self.check_dir)
        self.BOX_THRESHOLD = 0.25
        self.TEXT_THRESHOLD = 0.25

        text_phrases = [
            "objects",
            "white box"
        ]

        self.TEXT_PROMPT = "".join([
            phrase + " ."
            for phrase in text_phrases
        ])

        # GPT4
        self.gpt4 = GPTInterpreter(
            api_json=args.api_json,
            example_prompt_json=args.example_prompt_json,
            result_dir=args.result_dir,
            version="vision"
        )

    def print_args(self):
        table = [["Project Time", datetime.now()],
                 ["Task", self.task_name],
                 ["Exp_Name", self.exp_name],
                 ["API JSON", self.args.api_json],
                 ["Example Prompt", self.args.example_prompt_json]]
        print(tabulate(table))

    def visual_interpreter(self, prompt, image_url):
        self.gpt4.add_example_prompt("init_state_message")
        self.gpt4.add_message_manual(role="user", content=prompt, image_url=image_url)
        answer = self.gpt4.run_manual_prompt(name=self.exp_name, is_save=True)


def main():
    args = parse_args()
    data_path = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/val"
    find_obj = FindObjects(args)

    prompt = f"We are now doing a bin_packing task which is packing all target objects into the box. \n"
    prompt += "This is a first observation where I work in. \n"
    prompt += "What objects or tools are here? \n"

    for exp_name in ["problem15", "problem10", "problem17"]:
        for i in range(3):
            find_obj.exp_name = exp_name + f"_test{i}"
            find_obj.print_args()
            find_obj.visual_interpreter(prompt, data_path + f"/{exp_name}.jpg")


if __name__ == '__main__':
    main()
