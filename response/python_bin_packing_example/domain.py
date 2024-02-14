from dataclasses import dataclass
from script.robot_action_set import Robot


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
    is_flexible: bool = False
    is_rigid: bool = False
    is_fragile: bool = False
    is_soft: bool = False
    out_bin: bool = True
    in_bin: bool = False


class Domain(Robot):
    def __init__(self):
        super().__init__(name="Robot_name",
                         goal="goal of the task",
                         actions={"pick": "description1",
                                  "place": "description1",
                                  "push": "",
                                  "fold": "",
                                  "out": ""
                                  })
        # task
        self.task = "task_name"

        # cautions
        self.cautions = """
        1. place a fragile object on top of a soft object to prevent breaking the fragile object.
        2. fold a flexible object to make it compact to secure spaces for other objects.
        3. don't press a rigid object. Press deformable objects.
        """

    # Robot action re-define
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



#
# class Domain(Robot):
#     def __init__(self):
#         super().__init__(name="Robot_name",
#                          goal="goal of the task",
#                          actions={"pick": "description1",
#                                   "place": "description1",
#                                   "push": "",
#                                   "fold": "",
#                                   "out": ""
#                                   })
#         # task
#         self.task = "task_name"
#
#         # cautions
#         self.cautions = """
#         1. place a fragile object on top of a soft object to prevent breaking the fragile object.
#         2. fold a flexible object to make it compact to secure spaces for other objects.
#         3. don't press a rigid object. Press deformable objects.
#         """
#
#     def pick(self, obj):
#         # Preconditions
#         if self.robot_handempty and obj.in_bin:
#             # Update state transitions
#             self.state_holding(obj)
#             # Update object predicates
#             obj.in_bin = False
#             obj.out_bin = True
#             print(f"{self.name} picks up {obj.name}")
#
#     def place(self, obj, bins):
#         # Preconditions
#         if not self.robot_handempty and obj.out_bin and bins.in_bin:
#             # Update state transitions
#             self.state_handempty()
#             # Update object predicates
#             obj.in_bin = True
#             obj.out_bin = False
#             print(f"{self.name} places {obj.name} in {bins.name}")
#
#     def push(self, obj):
#         # Preconditions
#         if not self.robot_handempty and obj.in_bin:
#             # Update object predicates
#             obj.location = (obj.location[0] + 10, obj.location[1])
#             print(f"{self.name} pushes {obj.name}")
#
#     def fold(self, obj):
#         # Preconditions
#         if not self.robot_handempty and obj.is_flexible:
#             # Update object predicates
#             obj.size = (obj.size[0] // 2, obj.size[1])
#             print(f"{self.name} folds {obj.name}")
#
#     def out(self, obj, bins):
#         # Preconditions
#         if not self.robot_handempty and obj.in_bin and bins.out_bin:
#             # Update state transitions
#             self.state_handempty()
#             # Update object predicates
#             obj.in_bin = False
#             obj.out_bin = True
#             print(f"{self.name} takes {obj.name} out of {bins.name}")

