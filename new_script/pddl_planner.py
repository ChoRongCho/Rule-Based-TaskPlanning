from changmin_planner import ChangminPlanner
from new_script.utils.prompt_function import PromptSetPDDL


class PDDLPlanner(ChangminPlanner):
    def __init__(self, args):
        super().__init__(args=args)
        self.args = args
        self.load_prompt = PromptSetPDDL(task=self.task, task_description=self.task_description)
