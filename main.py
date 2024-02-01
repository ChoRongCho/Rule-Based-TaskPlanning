import json
import time
import os
from script.gpt_model.pddl_generator import PDDL
from script.gpt_model.gpt_prompt import GPTInterpreter
from script.utils.utils import parse_args, seed_all_types, DomainPredicate
from script.utils.make_exp import CreateExperiment


def main0():
    exp_name = "robot_action_test"
    api_json = "setting.json"
    prompt_json = "my_personal.json"
    result_dir = "response/" + exp_name

    gpt4 = GPTInterpreter(api_json=api_json,
                          prompt_json=prompt_json,
                          result_dir=result_dir,
                          version="pddl")

    content = """from dataclasses import dataclass
            

            @dataclass
            class Objects:
                # Basic dataclass
                index: int
                name: str
                location: tuple
                color: str or bool
                object_type: str


            @dataclass
            class BinPackingObject:
                # Basic dataclass
                index: int
                name: str
                location: tuple
                color: str or bool
                object_type: str

                is_foldable: bool = False
                is_flexible: bool = False
                is_deformable: bool = False
                is_fragile: bool = False

            def main():
                # Given task and object list from image understanding
                task = "bin_packing"

                obj1 = BinPackingObject(index=1, name="obj1", location=(10, 20), color="red", object_type="object")
                obj2 = BinPackingObject(index=2, name="obj2", location=(15, 30), color="blue", object_type="object",
                                        is_deformable=True)
                obj3 = BinPackingObject(index=3, name="obj3", location=(0, 10), color="red", object_type="object",
                                        is_fragile=True)
                obj4 = BinPackingObject(index=4, name="obj4", location=(30, 40), color="green", object_type="object",
                                        is_foldable=True)
                box = BinPackingObject(index=0, name="box", location=(20, 50), color=None, object_type="bin")
                objects_list = [obj1, obj2, obj3, obj4, box]

                # robot skill
                robot = Robot(
                    name="UR5",
                    goal="packing all object in the bin",
                    actions={
                        "pick": "pick {object} not in {bin}",
                        "place": "place {object} in hand on {bin}",
                        "push": "push {object} downward",
                        "fold": "fold {object}",
                        "out": "pick {object} in {bin}"
                    }
                )
                
                # for example, when command robot.place comes,
                # robot.place(object, bin) => The robot actually place the holding {object} in {bin}
                # But we have to define preconditions and effect of the robot action like pddl script.
                 
                # rule
                # 0. if object.location == bin.location => the object is in {bin}
                # 1. when pick the object, the robot.handempty is True.
                # 2. when place the object, the robot.handempty is False.
                # 3. when push the object, the object.is_fragile is False, object.is_deformable and robot.handempty is True and {object} in {bin}
                # 4. when place the object.is_fragile, after object.is_deformable is placed.
                # 5. when out the object, the robot.handempty is True
                
                Fill the                 
                "
                def robot_pick():
                    pass
                def robot_place():
                    pass
                def robot_push():
                    pass
                def robot_fold():
                    pass
                def robot_out():
                    pass "
                function using rule conditions and planning the actions to pack all objects_list in bin 
            """
    content_answer = """
        def robot_pick(object, bin):
            if self.robot.handempty and object.location != bin.location:
                self.robot.pick(object)
                self.robot.handempty(False) 
                self.robot.holding(object)
        
        def robot_place(object1, object2, bin):
            if not self.robot.handempty and robot.holding(object1)
    """
    
    gpt4.add_message_manual(role="user", content=content)
    gpt4.run_manual_prompt(name="robot_action_0", is_save=True)


def main():
    exp_name = "domain_test"

    api_json = "setting.json"
    prompt_json = "my_personal.json"
    result_dir = "response/" + exp_name

    gpt4 = GPTInterpreter(api_json=api_json,
                          prompt_json=prompt_json,
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
    data_path = "data/prompt_examples.json"
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
                          prompt_json=prompt_json,
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
                          prompt_json=prompt_json,
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
    read_python_code()
