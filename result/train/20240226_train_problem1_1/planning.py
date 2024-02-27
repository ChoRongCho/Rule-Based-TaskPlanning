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
    is_soft: bool = False
    is_elastic: bool = False
    is_foldable: bool = False
    is_rigid: bool = False

    # bin_packing Predicates (max 5)
    in_bin: bool = False
    out_bin: bool = False
    is_stackable: bool = False
    is_bigger_than_bin: bool = False
    on_the_object: object or bool = False

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
        else:
            print(f"Place {obj.name} in {bins.name}")
            self.state_handempty()
            obj.in_bin = True
            obj.out_bin = False

    # bin_packing
    def push(self, obj):
        if not self.robot_handempty or not obj.is_soft:
            print(f"Cannot push a {obj.name} when hand is not empty or the object is not soft.")
        else:
            print(f"Push {obj.name}")

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


# Object 1
bin1 = Object(
    index=2,
    name='white box',
    location=(498, 218),
    size=(250, 353),
    color='white',
    object_type='box',
    is_elastic=True,
    is_foldable=True,
    in_bin=True
)

# Object 2
object1 = Object(
    index=0,
    name='yellow sponge',
    location=(89, 136),
    size=(156, 154),
    color='yellow',
    object_type='sponge',
    is_rigid=True,
    out_bin=True
)

# Object 3
object2 = Object(
    index=1,
    name='blue paper towel',
    location=(203, 278),
    size=(156, 150),
    color='blue',
    object_type='paper towel',
    is_soft=True,
    out_bin=True
)

# Object 4
object3 = Object(
    index=3,
    name='black strips',
    location=(294, 150),
    size=(147, 123),
    color='black',
    object_type='strips',
    is_foldable=True,
    out_bin=True
)

if __name__ == '__main__':
    """
    bin 
    elastic and foldable but we don't have to consider this predicates.

    objects
    1 foldable objects: object3
    1 rigid object: object1
    1 soft object: object2
    
    objects in the bin: 
    objects out the bin: object1, object2, object3

    Available action
    object1: [rigid, out_bin]: pick, place
    object2: [soft, out_bin]: pick, place, push
    object3: [foldable, out_bin]: pick, place, fold
    
    Goal: packing all objects in the bin: make all objects state to in_bin = True
    """
    # Initialize robot
    robot = Robot()

    # Pick and place object2 in the bin
    robot.pick(object2)
    robot.place(object2, bin1)
    robot.push(object2)

    # Pick and place object1 in the bin
    robot.pick(object1)
    robot.place(object1, bin1)

    # Fold and place object3 in the bin
    robot.fold(object3)
    robot.pick(object3)
    robot.place(object3, bin1)
