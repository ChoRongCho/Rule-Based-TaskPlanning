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
    is_soft: bool = False

    # bin_packing Predicates (max 6)
    in_bin: bool = False
    out_bin: bool = False
    is_bigger_than_bin: bool = False
    on_the_object: object or bool = False
    is_allowed_in_bin: bool = False
    is_not_allowed_in_bin: bool = False

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
        elif bins is True:
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
object1 = Object(
    index=0,
    name='red object',
    location=(71, 277),
    size=(66, 62),
    color='red',
    object_type='object',
    is_fragile=True,
    out_bin=True
)

# Bin
bin1 = Object(
    index=1,
    name='white box',
    location=(506, 192),
    size=(247, 346),
    color='white',
    object_type='box',
    is_soft=True,
    in_bin=True
)

# Object 2
object2 = Object(
    index=2,
    name='black object',
    location=(171, 247),
    size=(135, 137),
    color='black',
    object_type='object',
    is_rigid=True,
    out_bin=True
)

# Object 3
object3 = Object(
    index=3,
    name='blue object',
    location=(490, 233),
    size=(151, 206),
    color='blue',
    object_type='object',
    is_rigid=True,
    in_bin=True
)

# Object 4
object4 = Object(
    index=4,
    name='brown object',
    location=(259, 157),
    size=(124, 153),
    color='brown',
    object_type='object',
    is_soft=True,
    out_bin=True
)

if __name__ == '__main__':
    """
    bin 
    soft but we don't have to consider this predicates.
    
    rules
    rule0: "you should never pick and place a box",
    rule1: "when place a fragile objects, the soft objects must be in the bin",
    rule2: "when fold a object, the object must be foldable",
    rule3: "when push a object, neither fragile and rigid objects are permitted, but only soft objects are permitted",
    rule4: "you must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object"

    objects
    1 fragile objects: object1
    2 rigid objects: object2, object3
    1 soft object: object4
    
    objects in the bin: object3
    objects out the bin: object1, object2, object4

    Available action
    object1: [fragile, out_bin]: pick, place
    object2: [rigid, out_bin]: pick, place
    object3: [rigid, in_bin]: out, place
    object4: [soft, out_bin]: pick, place, push
    """
    # Initialize robot
    robot = Robot()

    # Out and place a rigid object3 based on rule3
    robot.out(object3, bin1)
    robot.place(object3, False)

    # Pick and place soft object4 in the bin
    robot.pick(object4)
    robot.place(object4, bin1)

    # Push soft object4 based on rule4
    robot.push(object4)

    # Pick and place fragile object1 in the bin based on rule1
    robot.pick(object1)
    robot.place(object1, bin1)

    # End the planning
    robot.state_base()
