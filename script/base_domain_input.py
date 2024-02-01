"""
The definition for domain input
1. task name
2. robot action, state: available action: give the constraint and pre-condition and effect
3. object list, state: from LLMs and images, get predicates
4. predicates:

"""
from dataclasses import dataclass
from robot_action_set import Robot


@dataclass
class Object:
    # Basic dataclass
    index: int  # index of the object
    name: str  # name of the object
    location: tuple  # (start x, start y) of the bound box of the object
    size: tuple  # (height, width) of the bound box of the object
    color: str or bool  # color of the object.
    object_type: str  # the type of the objects for action parameters

    # Add new object predicates


class Domain(Robot):
    def __init__(self):
        super().__init__(name="Robot_name",
                         goal="goal of the task",
                         actions={"action1": "description1", "action2": "description1"})
        # task
        self.task = "task_name"

        # list of the object
        # ... Modifying Object
        obj1 = Object(index=0, name="", location=(0, 0), size=(0, 0), color=None, object_type="")
        obj2 = Object(index=1, name="", location=(0, 0), size=(0, 0), color=None, object_type="")
        self.object_list = [obj1, obj2]

        # cautions
        self.cautions = """
        Summarize the given cautions in the multi-line annotation
        """

    # Robot action re-definition
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

