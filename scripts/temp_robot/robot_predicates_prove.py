from scripts.temp_robot.robot import Robot


class RobotProve(Robot):
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        super().__init__(name, goal, actions)
        self.predicates = self.active_predicates_list

    def prove_fragile(self, obj):
        image1 = self.get_image()
        self.push(obj)
        image2 = self.get_image()

    def prove_push(self):
        pass

    def prove_fold(self):
        pass

    def get_image(self):
        return True

    def get_object_predicates(self, info):
        self.prove_push()
        self.prove_fold()
        self.prove_fragile(info)
        predicates = []
        return predicates
