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
    is_rigid: bool = False
    is_fragile: bool = False
    is_elastic: bool = False
    is_foldable: bool = False

    # bin_packing Predicates (max 2)
    in_bin: bool = False
    out_bin: bool = False

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
                if obj.is_elastic:
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
        elif obj.is_elastic:
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

    def dummy(self):
        pass


# Object 0
bin1 = Object(
    index=0,
    name='white box',
    location=(511, 216),
    size=(232, 324),
    color='white',
    object_type='box',
    is_rigid=True,
    is_foldable=True,
    in_bin=True
)

# Object 1
object1 = Object(
    index=1,
    name='yellow object',
    location=(82, 153),
    size=(138, 218),
    color='yellow',
    object_type='object',
    is_fragile=True,
    out_bin=True
)

# Object 2
object2 = Object(
    index=2,
    name='blue object',
    location=(203, 216),
    size=(366, 247),
    color='blue',
    object_type='object',
    is_fragile=True,
    out_bin=True
)

# Object 3
object3 = Object(
    index=3,
    name='black object',
    location=(496, 276),
    size=(142, 118),
    color='black',
    object_type='object',
    is_foldable=True,
    is_elastic=True,
    in_bin=True
)

# Object 4
object4 = Object(
    index=4,
    name='brown object',
    location=(502, 168),
    size=(152, 128),
    color='brown',
    object_type='object',
    is_elastic=True,
    in_bin=True
)

if __name__ == '__main__':
    """
Given init state and goal state of the task
|------------------------------------Init-State------------------------------------|
| item    | name          | in_bin | out_bin | is_rigid | is_foldable | is_fragile | is_elastic |
|----------------------------------------------------------------------------------|
| bin1    | white box     | None   | None    | None     | None        | None       | None       |
| object1 | yellow object | False  | True    | False    | False       | True       | False      |
| object2 | blue object   | False  | True    | False    | False       | True       | False      |
| object3 | black object  | True   | False   | False    | True        | False      | True       |
| object4 | brown object  | True   | False   | False    | False       | False      | True       |
|----------------------------------------------------------------------------------|

|---------------------------------Goal-State---------------------------------|
| item    | name          | in_bin | out_bin | is_rigid | is_foldable | is_fragile | is_elastic |
|----------------------------------------------------------------------------------|
| bin1    | white box     | None   | None    | None     | None        | None       | None       |
| object1 | yellow object | True   | False   | False    | False       | True       | False      |
| object2 | blue object   | True   | False   | False    | False       | True       | False      |
| object3 | black object  | False  | True    | False    | True        | False      | True       |
| object4 | brown object  | True   | False   | False    | False       | False      | True       |
|----------------------------------------------------------------------------------|

'rule0': 'you should never pick and place a box', 
'rule1': 'when place a fragile objects, the soft objects must be in the bin', 
'rule2': 'when fold a object, the object must be foldable', 
'rule3': 'when push a object, neither fragile and rigid objects are permitted, but only soft objects are permitted', 
'rule4': 'you must push a soft object to make more space in the bin, however, 
if there is a fragile object on the soft object, you must not push the object'

object1: {out_bin} => {in_bin} : pick and place
object2: {out_bin} => {in_bin} : pick and place
object3: {in_bin} => {out_bin} : out and place
object4: {in_bin} => {in_bin} : 

1. Out object3 that goal state of in_bin=False
2. pick and place object1
3. pick and place object2
"""
    # Initialize robot
    robot = Robot()

    # Step 1: Out and place object3 (elastic and out_bin)
    robot.out(object3, bin1)
    robot.place(object3, bins=False)

    # Step 2: Pick and place object1 (fragile)
    robot.pick(object1)
    robot.place(object1, bin1)

    # Step 3: Pick and place object2 (fragile)
    robot.pick(object2)
    robot.place(object2, bin1)

    # Robot end
    robot.state_base()
