import os

import cv2
from groundingdino.util.inference import load_image, load_model, predict, annotate

names = [
    "BlackRigid_fold_0.png",
    "BlackRigid_fold_1.png",
    "BlackRigid_pull_0.png",
    "BlackRigid_pull_1.png",
    "BlackRigid_push_0.png",
    "BlackRigid_push_1.png",
    "BlueFlexible_fold_0.png",
    "BlueFlexible_fold_1.png",
    "BlueFlexible_pull_0.png",
    "BlueFlexible_pull_1.png",
    "BlueFlexible_push_0.png",
    "BlueFlexible_push_1.png",
    "GreenElastic_fold_0.png",
    "GreenElastic_fold_1.png",
    "GreenElastic_pull_0.png",
    "GreenElastic_pull_1.png",
    "GreenElastic_push_0.png",
    "GreenElastic_push_1.png",
    "SkyRigid_fold_0.png",
    "SkyRigid_fold_1.png",
    "SkyRigid_pull_0.png",
    "SkyRigid_pull_1.png",
    "SkyRigid_push_0.png",
    "SkyRigid_push_1.png",
    "YellowFoldable_fold_0.png",
    "YellowFoldable_fold_1.png",
    "YellowFoldable_pull_0.png",
    "YellowFoldable_pull_1.png",
    "YellowFoldable_push_0.png",
    "YellowFoldable_push_1.png",
    "BrownSoft_fold_0.png",
    "BrownSoft_fold_1.png",
    "BrownSoft_pull_0.png",
    "BrownSoft_pull_1.png",
    "BrownSoft_push_0.png",
    "BrownSoft_push_1.png",
]


def main():
    model_dir = "/home/changmin/PycharmProjects/research/GroundingDINO"
    gd_dir = os.path.join(model_dir, "groundingdino/config/GroundingDINO_SwinT_OGC.py")
    check_dir = os.path.join(model_dir, "weights/groundingdino_swint_ogc.pth")

    model = load_model(gd_dir, check_dir)
    """ linear, triangle, octagon, rectangle """
    image_path = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/active_prove"
    save_path = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/active_prove"

    i = 0
    for name in names:
        i += 1
        print(i)
        IMAGE_PATH = os.path.join(image_path, name)
        # TEXT_PROMPT = "black object. brown object. yellow object. sky object. green object. blue object"
        TEXT_PROMPT = "object. "
        # TEXT_PROMPT = "tiger . bird . bear ."
        BOX_TRESHOLD = 0.35
        TEXT_TRESHOLD = 0.25

        image_source, image = load_image(IMAGE_PATH)

        boxes, logits, phrases = predict(
            model=model,
            image=image,
            caption=TEXT_PROMPT,
            box_threshold=BOX_TRESHOLD,
            text_threshold=TEXT_TRESHOLD
        )
        new_name = "annotated_" + name
        annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
        cv2.imwrite(os.path.join(save_path, new_name), annotated_frame)


if __name__ == '__main__':
    main()
