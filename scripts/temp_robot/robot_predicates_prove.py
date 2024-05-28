import os
from scripts.temp_robot.robot import Robot
from scripts.utils.utils import list_file, sort_files


class RobotProve(Robot):
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None,
                 gpt_interface: object = False):
        super().__init__(name, goal, actions)

        self.predicates = self.active_predicates_list
        self.gpt_interface = gpt_interface
        self.object_list = [
            "obj1",
            "obj2",
            "obj3",
            "obj4",
            "obj5",
            "obj6",
            "obj7",
            "obj8"
        ]
        self.data_path = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/predicates_prove"

    def get_object_predicates(self, info: dict) -> list:
        """

        :param info: {'white box': [509, 210, 231, 323]}
        :return: list ['pred1', 'pred2', 'pred3']
        """
        name = list(info.keys())[0]
        name_database = list(self.database.object_database.keys())

        if name in name_database:
            print("Load dataset predicates")
            info = self.database.object_database.get(name)
            predicates = info.get("predicates")
            return predicates

        else:
            print("Active Prove")

            # take image
            images = ["", "", ""]

            self.gpt_prove_object(info, images)
            return [False]

    def gpt_prove_object(self, info, images):
        name = list(info.keys())[0]
        root = os.path.join(self.data_path, name)
        obj_data_path = list_file(root)
        obj_data_path = sort_files(obj_data_path)

        is_push, is_fold, is_pull = False, False, False
        for data_name in obj_data_path:
            if "push" in data_name:
                is_push = True
                continue
            if "fold" in data_name:
                is_fold = True
                continue
            if "pull" in data_name:
                is_pull = True
                continue



    def get_datapath(self, name):
        pass


    def identifying_properties(self, images: list or False = False):
        if not images:
            # self.database_path 내의 모든 이미지를 data로 불러오
            pass
        skills = self.database.skill_predicates_pair.keys()
        # push
        push_image = []
        for image in images:
            if skills[0] in image:
                push_image.append(image)

        # fold
        fold_image = []
        for image in images:
            if skills[1] in image:
                fold_image.append(image)

        # pull
        pull_image = []
        for image in images:
            if skills[2] in image:
                pull_image.append(image)

        return push_image, fold_image, pull_image


