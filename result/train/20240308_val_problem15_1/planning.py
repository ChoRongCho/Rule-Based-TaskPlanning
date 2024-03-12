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
    is_foldable: bool = False
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
            print(f"Place {obj.name} in {bins.name}")
            self.state_handempty()
            obj.in_bin = True
            obj.out_bin = False
        else:
            # place an object out of the bin
            print(f"Place {obj.name} out of the box")
            self.state_handempty()
            obj.in_bin = False
            obj.out_bin = True

    # bin_packing
    def push(self, obj):
        if not self.robot_handempty or obj.is_rigid:
            print(f"Cannot push a {obj.name} when hand is not empty or the object is rigid.")
        elif obj.is_elastic:
            print(f"Push {obj.name}")
        else:
            print(f"Cannot push {obj.name} because it is not elastic.")    

    # bin_packing
    def fold(self, obj):
        if not self.robot_handempty or not obj.is_foldable:
            print(f"Cannot fold a {obj.name} when hand is not empty or the object is not foldable.")
        else:
            print(f"Fold {obj.name}")

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
    location=(488, 224),
    size=(281, 400),
    color='white',
    object_type='box',
    is_rigid=True,
    in_bin=True
)

# Object 2
object1 = Object(
    index=1,
    name='black object',
    location=(102, 288),
    size=(159, 160),
    color='black',
    object_type='object',
    is_foldable=True,
    out_bin=True
)

# Object 3
object2 = Object(
    index=2,
    name='brown object',
    location=(202, 183),
    size=(143, 178),
    color='brown',
    object_type='object',
    is_elastic=True,
    out_bin=True
)

# Object 4
object3 = Object(
    index=3,
    name='blue object',
    location=(472, 270),
    size=(174, 238),
    color='blue',
    object_type='object',
    is_foldable=True,
    in_bin=True
)

if __name__ == '__main__':
    """
    bin 
    rigid but we don't have to consider this predicates.

    objects
    2 foldable objects: object1, object3
    1 elastic object: object2
    
    objects in the bin: object3
    objects out the bin: object1, object2

    Available action
    object1: [foldable, out_bin]: pick, place, fold
    object2: [elastic, out_bin]: pick, place, push
    object3: [foldable, in_bin]: out, place, fold
    
    Goal: packing all objects in the bin: make all objects state to in_bin = True
    """
    # Initialize robot
    robot = Robot()

    # Pick and place object1 in the bin
    robot.fold(object1)
    robot.pick(object1)
    robot.place(object1, bin1)

    # Pick and place object2 in the bin
    robot.pick(object2)
    robot.place(object2, bin1)
    robot.push(object2)

    # Don't out and place the object in the bin
    
    # End the planning
    robot.state_base()
