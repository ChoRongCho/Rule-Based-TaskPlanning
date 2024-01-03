import os.path

from script.gpt_model.gpt_communicator import GPT4Vision, GPT4Text


def run_gpt4_vision(api_json_path, prompt_file_path, target_image_path):
    image_path0 = "data/object_shape_examples/1d_shape.jpg"
    image_path1 = "data/object_shape_examples/2d_shape.png"
    image_path2 = "data/object_shape_examples/3d_shape.jpeg"
    image_path3 = "data/object_shape_examples/test_0.png"
    image_path4 = "data/object_shape_examples/test_1.jpg"
    # image_path5 = "data/fold_examples/annotated_cropped_cushion_before.jpg"
    ask_gpt = GPT4Vision(api_json_path=api_json_path,
                         prompt_file_path=prompt_file_path,
                         max_token=100)

    ask_gpt.add_message(image_path0)
    ask_gpt.add_message(image_path1)
    ask_gpt.add_message(image_path2)
    ask_gpt.add_message(image_path3)
    ask_gpt.add_message_text_only(role="assistant")
    ask_gpt.add_message(image_path4)
    ask_gpt.add_message_text_only(role="assistant")
    ask_gpt.add_message(target_image_path)
    ask_gpt.run()


def run_gpt4_text(api_json_path, prompt_file_path):
    role1 = "user"
    role2 = "assistant"

    ask_gpt = GPT4Text(api_json_path=api_json_path,
                       prompt_file_path=prompt_file_path,
                       max_token=1000)
    ask_gpt.add_message(role=role1)
    # ask_gpt.add_message(role=role2)
    # ask_gpt.add_message(role=role1)
    # print(ask_gpt.message)
    ask_gpt.run()


def main():
    api_json_path = "instructions/setting.json"
    prompt_file_path = "my_memos/message.txt"
    target_path = "data/examples_240103_shape/examples_240103_shape_annotated"
    name = "annotated_cropped_muffler_before.jpg"

    target_image_path = os.path.join(target_path, name)

    run_gpt4_vision(api_json_path, prompt_file_path, target_image_path)
    # run_gpt4_text(api_json_path, prompt_file_path)


if __name__ == '__main__':
    main()
