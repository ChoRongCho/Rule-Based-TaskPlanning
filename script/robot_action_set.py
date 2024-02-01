class Robot:
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

    def state_handempty(self):
        self.robot_handempty = True

    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects

    def state_base(self):
        self.robot_base_pose = True

    def pick(self):
        pass

    def place(self):
        pass

    def push(self):
        pass

    def fold(self):
        pass

    def out(self):
        pass

    def pick_up(self):
        pass

    def put_down(self):
        pass

    def stack(self):
        pass

    def unstack(self):
        pass

    def slice(self):
        pass

    def move(self):
        pass
