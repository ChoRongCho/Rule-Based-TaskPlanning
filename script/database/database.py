from dataclasses import dataclass


# Basic Robot class
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
        self.robot_base_pose = True

    def state_handempty(self):
        self.robot_handempty = True

    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects

    def state_base(self):
        self.robot_base_pose = True

    # robot action set
    def pick(self):
        pass

    def place(self):
        pass

    def push(self):
        pass

    def fold(self):
        pass

    def out(self):
        pass

    def pick_up(self):
        pass

    def put_down(self):
        pass

    def stack(self):
        pass

    def unstack(self):
        pass

    def slice(self):
        pass

    def move(self):
        pass


@dataclass
class Objects:
    # Basic dataclass
    index: int
    task: str
    size: tuple
    color: str
    object_type: str


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
