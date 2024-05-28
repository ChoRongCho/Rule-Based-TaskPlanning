# from scripts.gpt_model.gpt_interface import GPTInterpreter


class Database:
    def __init__(self, def_table):
        """

        :param def_table:
        ---------------  -------------------------------------------------------
        Predicates List  Definition
        is_fragile       the fact of tending to break or be damaged easily
        is_rigid         the fact of being very strict and difficult to change
        is_soft          the quality of changing shape easily when pressed
        is_foldable      the ability to bend easily without breaking
        is_elastic       the quality of returning to its original size and shape
        ---------------  -------------------------------------------------------
        push: is_soft, is_rigid
        fold: is_fpldable
        pull: is_elastic
        is_fragile: we know this properties
        """
        self.def_table = def_table
        self.data_update = False
        self.database_path = ""
        self.object_database = {}

        self.user_message = ""
        self.system_message = f"This table defines the physical properties of the object we are investigating." + \
                              f"Answer the questions below in accordance with this criterion. \n"
        self.system_message += f"{self.def_table}"
        self.system_message += "\n"

        self.skill_predicates_pair = {"push": ["soft", "rigid"],
                                      "fold": ["foldable"],
                                      "pull": ["elastic"]}

    def update_database(self):
        pass

    def search(self):
        pass

    def prove(self):
        pass

    def load_prompt(self, action: str, predicate: str):
        self.user_message = f"\nThe first image shows before the robot {action} an unknown object. " + \
                            f"The second image shows after the robot presses an object. Does this object have {predicate} properties?" + \
                            f"Answer with the template below \nAnswer: \nReason: "
        return self.user_message
