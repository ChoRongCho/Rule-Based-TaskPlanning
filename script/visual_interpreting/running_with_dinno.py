import os

import cv2
from groundingdino.util.inference import load_image, load_model, predict, annotate


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
        self.TEXT_PROMPT = "objects . "

        # TEXT_PROMPT = "tiger . bird . bear ."
        self.BOX_TRESHOLD = 0.25
        self.TEXT_TRESHOLD = 0.25

    def run_dinno(self):
        image_source, image = load_image(self.IMAGE_PATH)

        boxes, logits, phrases = predict(
            model=self.model,
            image=image,
            caption=self.TEXT_PROMPT,
            box_threshold=self.BOX_TRESHOLD,
            text_threshold=self.TEXT_TRESHOLD
        )
        new_name = "annotated_" + self.name
        annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
        cv2.imwrite(os.path.join(self.save_path, new_name), annotated_frame)

    def modifying_text_prompt(self, text_prompt: str):
        self.TEXT_PROMPT = text_prompt


def main():
    visual_interpreter = MyDino(
        name="problem2.jpg",
        image_path="/home/changmin/PycharmProjects/GPT_examples/data/hanoi",
        save_path="/home/changmin/PycharmProjects/GPT_examples/data/hanoi"
    )
    visual_interpreter.run_dinno()
    print("Done")


if __name__ == '__main__':
    main()
