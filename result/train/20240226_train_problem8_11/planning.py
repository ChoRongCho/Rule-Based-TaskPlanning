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
    is_elastic: bool = False
    is_soft: bool = False
    is_rigid: bool = False

    # bin_packing Predicates (max 5)
    in_bin: bool = False
    out_bin: bool = False
    is_bigger_than_bin: bool = False
    on_the_object: object or bool = False
    is_folded: bool = False

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
        if not self.robot_handempty or obj.is_rigid or obj.on_the_object:
            print(f"Cannot push a {obj.name} when hand is not empty or the object is rigid or there is an object on it.")
        elif obj.is_soft:
            print(f"Push {obj.name}")
        else:
            print(f"Cannot push {obj.name} because it is not soft.")

    # bin_packing
    def fold(self, obj):
        if not self.robot_handempty or not obj.is_foldable or obj.in_bin:
            print(f"Cannot fold a {obj.name} when hand is not empty or the object is not foldable or the object is in the bin.")
        else:
            print(f"Fold {obj.name}")
            obj.is_folded = True

    def out(self, obj, bins):
        if not obj.in_bin:
            print(f"Cannot pick a {obj.name} not in the bin.")
        else:
            print(f"Out {obj.name} from {bins.name}")
            self.state_holding(obj)
            obj.in_bin = False
            obj.out_bin = True


# Object 1
bin1 = Object(
    index=0,
    name='white box',
    location=(511, 216),
    size=(232, 324),
    color='white',
    object_type='box',
    is_foldable=True,
    in_bin=True
)

# Object 2
object2 = Object(
    index=1,
    name='yellow object',
    location=(82, 153),
    size=(138, 218),
    color='yellow',
    object_type='object',
    is_soft=True,
    out_bin=True
)

# Object 3
object3 = Object(
    index=2,
    name='blue object',
    location=(203, 216),
    size=(366, 247),
    color='blue',
    object_type='object',
    is_elastic=True,
    out_bin=True
)

# Object 4
object4 = Object(
    index=3,
    name='black object',
    location=(496, 276),
    size=(142, 118),
    color='black',
    object_type='object',
    is_rigid=True,
    is_elastic=True,
    in_bin=True
)

# Object 5
object5 = Object(
    index=4,
    name='brown object',
    location=(502, 168),
    size=(152, 128),
    color='brown',
    object_type='object',
    is_foldable=True,
    in_bin=True
)

if __name__ == '__main__':
    """
    bin 
    foldable but we don't have to consider this predicates.

    objects
    2 foldable objects: object5
    1 soft object: object2
    2 elastic objects: object3, object4
    1 rigid object: object4

    objects in the bin: object4, object5
    objects out the bin: object2, object3

    Available action
    object2: [soft, out_bin]: pick, place, push
    object3: [elastic, out_bin]: pick, place
    object4: [rigid, elastic, in_bin]: out, place
    object5: [foldable, in_bin]: out, place, fold

    Goal: packing all objects in the bin: make all objects state to in_bin = True
    """
    # Initialize robot
    robot = Robot()

    # Pick and place object2 in the bin
    robot.pick(object2)
    robot.place(object2, bin1)
    robot.push(object2)

    # Pick and place object3 in the bin
    robot.pick(object3)
    robot.place(object3, bin1)

    # Don't out and place the object in the bin
    
    # End the planning
    robot.state_base()
