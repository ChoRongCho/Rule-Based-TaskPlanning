import os
from datetime import datetime
from typing import List

import cv2
import torch
from groundingdino.util.inference import load_image, predict, annotate
from groundingdino.util.inference import load_model
from tabulate import tabulate
from torchvision.ops import box_convert

from script.gpt_model.gpt_prompt import GPTInterpreter
from script.utils.utils import parse_args


class FindObjects:
    def __init__(self, args):
        self.args = args
        self.task_name = args.task
        self.exp_name = args.name
        self.data_dir = args.data_dir
        self.input_image_name = args.input_image
        self.image_url = os.path.join(self.data_dir, self.input_image_name)
        self.is_save = args.is_save

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
        self.result_dir = os.path.join(args.result_dir, self.exp_name)
        self.gpt4 = GPTInterpreter(
            api_json=args.api_json,
            example_prompt_json=args.example_prompt_json,
            result_dir=self.result_dir,
            version="vision"
        )

        self.detected_object = {}
        self.prompt = f"We are now doing a {self.args.task} task which is packing all target objects into the box. \n"
        self.prompt += "This is a first observation where I work in. \n"
        self.prompt += "What objects or tools are here? \n"

    # Dinno
    def run_dinno(self):
        image_path = os.path.join(self.data_dir, self.input_image_name)
        image_source, image = load_image(image_path=image_path)

        boxes, logits, phrases = predict(
            model=self.model,
            image=image,
            caption=self.TEXT_PROMPT,
            box_threshold=self.BOX_THRESHOLD,
            text_threshold=self.TEXT_THRESHOLD
        )
        labels = [
            f"{phrase} {logit:.2f}"
            for phrase, logit
            in zip(phrases, logits)
        ]

        annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
        return boxes, phrases, annotated_frame

    def modifying_text_prompt(self, text_prompt: List):
        text_query = "".join([
            phrase + " ."
            for phrase in text_prompt
        ])
        self.TEXT_PROMPT = text_query

    def get_bbox(self):
        boxes, phrases, frame = self.run_dinno()
        h, w, _ = frame.shape
        boxes = boxes * torch.Tensor([w, h, w, h])
        xyxy = box_convert(boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()

        for points, phrase, index in zip(xyxy, phrases, range(len(xyxy))):
            x1, y1, x2, y2 = points.astype(int)
            self.detected_object.update({index: {phrase: [int((x1 + x2) / 2), int((y1 + y2) / 2), x2 - x1, y2 - y1]}})

        if self.is_save:
            new_name = "annotated_" + self.input_image_name
            cv2.imwrite(os.path.join(self.result_dir, new_name), frame)
        return self.detected_object

    # GPT
    def print_args(self):
        table = [["Project Time", datetime.now()],
                 ["Task", self.task_name],
                 ["Exp_Name", self.exp_name],
                 ["Input Image", self.input_image_name],
                 ["API JSON", self.args.api_json],
                 ["Example Prompt", self.args.example_prompt_json]]
        print(tabulate(table))

    def visual_interpreter(self, prompt, image_url):
        self.gpt4.add_example_prompt("init_state_message")
        self.gpt4.add_message_manual(role="user", content=prompt, image_url=image_url)
        answer = self.gpt4.run_manual_prompt(name=self.exp_name, is_save=self.is_save)
        result_dict, result_list = self.parse_input(answer=answer)
        return result_dict, result_list

    @staticmethod
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

    def run_find_obj(self):
        patience_repeat = 3
        for i in range(patience_repeat):
            try:
                print(f"Start {i}")
                result_dict, result_list = self.visual_interpreter(prompt=self.prompt, image_url=self.image_url)
                break
            except:
                raise Exception("Making expected answer went wrong. ")
        self.modifying_text_prompt(result_list)
        detected_object = self.get_bbox()
        return detected_object, result_dict


def main():
    args = parse_args()
    args.data_dir = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/val"
    find_obj = FindObjects(args)
    detected_object, detected_object_types = find_obj.run_find_obj()
    print(detected_object)
    print(detected_object_types)


if __name__ == '__main__':
    main()
