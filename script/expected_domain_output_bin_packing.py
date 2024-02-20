"""
The definition for domain input
1. task name: bin_packing
2. robot action, state: available action: give the constraint and pre-condition and effect
3. object list, state: from LLMs and images, get predicates
4. predicates:

"""
from dataclasses import dataclass
from robot_action_set import Robot


@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    location: tuple
    size: tuple
    color: str or bool
    object_type: str

    # bin_packing predicates
    on_item: bool
    left_item: bool
    right_item: bool
    top_item: bool
    bottom_item: bool
    is_flexible: bool
    is_rigid: bool
    is_fragile: bool
    is_soft: bool
    out_bin: bool
    in_bin: bool


class Domain(Robot):
    def __init__(self):
        super().__init__(name="Robot_name",
                         goal="goal of the task",
                         actions={"action1": "description1", "action2": "description1"})
        # task
        self.task = "task_name"

        # list of the object
        # ... Modifying Object
        obj1 = Object(index=0, name="", location=(0, 0), size=(0, 0), color=None, object_type="object")
        obj2 = Object(index=1, name="", location=(0, 0), size=(0, 0), color=None, object_type="box")
        self.object_list = [obj1, obj2]

        # cautions
        self.cautions = """
        Summarize the given cautions in the multi-line annotation
        """

    # Robot action re-definition
    def main(self):
        obj1, obj2 = self.object_list

        self.pick(obj=obj1)
        self.place(obj=obj1, bins=obj2)
        self.state_base()
