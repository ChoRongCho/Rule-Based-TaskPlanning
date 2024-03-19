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
    is_foldable: bool = False
    is_soft: bool = False
    is_fragile: bool = False
    is_rigid: bool = False

    # bin_packing Predicates (max 6)
    in_bin: bool = False
    out_bin: bool = False
    is_bigger_than_bin: bool = False
    on_the_object: object or bool = False
    is_folded: bool = False
    is_broken: bool = False


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
        self.is_soft_object_in_bin = False

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
            if obj.is_fragile and not self.is_soft_object_in_bin:
                print(f"Cannot place a {obj.name} without the soft object in the box. ")
            else:
                print(f"Place {obj.name} in {bins.name}")
                self.state_handempty()
                obj.in_bin = True
                obj.out_bin = False
                if obj.is_soft:
                    self.is_soft_object_in_bin = True
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
            obj.is_folded = True

        # bin_packing

    def out(self, obj, bins):
        if not obj.in_bin:
            print(f"Cannot pick a {obj.name} not in the bin.")
        else:
            print(f"Out {obj.name} from {bins.name}")
            self.state_holding(obj)
            obj.in_bin = False
            obj.out_bin = True


# Object 0
bin1 = Object(
    index=0,
    name='white box',
    location=(511, 216),
    size=(232, 324),
    color='white',
    object_type='box',
    is_fragile=True,
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
    is_foldable=True,
    is_rigid=True,
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
    is_soft=True,
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
    is_rigid=True,
    in_bin=True
)

if __name__ == '__main__':
    """
Given init state and goal state of the task
|------------------------------------Init-State------------------------------------|
| item    | name          | in_bin | out_bin | is_soft | is_rigid | is_elastic | is_foldable |
|----------------------------------------------------------------------------------|
| bin1    | white box     | None   | None    | None    | None     | None       | None        |
| object1 | yellow object | False  | True    | False   | False    | True       | False       |
| object2 | blue object   | False  | True    | False   | True     | False      | False       |
| object3 | black object  | True   | False   | True    | False    | False      | True        |
| object4 | brown object  | True   | False   | False   | False    | True       | True        |
|----------------------------------------------------------------------------------|

|---------------------------------Goal-State---------------------------------|
| item    | name          | in_bin | out_bin | foldable_folded | soft_pushed |
|----------------------------------------------------------------------------|
| bin1    | white box     | None   | None    | None            | None        |
| object1 | yellow object | True   | False   | False           | False       |
| object2 | blue object   | True   | False   | False           | False       |
| object3 | black object  | False  | True    | True            | True        |
| object4 | brown object  | True   | False   | True            | False       |
|----------------------------------------------------------------------------|

'rule0': 'you should never pick and place a box', 
'rule1': 'when place a fragile objects, the soft objects must be in the bin', 
'rule2': 'when fold a object, the object must be foldable', 
'rule3': 'when push a object, neither fragile and rigid objects are permitted, but only soft objects are permitted', 
'rule4': 'you must push a soft object to make more space in the bin, however, 
if there is a fragile object on the soft object, you must not push the object'

object1: {out_bin} => {in_bin} : pick and place
object2: {out_bin} => {in_bin} : pick and place
object3: {in_bin} => {out_bin, folded, pushed} : out and place, fold, push
object4: {in_bin} => {in_bin, folded} : fold

1. Out and place object3 that goal state of in_bin=False
2. Fold and push object3
3. pick and place object1
4. pick and place object2
5. Fold object4
"""
    # Initialize robot
    robot = Robot()

    # Step 1: Out and place object3 (soft and foldable and out_bin)
    robot.out(object3, bin1)
    robot.place(object3, bins=False)

    # Step 2: Fold and push object3
    robot.fold(object3)
    robot.push(object3)

    # Step 3: Pick and place object1 (elastic)
    robot.pick(object1)
    robot.place(object1, bin1)

    # Step 4: Pick and place object2 (rigid)
    robot.pick(object2)
    robot.place(object2, bin1)

    # Step 5: Fold object4 (elastic and foldable)
    robot.fold(object4)

    # Robot end
    robot.state_base()
