from script.gpt_model.gpt_prompt import GPTInterpreter
from script.visual_interpreting.running_with_dinno import MyDino


def main():
    # name = "hanoi_test2"
    #
    # gpt4 = GPTInterpreter(
    #     api_json="setting.json",
    #     example_prompt_json="test_prompt_vision.json",
    #     result_dir="response/my_vision",
    #     version="vision"
    # )
    #
    # answer = gpt4.run_json_prompt(name)
    # print(answer)

    """text_phrases = [
        "blue disk",
        "green disk",
        "yellow disk",
        "purple disk",
        "orange disk",
        "pink disk",
        "wooden stick",
    ]"""

    text_phrases = [
        "carrot",
        "cucumber",
        "tomato",
        "round cutting board",
        "white bowl",
        "kitchen knife",
    ]

    text_query = "".join([
        phrase + " ."
        for phrase in text_phrases
    ])
    print(text_query)

    answer = text_query
    path = "/home/changmin/PycharmProjects/GPT_examples/data/cooking"
    visual_interpreter = MyDino(
        name="problem3.jpg",
        image_path=path,
        save_path=path
    )
    visual_interpreter.modifying_text_prompt(answer)
    visual_interpreter.run_dinno()


if __name__ == '__main__':
    main()
