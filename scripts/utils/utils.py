import argparse
import os.path

import cv2
import numpy as np


def parse_args_v2():
    parser = argparse.ArgumentParser()

    # task and experiment setting
    parser.add_argument("--task_name", type=str or int, default=None, help="domain name")
    parser.add_argument("--exp_name", type=str, default=None, help="Experiment name")
    parser.add_argument("--is_save", type=bool, default=True, help="save the response")
    parser.add_argument("--max_predicates", type=int, default=5, help="number of predicates you want to generate")

    # additional path
    parser.add_argument("--data_dir", type=str, default="/home/changmin/PycharmProjects/GPT_examples/data", help="")
    parser.add_argument("--json_dir", type=str, default="/home/changmin/PycharmProjects/GPT_examples/data/json",
                        help="")
    parser.add_argument("--result_dir", type=str,
                        default="/home/changmin/PycharmProjects/GPT_examples/new_result/train", help="")
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


def merge_image(name, image_dir):
    images = []
    before_after = [0, 1]
    actions = ["push", "pull", "fold"]
    for at in actions:
        for ba in before_after:
            image_name = f"{name}_{at}_{ba}.png"
            image_path = os.path.join(image_dir, image_name)
            image = cv2.imread(image_path)
            print(image.shape)
            images.append(image)
    image1 = np.concatenate([images[0], images[1]], axis=0)
    image2 = np.concatenate([images[2], images[3]], axis=0)
    image3 = np.concatenate([images[4], images[5]], axis=0)
    total_image = np.concatenate([image1, image2, image3], axis=1)
    h, w, _ = total_image.shape
    all_new_image = cv2.resize(total_image, (w // 2, h // 2))
    cv2.line(all_new_image, (320 - 1, 0), (320 - 1, 480), color=(0, 0, 255), thickness=3)
    cv2.line(all_new_image, (640 - 1, 0), (640 - 1, 480), color=(0, 0, 255), thickness=3)
    cv2.imshow("asdf", all_new_image)

    save_dir = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/predicates_prove"
    save_name = os.path.join(save_dir, f"{name}.png")
    cv2.imwrite(save_name, all_new_image)
    cv2.waitKey(0)


def int_to_ordinal(n):
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = suffixes.get(n % 10, 'th')
    return str(n) + suffix


def list_file(directory):
    entries = os.listdir(directory)
    files = [os.path.join(directory, entry) for entry in entries if os.path.isfile(os.path.join(directory, entry))]
    return files


def sort_files(file_list):
    # 키워드와 우선순위 매핑
    keyword_order = {
        'base': 0,
        'push': 1,
        'fold': 2,
        'pull': 3
    }

    # 파일명에서 키워드 추출 및 정렬
    def get_keyword(file_name):
        for keyword in keyword_order:
            if keyword in file_name:
                return keyword_order[keyword], file_name
        return len(keyword_order), file_name  # 키워드가 없으면 마지막에 정렬

    # 파일 목록 정렬
    sorted_files = sorted(file_list, key=get_keyword)
    return sorted_files
