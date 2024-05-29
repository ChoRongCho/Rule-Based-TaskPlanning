import os
import os.path
import random
import time

# from scripts.pddl_planner import PDDLPlanner
from scripts.python_planner import PythonPlanner
from scripts.utils.utils import parse_args_v2


def main():
    """
    --task_name
    bin_packing

    --exp_name
    packing_all

    --input_image
    problem1.jpg

    --api_json
    setting.json

    --example_prompt_json
    prompt_examples_python.json

    --robot_json
    robot.json

    --task_json
    task_instruction.json
    :return:
    """

    args = parse_args_v2()
    image_number = 8
    exp_number = 8
    args.exp_name = f"20240418_train_problem{image_number}_{exp_number}"
    args.input_image = f"train/problem{image_number}.jpg"
    args.max_predicates = random.randint(1, 6)

    # make plan
    planner = PythonPlanner(args=args)
    content = f"""This table defines the physical properties of the object we are investigating.
Answer the questions below in accordance with this criterion.
"""
    content += "\nThe first image shows before the robot presses an unknown object. " + \
               "The second image shows after the robot presses an object. Does this object have soft properties?" + \
               "Answer with the template below \nAnswer: \nReason: "

    role = "user"
    print(content)
    image_dir = "/data/bin_packing/property_search_database/my_data/obj1_side"
    image_url1 = os.path.join(image_dir, "Capture_obj1_frame671.jpg")
    image_url2 = os.path.join(image_dir, "Capture_obj1_frame901.jpg")
    image_url = [image_url1, image_url2]
    answer = planner.just_chat(message=content, role=role, image_url=image_url)
    print(answer)


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


def temp3():
    for obj_num in range(2, 3):
        root = f"/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/property_search_database/obj{obj_num}"
        data_path = list_file(root)
        data_path = sort_files(data_path)

        i, j, k = False, False, False
        # push image
        for data_name in data_path:
            if "push" in data_name:
                i = True
                continue
            if "fold" in data_name:
                j = True
                continue
            if "pull" in data_name:
                k = True
                continue

        system_message = f"You're working to verify the object's properties through images." + \
                         f"This table defines the physical properties of the object we are investigating." + \
                         f"Answer the questions below in accordance with this criterion. \n"
        system_message += """
---------------  -------------------------------------------------------
Predicates List  Definition
is_fragile       the fact of tending to break or be damaged easily
is_rigid         the fact of being very strict and difficult to change
is_soft          the quality of changing shape easily when pressed
is_foldable      the ability to bend without breaking
is_elastic       the quality of returning to its original size and shape
---------------  -------------------------------------------------------
"""
        args = parse_args_v2()
        image_number = 8
        exp_number = 8
        args.exp_name = f"20240418_train_problem{image_number}_{exp_number}"
        args.input_image = f"train/problem{image_number}.jpg"
        args.max_predicates = random.randint(1, 6)
        #
        # # make plan
        planner = PythonPlanner(args=args)
        prompt = planner.load_prompt.load_verification_module([i, j, k])
        print("-" * 90)
        print(data_path)
        planner.gpt_interface_vision.reset_message()
        planner.gpt_interface_vision.add_message(role="system", content=system_message, image_url=False)
        planner.gpt_interface_vision.add_message(role="user", content=prompt, image_url=data_path)

        start_time = time.time()
        ans = planner.gpt_interface_vision.run_prompt()
        end_time = time.time()
        print(ans)
        print(f"time: {end_time - start_time} s ")


def temp2():
    """
    obj3: soft, not foldable elastic
    :return:
    """
    for num in range(1, 9):
        im1 = f"/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/property_search_database/obj{num}/obj{num}_side_base_image.jpg"
        im2 = f"/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/property_search_database/obj{num}/obj{num}_top_base_image.jpg"
        args = parse_args_v2()
        image_number = 8
        exp_number = 8
        args.exp_name = f"20240418_train_problem{image_number}_{exp_number}"
        args.input_image = f"train/problem{image_number}.jpg"
        args.max_predicates = random.randint(1, 6)

        # prompt
        system_message = "You are a vision AI that describes the shape and color of an object. " + \
                         "You should look at a picture of a given object and explain its size and color."
        prompt = "The first image is when you see the object from the side " + \
                 "and the next image is when you see the object from the top. \n" + \
                 "Define the shape and color of the object through this image. \n" + \
                 "Use the simple classification table below for the shape of the object. \n" + \
                 """
-----  ----------------------------------------------             
Shape  Examples
1D     linear or ring
2D     flat rectangle, circle, etc
3D     cube, cuboid, cylinder, cone, polyhedron, etc
-----  ----------------------------------------------

Please answer with the template below:

Answer
Object Name: color_dimension_shape object
*Example: white_3D_cube object

Descriptions about object
*your descriptions in 300 words

"""

        # make plan
        planner = PythonPlanner(args=args)
        # print(system_message)
        # print(prompt)
        planner.gpt_interface_vision.reset_message()
        planner.gpt_interface_vision.add_message(role="system", content=system_message, image_url=False)
        planner.gpt_interface_vision.add_message(role="user", content=prompt, image_url=[im1, im2])

        start_time = time.time()
        ans = planner.gpt_interface_vision.run_prompt()
        end_time = time.time()
        print(ans)
        print(f"time: {end_time - start_time} s ")
        print("-"*50)


if __name__ == '__main__':
    temp2()
