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
    is_elastic: bool = False
    is_soft: bool = False
    is_rigid: bool = False
    is_foldable: bool = False

    # bin_packing Predicates (max 6)
    in_bin: bool = False
    out_bin: bool = False
    is_bigger_than_bin: bool = False
    on_the_object: object or bool = False
    is_folded: bool = False
    is_black: bool = False


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

    def dummy(self):
        pass


# Object 1
bin1 = Object(
    index=0,
    name='white box',
    location=(516, 201),
    size=(238, 334),
    color='white',
    object_type='box',
    is_elastic=True,
    is_rigid=True,
    in_bin=True
)

# Object 2
object2 = Object(
    index=1,
    name='yellow object',
    location=(280, 134),
    size=(227, 221),
    color='yellow',
    object_type='object',
    is_foldable=True,
    out_bin=True
)

# Object 3
object3 = Object(
    index=2,
    name='black object',
    location=(79, 275),
    size=(151, 113),
    color='black',
    object_type='object',
    is_rigid=True,
    out_bin=True,
    is_black=True
)

# Object 4
object4 = Object(
    index=3,
    name='brown object',
    location=(503, 205),
    size=(147, 153),
    color='brown',
    object_type='object',
    is_rigid=True,
    is_elastic=True,
    in_bin=True
)

# Object 5
object5 = Object(
    index=4,
    name='blue object',
    location=(223, 209),
    size=(355, 244),
    color='blue',
    object_type='object',
    is_soft=True,
    out_bin=True
)

if __name__ == '__main__':
    """
    bin 
    elastic and rigid but we don't have to consider this predicates.
    
    rules
    rule0: "you should never pick and place a box",
    rule1: "when place a fragile objects, the soft objects must be in the bin",
    rule2: "when fold a object, the object must be foldable",
    rule3: "when push a object, neither fragile and rigid objects are permitted, but only soft objects are permitted",
    rule4: "you must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object"

    objects
    1 foldable objects: object2
    1 soft object: object5
    2 rigid objects: object3, object4
    1 elastic object: object4
    
    objects in the bin: object4
    objects out the bin: object2, object3, object5

    Available action
    object2: [foldable, out_bin]: pick, place, fold
    object3: [rigid, out_bin]: pick, place
    object4: [rigid, elastic, in_bin]: out, place
    object5: [soft, out_bin]: pick, place, push
    """
    # Initialize robot
    robot = Robot()

    # Out and place a rigid object4 based on rule3
    robot.out(object4, bin1)
    robot.place(object4, False)
    robot.pick(object4)
    robot.place(object4, bin1)

    # Fold, pick and place an foldable object2 in the bin based on rule2
    robot.fold(object2)
    robot.pick(object2)
    robot.place(object2, bin1)

    # Pick and place a soft object5 in the bin based on rule1
    robot.pick(object5)
    robot.place(object5, bin1)

    # Push a soft object5 in the bin based on rule4
    robot.push(object5)

    # End the planning
    robot.state_base()
