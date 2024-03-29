import random
import yaml

# from scripts.pddl_planner import PDDLPlanner
from scripts.python_planner import PythonPlanner
from scripts.utils.utils import parse_args_v2


def main():
    args = parse_args_v2()
    image_number = 8
    exp_number = 6
    args.exp_name = f"20240319_train_problem{image_number}_{exp_number}"
    args.input_image = f"train/problem{image_number}.jpg"
    args.max_predicates = random.randint(1, 6)

    # make plan
    planner = PythonPlanner(args=args)
    planner.plan()
    # planner.feedback()


def main2():
    args = parse_args_v2()
    image_number = 7
    exp_number = 1
    args.exp_name = f"20240314_train_problem{image_number}_{exp_number}"
    args.input_image = f"train/problem{image_number}.jpg"
    args.max_predicates = random.randint(1, 6)

    # make plan
    planner = PythonPlanner(args=args)

    message = """
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
    is_elastic: bool = False
    is_foldable: bool = False
    is_rigid: bool = False
    is_soft: bool = False
    is_fragile: bool = False

    # bin_packing Predicates (max 3)
    in_bin: bool = False
    out_bin: bool = False
    is_bigger_than_bin: bool = False

class Robot:
    # Define skills
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions

        self.robot_handempty = True
        self.robot_now_holding = False
        self.robot_base_pose = True

        # new state for bin_packing
        self.is_soft_in_bin = False

    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False

    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False

    # basic state
    def state_base(self):
        self.robot_base_pose = True

    # bin_packing
    def pick(self, obj):
        if obj.in_bin or obj.object_type == 'box':
            print(f"Cannot pick a {obj.name} in the bin or a box.")
        else:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_bin = True
            obj.in_bin = False

    # bin_packing
    def place(self, obj, bins):
        if self.robot_now_holding != obj or obj.object_type == 'box':
            print(f"Cannot place a {obj.name} not in hand or a box.")
        elif bins:
            # place an object in the bin
            if obj.is_fragile and not self.is_soft_in_bin:
                print(f"Cannot place a {obj.name} without the soft object in the box. ")
            else:
                print(f"Place {obj.name} in {bins.name}")
                self.state_handempty()
                obj.in_bin = True
                obj.out_bin = False
                if obj.is_soft:
                    self.is_soft_in_bin = True
        else:
            # place an object out of the bin
            print(f"Place {obj.name} out of the box")
            self.state_handempty()
            obj.in_bin = False
            obj.out_bin = True

    # bin_packing
    def push(self, obj):
        if not self.robot_handempty or obj.is_fragile or obj.is_rigid:
            print(f"Cannot push a {obj.name} when hand is not empty or the object is fragile or rigid.")
        elif obj.is_soft and obj.in_bin:
            print(f"Push {obj.name}")

    # bin_packing
    def fold(self, obj):
        if not self.robot_handempty or not obj.is_foldable:
            print(f"Cannot fold a {obj.name} when hand is not empty or the object is not foldable.")
        else:
            print(f"Fold {obj.name}")

    # bin_packing
    def out(self, obj, bins):
        if not obj.in_bin:
            print(f"Cannot pick a {obj.name} not in the bin.")
        else:
            print(f"Out {obj.name} from {bins.name}")
            self.state_holding(obj)
            obj.in_bin = False
            obj.out_bin = True

# Object 1
object1 = Object(
    index=0,
    name='yellow object',
    location=(89, 136),
    size=(156, 154),
    color='yellow',
    object_type='object',
    is_rigid=True,
    out_bin=True
)

# Object 2
object2 = Object(
    index=1,
    name='blue object',
    location=(203, 278),
    size=(156, 150),
    color='blue',
    object_type='object',
    is_elastic=True,
    is_soft=True,
    out_bin=True
)

# Bin
bin1 = Object(
    index=2,
    name='white box',
    location=(498, 218),
    size=(249, 353),
    color='white',
    object_type='box',
    is_rigid=True,
    is_foldable=True,
    in_bin=True
)

# Object 3
object3 = Object(
    index=3,
    name='black object',
    location=(294, 150),
    size=(147, 123),
    color='black',
    object_type='object',
    is_elastic=True,
    out_bin=True
)

if __name__ == '__main__':
	# packing all object in the box
	# make a plan
Your goal is packing objects into the bin. 
You must follow the rule: 

{'pick': 'pick an {object} not in the {bin}',
'place': 'place an {object} on the {anywhere}',
'push': 'push an {object} downward in the bin, hand must be empty when pushing',
'fold': 'fold an {object}, hand must be empty when folding',
'out': 'pick an {object} in {bin}'}

{'rule0': 'you should never pick and place a box', 
'rule1': 'when place a fragile objects, the soft objects must be in the bin', 
'rule2': 'when fold a object, the object must be foldable', 
'rule3': 'when push a object, neither fragile and rigid objects are permitted, but only soft objects are permitted', 
'rule4': 'you must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object'}

Make a plan under the if __name__ == '__main__':. 
make init state to goal state using actions
|-------------------------------------Init-State-----------------------------------|
| item    | name             | in_bin | out_bin | is_soft |  is_rigid | is_elastic |
|----------------------------------------------------------------------------------|
| object1 | yellow object    | False  | True    | False   |  True     | False      |
| object2 | blue object      | False  | True    | True    |  False    | True       |
| bin1    | white box        | None   | None    | None    |  None     | None       |
| object3 | black object     | False  | True    | False   |  False    | True       |
|----------------------------------------------------------------------------------|

|------------------------Goal-State------------------------|
| item    | name          | in_bin | out_bin | soft_pushed |
|----------------------------------------------------------|
| object1 | yellow object | True   | False   | False       |
| bin1    | white box     | None   | None    | None        |
| object2 | blue object   | True   | False   | True        |
| object3 | black object  | False  | True    | False       |
|----------------------------------------------------------|
"""
    planner.append_chat(message=message, is_reset=True)
    answer = planner.run_chat()
    print(answer)


if __name__ == '__main__':
    main()
