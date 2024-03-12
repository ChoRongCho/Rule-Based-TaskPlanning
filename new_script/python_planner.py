import os
import subprocess
from new_script.changmin_planner import ChangminPlanner


class PythonPlanner(ChangminPlanner):
    def __init__(self, args):
        super().__init__(args=args)
        self.args = args

    def plan_and_run(self):
        self.plan()
        self.run()

    def plan(self):
        self.make_plan()

    def run(self):
        file_path = os.path.join(self.result_dir, "planning.py")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"There is no file at {file_path}. ")
        process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:  # robot action re-definition
            planning_output = output.decode('utf-8') + "\n" + error.decode('utf-8')

        else:
            planning_output = output.decode('utf-8') + "\n"

        if self.is_save:
            file_path = os.path.join(self.result_dir, "planning_result.txt")
            with open(file_path, "w") as file:
                file.write(str(planning_output) + "\n\n")
                file.close()
        return planning_output

    def feedback(self):
        for i in range(3):
            self.planning_feedback()
