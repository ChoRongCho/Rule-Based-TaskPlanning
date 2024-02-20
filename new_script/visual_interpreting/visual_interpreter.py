import os
from typing import List

import cv2
import torch
from groundingdino.util.inference import load_image, predict, annotate
from groundingdino.util.inference import load_model
from torchvision.ops import box_convert


class FindObjects:
    def __init__(self, is_save=True):
        # Get Visual Interpreter
        self.is_save = is_save
        self.model_dir = "/home/changmin/PycharmProjects/research/GroundingDINO"
        self.gd_dir = os.path.join(self.model_dir, "groundingdino/config/GroundingDINO_SwinT_OGC.py")
        self.check_dir = os.path.join(self.model_dir, "weights/groundingdino_swint_ogc.pth")
        self.model = load_model(self.gd_dir, self.check_dir)
        self.BOX_THRESHOLD = 0.25
        self.TEXT_THRESHOLD = 0.25

        self.TEXT_PROMPT = ""
        self.detected_object = {}

    # Dinno
    def run_dinno(self, image_path):
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

    def get_bbox(self, image_path, result_dir):
        boxes, phrases, frame = self.run_dinno(image_path)
        h, w, _ = frame.shape
        boxes = boxes * torch.Tensor([w, h, w, h])
        xyxy = box_convert(boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()

        for points, phrase, index in zip(xyxy, phrases, range(len(xyxy))):
            x1, y1, x2, y2 = points.astype(int)
            self.detected_object.update({index: {phrase: [int((x1 + x2) / 2), int((y1 + y2) / 2), x2 - x1, y2 - y1]}})

        if self.is_save:
            new_name = "annotated_observation.jpg"
            cv2.imwrite(os.path.join(result_dir, new_name), frame)
        return self.detected_object


