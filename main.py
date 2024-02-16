import json

from script.gpt_model.gpt_prompt import GPTInterpreter
from script.gpt_model.pddl_generator import PDDL
from script.utils.make_exp import CreateExperiment
from script.utils.utils import parse_args, seed_all_types, DomainPredicate


def main_types():
    exp_name = "robot_action_test"
    api_json = "setting.json"
    prompt_json = False
    result_dir = "response/" + exp_name

    gpt4 = GPTInterpreter(api_json=api_json,
                          example_prompt_json=prompt_json,
                          result_dir=result_dir,
                          version="vision")

    # examples
    with open("prompt_examples.json", "r") as file:
        exp = json.load(file)
        object_message0 = exp["object_observation_message"]
        object_message1 = exp["object_type_message"]

    images = ["/home/changmin/PycharmProjects/GPT_examples/data/cooking/problem1.jpg"]
    gpt4.add_message_manual(role="user", content=object_message0[0]["content"], image_url=images)
    gpt4.add_message_manual(role="assistant", content=object_message0[1]["content"], image_url=False)

    images = ["/home/changmin/PycharmProjects/GPT_examples/data/blocksworld/problem1.jpg"]
    gpt4.add_message_manual(role="user", content=object_message0[2]["content"], image_url=images)
    gpt4.add_message_manual(role="assistant", content=object_message0[3]["content"], image_url=False)

    prompt = f"We are going to do a hanoi task which is stacking disks in order from the big ones. \n" + \
             "These are the observations where I'm going to work. \n"
    prompt += "What objects or tools are here? Don't include a robot. \n"
    images = ["/home/changmin/PycharmProjects/GPT_examples/data/hanoi/problem1.jpg"]

    gpt4.add_message_manual(role="user", content=prompt, image_url=images)
    answer = gpt4.run_manual_prompt(name="", is_save=False)

    print("\n\n")
    print("-" * 50)

    # gpt4.reset_message()
    # gpt4.message = object_message1
    #
    # prompt = f"We are going to do a cooking task which is cooking foods using given ingredients. \n" + \
    #          f"In our case, we are only doing slice. \n" + \
    #          "\nThese are the observations where I'm going to work. \n"
    # prompt += "What objects or tools are here? \n"
    # images = ["/home/changmin/PycharmProjects/GPT_examples/data/cooking/problem1.jpg"]
    # gpt4.add_message_manual(role="user", content=prompt, image_url=images)
    # gpt4.add_message_manual(role="assistant", content=answer, image_url=False)
    #
    # prompt = "Divide the character of the object according to the task. \n"
    # gpt4.add_message_manual(role="user", content=prompt, image_url=False)
    #
    # print("\n\n")
    # print("-"*50)
    # answer = gpt4.run_manual_prompt(name="", is_save=False)

    # new_answer = "1. Location: plate, chopping board. \n2. Ingredients: carrot, meat, garlic. \n3. Tool: knife. \n"


def main0():
    exp_name = "20240216_get_domain"
    api_json = "setting.json"
    prompt_json = "prompt_examples.json"
    result_dir = "response/" + exp_name
    name = "test6_with_examples"

    task = "hanoi"
    task_description = "stacking disks in order from the big ones. \n"
    max_predicates = 3

    gpt4 = GPTInterpreter(api_json=api_json,
                          example_prompt_json=prompt_json,
                          result_dir=result_dir,
                          version="pddl")
    gpt4.add_example_prompt("domain_message")
    content = f"""
    We are now going to do a {task} task whose goal is {task_description}""" + """
There are many objects in this domain, this is object information that comes from image observation. \n
1. {'Disk': ['yellow object', 'black object ', 'red object', 'blue object'], 'Peg': ['left peg', 'right peg', 'middle peg']} 
This is an example of python dataclass code 
    """ + f"""
from dataclasses import dataclass


@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    location: tuple
    size: tuple
    color: str or bool
    object_type: str
    
    # Object physical properties predicates
    
    # {task} Predicates (max {max_predicates})
    

However, we cannot do complete planning with this dataclass predicate alone that means we have to add another predicates that fully describe the {task}. 
We don't have to consider physical properties of the object.
Add more predicates needed for {task} to class Object. 
            """

    gpt4.add_message_manual(role="user", content=content)
    gpt4.run_manual_prompt(name=name, is_save=True)


def main():
    exp_name = "domain_test"

    api_json = "setting.json"
    prompt_json = "my_personal.json"
    result_dir = "response/" + exp_name

    gpt4 = GPTInterpreter(api_json=api_json,
                          example_prompt_json=prompt_json,
                          result_dir=result_dir,
                          version="vision")

    content1 = "We are now going to do cooking which is cooking foods using given ingredients. " + \
               "In our case, we are only doing slicing. \nWhen slicing, we only do them on the chopping board. \n"
    # content1 += "We want to "
    content1 += "There are many objects in interest such as tomato, bowl, chopping_board and knife. \n"
    content1 += "Additionally, there are types of the objects such as" + \
                " ingredient-[tomato], location-[bowl], tool-[knife, chopping_board]. \n"
    content1 += "We have to define the physical or semantic relationships and state between " + \
                "the types of the objects which is called predicates. \n"
    content1 += "We must use the types [ingredient, location, tool] as parameters when defining predicates. \n"
    content1 += "First, describe the physical relationship between objects. \n"
    content1 += "Second, describe the physical or semantic state of the objects itself. \n"
    content1 += "Make appropriate predicates up to 8 that fully describe the domain using given rules.\n"

    content1_answer = "What we are doing is cooking foods using given ingredients. \n"
    content1_answer += "We are now doing slicing. And there are some rules. \n"
    content1_answer += "We are cutting the ingredients on the chopping board. So we have to know " + \
                       "the state of the ingredients whether sliced or not. \n"

    # content2 = "We are now going to do cooking which is cooking foods using given ingredients. "\
    #            "In our case, we are only doing slicing. \nWhen slicing, we only do them on the chopping board. "
    # content2 += "There are many objects in interest such as a plate, carrot, knife, meat, garlic and hopping board. \n"
    # content2 += "Divide the type of the objects according to the task. \n"
    # content2_answer = "1. Location: plate, chopping board. \n2. Ingredients: carrot, meat, garlic. \n3. Tool: knife. \n"
    #
    # content3 = "We are now going to do blocksworld which is stacking blocks. \n"
    # content3 += "There are many objects in interest such as a block1, block2, block3, block4 and table. \n"
    # content3 += "Divide the type of the objects according to the task. \n"
    # content3_answer = "1. Blocks: block1, block2, block3, block4.\n2. Base: table. \n"

    gpt4.add_message_manual(role="user", content=content1,
                            image_url="/home/changmin/PycharmProjects/GPT_examples/data/cooking/annotated_problem3.jpg")
    # gpt4.add_text_message_manual(role="assistant", content=content1_answer)

    # gpt4.add_text_message_manual(role="user", content=content3)
    # gpt4.add_text_message_manual(role="assistant", content=content3_answer)
    #
    # gpt4.add_text_message_manual(role="user", content=content2)
    # gpt4.add_text_message_manual(role="assistant", content=content2_answer)

    gpt4.run_manual_prompt(name="domain_predicate_0", is_save=True)


def main1():
    args = parse_args()
    domain = DomainPredicate(args.task)
    predicates = domain.return_predicate()

    seed_all_types(args.seed)
    pddl_gen = PDDL(args=args, predicates=predicates)
    pddl_gen.print_args()
    pddl_gen.run()


def main2():
    exp = CreateExperiment("test3", "bin_packing")
    exp.start_exp()


def main3():
    data_path = "prompt_examples.json"
    with open(data_path, "r") as file:
        data = json.load(file)
        message = data["domain_type_message"]
        message1 = data["domain_action_message"]
        message2 = data["domain_predicate_message"]
        file.close()

    exp_name = "domain_test"

    api_json = "setting.json"
    prompt_json = "my_personal.json"
    result_dir = "response/" + exp_name

    gpt4 = GPTInterpreter(api_json=api_json,
                          example_prompt_json=prompt_json,
                          result_dir=result_dir,
                          version="pddl")
    gpt4.message = message2

    content = "We are now going to do hanoi which is stacking disks in order from the big ones. \n"
    content += "There are many objects in interest such as blue_disk, red_disk, green_disk, orange_disk, black_disk, " \
               "wooden_peg1, wooden_peg2 and wooden_peg3. \n"
    content += "Divide the character of the object according to the task. \n"
    gpt4.add_message_manual(role="user", content=content)
    gpt4.run_manual_prompt(name="domain_predicate_0", is_save=True)


def read_python_code():
    file = "data/prompt_example_python_code_2.py"
    with open(file, "r") as f:
        content = f.read()
        f.close()

    file = "data/prompt_example_python_code3.py"
    with open(file, "r") as f:
        content3 = f.read()
        f.close()

    exp_name = "robot_action_test"
    api_json = "setting.json"
    prompt_json = "my_personal.json"
    result_dir = "response/" + exp_name

    gpt4 = GPTInterpreter(api_json=api_json,
                          example_prompt_json=prompt_json,
                          result_dir=result_dir,
                          version="pddl")

    gpt4.add_message_manual(role="user", content=content)

    content2 = "\n\n This is a example robot state code. However, here are some predicates to be added such as. is_rigid. \n"
    content2 += "Add is_rigid predicates to class Object"
    gpt4.add_message_manual(role="user", content=content2)
    gpt4.add_message_manual(role="assistant", content=content3)

    gpt4.add_message_manual(role="user", content=content)
    content2 = "\n\n This is a example robot state code. How ever, here are some predicates to add. is_flexible, is_deformable, is_fragile, and is_foldable. \n"
    content2 += "Add these predicates to class Object"
    gpt4.add_message_manual(role="user", content=content2)

    gpt4.run_manual_prompt(name="robot_action_1", is_save=True)


if __name__ == '__main__':
    main0()
