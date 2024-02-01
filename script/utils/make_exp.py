import json
import os


class CreateExperiment:
    def __init__(self,
                 exp_name: str,
                 task_name: str,
                 home_dir: str or None = None):

        self.exp_name = exp_name
        self.task_name = task_name
        self.home_dir = home_dir
        if not self.home_dir:
            self.current_dir = os.getcwd()
        else:
            self.current_dir = self.home_dir
        self.target_path = os.path.join(self.current_dir, "instructions", self.exp_name)

        # target directory
        self.file_name = ["env_info.json",
                          "pddl_info.json",
                          "robot_info.json",
                          "scene_info.json",
                          "task_info.json"]

    def dir_check(self):
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)
            print(f"Directory '{self.target_path}' created.")
        else:
            print(f"Directory '{self.target_path}' exist.")

    def make_files(self):
        for file_name in self.file_name:
            target_file = os.path.join(self.target_path, file_name)
            with open(target_file, 'w') as f:
                description = self.write_description(file_name)
                json_object = {"exp_name": self.exp_name,
                               "task_name": self.task_name,
                               "descriptions": description
                               }
                json_object = json.dumps(json_object, indent=4)
                f.write(json_object)
                f.close()

    def write_description(self, mode: str):
        if "env" in mode:
            description = {
                "scene0": "",
                "scene1": "",
                "scene2": "",
                "scene3": "",
            }

        elif "pddl" in mode:
            description = {
                "rule0": f"Domain name must be {self.task_name}. ",
                "rule1": f"Problem name must be  {self.task_name}_problem. ",
                "rule2": "Use an only given action set",
                "rule3": "Add your rules",
            }
        elif "robot" in mode:
            description = {
                "action0": "pick an object",
                "action1": "place an object in hand",
                "action2": "push an object toward ground",
                "action3": "Add your actions",
            }
        elif "scene" in mode:
            description = {
                "image_url0": "original observation",
                "image_url1": "after actions",
                "image_url2": "",
                "image_url3": "",
                "image_url4": "",
            }
        elif "task" in mode:
            description = {
                "rule0": f"The task name is {self.task_name}. ",
                "init": "",
                "goal": "",
                "rule3": "Add your task descriptions. "
            }
        else:
            raise ValueError
        return description

    def start_exp(self):
        self.dir_check()
        self.make_files()
        print("Done")


def main():
    exp = CreateExperiment("str", "str3")


if __name__ == '__main__':
    main()
