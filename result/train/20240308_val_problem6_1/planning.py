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
    is_rigid: bool = False
    is_elastic: bool = False

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
            if obj.is_rigid and not self.is_soft_in_bin:
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
        if not self.robot_handempty or obj.is_rigid:
            print(f"Cannot push a {obj.name} when hand is not empty or the object is rigid or fragile.")
        elif obj.is_soft:
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


# Object 1
bin1 = Object(
    index=0,
    name='white box',
    location=(509, 210),
    size=(231, 323),
    color='white',
    object_type='box',
    is_rigid=True,
    is_foldable=True,
    in_bin=True
)

# Object 1
object1 = Object(
    index=1,
    name='blue object',
    location=(204, 220),
    size=(361, 247),
    color='blue',
    object_type='object',
    is_rigid=True,
    out_bin=True
)

# Object 2
object2 = Object(
    index=2,
    name='yellow object',
    location=(83, 158),
    size=(135, 216),
    color='yellow',
    object_type='object',
    is_soft=True,
    is_elastic=True,
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
    is_rigid=True,
    is_elastic=True,
    out_bin=True
)

if __name__ == '__main__':
    """
    bin 
    rigid and foldable but we don't have to consider this predicates.
    
    rules
    rule0: "you should never pick and place a box",
    rule1: "when place a fragile objects, the soft objects must be in the bin",
    rule2: "when fold a object, the object must be foldable",
    rule3: "when push a object, neither fragile and rigid objects are permitted, but only soft objects are permitted",
    rule4: "you must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object"

    objects
    1 foldable objects: object2
    2 rigid objects: object1, object4
    1 soft object: object2
    
    objects in the bin: 
    objects out the bin: object1, object2, object4

    Available action
    object1: [rigid, out_bin]: pick, place
    object2: [soft, elastic, out_bin]: pick, place, push, fold
    object4: [rigid, elastic, out_bin]: pick, place
    """
    # Initialize robot
    robot = Robot()

    # Push, pick and place an elastic object2 based on rule4
    robot.push(object2)
    robot.pick(object2)
    robot.place(object2, bin1)

    # Pick and place object1 in the bin based on the rule1
    robot.pick(object1)
    robot.place(object1, bin1)

    # Pick and place object4 in the bin
    robot.pick(object4)
    robot.place(object4, bin1)

    # End the planning
    robot.state_base()
