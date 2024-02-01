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
        self.name = args.name

        # Get Visual Interpreter
        self.model_dir = "/home/changmin/PycharmProjects/research/GroundingDINO"
        self.gd_dir = os.path.join(self.model_dir, "groundingdino/config/GroundingDINO_SwinT_OGC.py")
        self.check_dir = os.path.join(self.model_dir, "weights/groundingdino_swint_ogc.pth")
        self.model = load_model(self.gd_dir, self.check_dir)
        self.BOX_THRESHOLD = 0.35
        self.TEXT_THRESHOLD = 0.25

        text_phrases = [
            "blue disk",
            "green disk",
            "yellow disk",
            "purple disk",
            "orange disk",
            "pink disk",
            "wooden stick",
        ]

        self.TEXT_PROMPT = "".join([
            phrase + " ."
            for phrase in text_phrases
        ])

        # GPT4
        self.gpt4 = GPTInterpreter(
            api_json=args.api_json,
            prompt_json=False,
            result_dir=args.result_dir,
            version="vision"
        )

    def print_args(self):
        table = [["Project Time", datetime.now()],
                 ["Task", self.task_name],
                 ["Exp_Name", self.name]]
        print(tabulate(table))

    def visual_interpreter(self, image_url):
        prompt = f"We are now doing a {self.task_name} task. \nThis is a first observation where I work in. \n"
        prompt += "What objects or tools are here? \n"

        self.gpt4.add_message_manual(role="user", content=prompt, image_url=image_url)
        answer = self.gpt4.run_manual_prompt(name="", is_save=False)
        print(answer)


def main():
    args = parse_args()
    find_obj = FindObjects(args)
    find_obj.print_args()
    find_obj.visual_interpreter("/home/changmin/PycharmProjects/GPT_examples/data/cooking/problem6.jpg")

if __name__ == '__main__':
    main()