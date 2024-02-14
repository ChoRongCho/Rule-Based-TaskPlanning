import os
import cv2
import torch
from groundingdino.util.inference import load_image, load_model, predict, annotate
from torchvision.ops import box_convert


class MyDino:
    def __init__(self,
                 name,
                 image_path,
                 save_path):
        self.name = name
        self.image_path = image_path
        self.save_path = save_path

        self.model_dir = "/home/changmin/PycharmProjects/research/GroundingDINO"
        self.gd_dir = os.path.join(self.model_dir, "groundingdino/config/GroundingDINO_SwinT_OGC.py")
        self.check_dir = os.path.join(self.model_dir, "weights/groundingdino_swint_ogc.pth")

        self.model = load_model(self.gd_dir, self.check_dir)
        self.IMAGE_PATH = os.path.join(self.image_path, self.name)
        self.TEXT_PROMPT = "objects . box . "

        # TEXT_PROMPT = "tiger . bird . bear ."
        self.BOX_TRESHOLD = 0.27
        self.TEXT_TRESHOLD = 0.25

        # return
        self.detected_object = {}

    def run_dinno(self):
        image_source, image = load_image(self.IMAGE_PATH)

        boxes, logits, phrases = predict(
            model=self.model,
            image=image,
            caption=self.TEXT_PROMPT,
            box_threshold=self.BOX_TRESHOLD,
            text_threshold=self.TEXT_TRESHOLD
        )
        labels = [
            f"{phrase} {logit:.2f}"
            for phrase, logit
            in zip(phrases, logits)
        ]

        annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
        return boxes, phrases, annotated_frame

    def modifying_text_prompt(self, text_prompt: str):
        self.TEXT_PROMPT = text_prompt

    def get_bbox(self):
        boxes, phrases, frame = self.run_dinno()
        h, w, _ = frame.shape
        boxes = boxes * torch.Tensor([w, h, w, h])
        xyxy = box_convert(boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()

        for points, phrase, index in zip(xyxy, phrases, range(len(xyxy))):
            x1, y1, x2, y2 = points.astype(int)
            self.detected_object.update({index: {phrase: [int((x1 + x2)/2), int((y1 + y2)/2), x2-x1, y2-y1]}})

        new_name = "annotated_" + self.name
        cv2.imwrite(os.path.join(self.save_path, new_name), frame)
        return self.detected_object


def main():
    # all_images = [
    #     "problem1.jpg",
    #     "problem5.jpg",
    #     "problem7.jpg"
    # ]

    # all_images = [
    #     "problem2.jpg",
    #     "problem3.jpg",
    #     "problem4.jpg",
    #     "problem6.jpg",
    #     "problem8.jpg",
    #     "problem9.jpg",
    #     "problem10.jpg",
    #     "problem11.jpg",
    #     "problem12.jpg",
    #     "problem13.jpg",
    #     "problem14.jpg",
    #     "problem15.jpg",
    #     "problem16.jpg",
    #     "problem17.jpg",
    # ]
    image_path = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/train"
    save_path = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/"

    visual_interpreter = MyDino(
            name="problem1.jpg",
            image_path=image_path,
            save_path=save_path
        )
    detected_obj = visual_interpreter.get_bbox()
    print(detected_obj)  # cx, cy, wx, hy


if __name__ == '__main__':
    main()
