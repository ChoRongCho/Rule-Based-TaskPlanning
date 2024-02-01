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

    is_rigid: bool = True


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

    # basic state
    def handempty(self):
        self.robot_handempty = True

    def holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects

    # robot skills
    def pick(self, x):
        # x target
        pass

    def place(self, x):
        pass

    def push(self, x):
        pass

    def out(self, x):
        pass

    def fold(self, x):
        pass

