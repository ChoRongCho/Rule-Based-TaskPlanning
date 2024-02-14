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
        self.robot_now_holding = None
        self.robot_base_pose = False

    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False

    # basic state
    def state_base(self):
        self.robot_base_pose = True

    # bin_packing, cooking
    def pick(self, obj):
        # make a preconditions for actions
        print(f"Pick {obj.name}")
        self.state_holding(obj)

    # bin_packing, cooking
    def place(self, obj, bins):
        # make a preconditions for actions
        print(f"Place {obj.name} in {bins.name}")
        self.state_handempty()
        self.state_base()

    # bin_packing
    def push(self, obj):
        # make a preconditions for actions
        if not self.robot_handempty:
            print(f"Can't push {obj.name}. Hand is not empty. ")
            return False
        print(f"Push {obj.name}")

    # bin_packing
    def fold(self, obj):
        # make a preconditions for actions
        print(f"Fold {obj.name}")

    # bin_packing
    def out(self, obj, bins):
        # make a preconditions for actions
        print(f"Out {obj.name} from {obj.name}")

    # blocksworld
    def pick_up(self, block1):
        # make a preconditions for actions
        print(f"Pick_up {block1.name}")

    # blocksworld
    def put_down(self, block1):
        # make a preconditions for actions
        print(f"Put_down {block1.name}")

    # blocksworld
    def stack(self, block1, block2):
        # make a preconditions for actions
        print(f"Stack {block1.name} on the {block2.name}")

    # blocksworld
    def unstack(self, block1, block2):
        # make a preconditions for actions
        print(f"Unstack {block1.name} from {block2.name}")

    # cooking
    def slice(self, ingredient):
        # make a preconditions for actions
        print(f"Slice {ingredient.name}")

    # hanoi
    def move(self, disk, peg):
        # make a preconditions for actions
        print(f"move {disk.name} to {peg.name}")
