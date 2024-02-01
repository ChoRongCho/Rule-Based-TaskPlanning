from dataclasses import dataclass


class Robot:
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions

        self.robot_handempty = True
        self.robot_now_holding = False

    def handempty(self):
        self.robot_handempty = True

    def holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects


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


@dataclass
class Task:
    name: str


@dataclass
class Domain:
    types: dict
    requirements: str
    predicates: str
    actions: dict


@dataclass
class Problem:
    objects: dict
    init_state: dict
    goal_state: dict


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

    def robot_pick(object, bin):
        pass

    def robot_place(object, bin):
        pass

    def robot_push(object):
        pass

    def robot_fold(object):
        pass

    def robot_out(object, bin):
        pass

    """
    rule
    1. when pick the object, the robot.handempty is True.
    2. when place the object, the robot.handempty is False.
    3. when push the object, the object.is_fragile is False, object.is_deformable and robot.handempty is True
    4. when place the object.is_fragile, after object.is_deformable is placed.
    5. when out the object, the robot.handempty is True
    
    Fill the robot_action function using rule conditions
    """
