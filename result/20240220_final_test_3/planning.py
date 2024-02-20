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
    is_flexible: bool=False
    is_fragile: bool=False
    is_foldable: bool=False
    is_soft: bool=False
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
        self.robot_now_holding = None
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
            print("Cannot pick an object in the bin or a box.")
        else:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_bin = True
            obj.in_bin = False
        
    # bin_packing
    def place(self, obj, bins):
        if self.robot_now_holding != obj or obj.object_type == 'box':
            print("Cannot place an object not in hand or a box.")
        else:
            print(f"Place {obj.name} in {bins.name}")
            self.state_handempty()
            obj.in_bin = True
            obj.out_bin = False
    
    # bin_packing
    def push(self, obj):
        if not self.robot_handempty or obj.is_fragile or not obj.is_soft:
            print("Cannot push an object when hand is not empty or the object is fragile or not soft.")
        else:
            print(f"Push {obj.name}")
    
    # bin_packing
    def fold(self, obj):
        if not self.robot_handempty or not obj.is_foldable:
            print("Cannot fold an object when hand is not empty or the object is not foldable.")
        else:
            print(f"Fold {obj.name}")
    
    def out(self, obj, bins):
        if not obj.in_bin:
            print("Cannot pick an object not in the bin.")
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
    is_flexible=True,
    is_fragile=True,
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
    is_elastic=True,
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
    is_fragile=True,
    is_soft=True,
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
    is_fragile=True,
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
    is_flexible=True,
    is_soft=True,
    in_bin=True
)

# Object 6
object6 = Object(
    index=5,
    name='brown object',
    location=(495, 275),
    size=(137, 117),
    color='brown',
    object_type='object',
    is_foldable=True,
    is_soft=True,
    in_bin=True
)

if __name__ == '__main__':
    # Initialize robot
    robot = Robot()

    # Pick and place object2 in the bin
    robot.pick(object2)
    robot.place(object2, bin1)

    # Pick and fold object6
    robot.pick(object6)
    robot.fold(object6)

    # Place folded object6 in the bin
    robot.place(object6, bin1)

    # Pick and place object3 in the bin
    robot.pick(object3)
    robot.place(object3, bin1)

    # Push object5 to make more space in the bin
    robot.push(object5)
