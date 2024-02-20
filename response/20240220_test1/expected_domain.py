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
    is_foldable: bool=False
    is_elastic: bool=False

    # bin_packing Predicates (max 3)
    in_bin: bool=False
    out_bin: bool=False
    is_bigger_than_bin: bool=False


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
        if obj.in_bin:
            print("Cannot pick an object in the bin.")
        else:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_bin = True
            obj.in_bin = False

    # bin_packing
    def place(self, obj, bins):
        if self.robot_now_holding != obj:
            print("Cannot place an object not in hand.")
        elif obj.is_fragile and not any(o.is_soft and o.in_bin for o in bins.objects):
            print("Cannot place a fragile object without a soft object in the bin.")
        else:
            print(f"Place {obj.name} in {bins.name}")
            self.state_handempty()
            obj.in_bin = True
            obj.out_bin = False

    # bin_packing
    def push(self, obj):
        if not self.robot_handempty:
            print("Cannot push an object when hand is not empty.")
        elif obj.is_fragile or obj.is_rigid:
            print("Cannot push a fragile or rigid object.")
        else:
            print(f"Push {obj.name}")
            obj.in_bin = True
            obj.out_bin = False

    # bin_packing
    def fold(self, obj):
        if not self.robot_handempty:
            print("Cannot fold an object when hand is not empty.")
        elif not obj.is_foldable:
            print("Cannot fold a non-foldable object.")
        else:
            print(f"Fold {obj.name}")
            obj.in_bin = True
            obj.out_bin = False

    def out(self, obj, bins):
        if not obj.in_bin:
            print("Cannot pick an object not in the bin.")
        else:
            print(f"Out {obj.name} from {bins.name}")
            self.state_holding(obj)
            obj.in_bin = False
            obj.out_bin = True


# Object 1
object1 = Object(
    index=0,
    name='white box',
    location=(509, 210),
    size=(231, 323),
    color='white',
    object_type='box',
    is_elastic=True,
    in_bin=True
)

# Object 2
object2 = Object(
    index=1,
    name='blue object',
    location=(204, 220),
    size=(361, 247),
    color='blue',
    object_type='object',
    is_elastic=True,
    out_bin=True
)

# Object 3
object3 = Object(
    index=2,
    name='yellow object',
    location=(83, 158),
    size=(135, 216),
    color='yellow',
    object_type='object',
    is_foldable=True,
    out_bin=True
)

# Object 4
object4 = Object(
    index=3,
    name='brown object',
    location=(257, 95),
    size=(139, 148),
    color='brown',
    object_type='object',
    out_bin=True
)


if __name__ == '__main__':
    # packing all object in the box
    # make a plan
    pass
