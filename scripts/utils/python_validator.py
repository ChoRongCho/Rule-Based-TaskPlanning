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
    is_foldable: bool = False
    is_elastic: bool = False
    is_fragile: bool = False
    is_soft: bool = False

    # bin_packing Predicates (max 1)
    in_bin: bool = False
    out_bin: bool = False
    is_bigger_than_bin: bool = False
    on_the_object: object or bool = False


# Object 0
bin1 = Object(
    index=0,
    name='white box',
    location=(511, 216),
    size=(232, 324),
    color='white',
    object_type='box',
    is_foldable=True,
    is_elastic=True,
    in_bin=True
)

# Object 1
object1 = Object(
    index=1,
    name='yellow object',
    location=(82, 153),
    size=(138, 218),
    color='yellow',
    object_type='object',
    is_elastic=True,
    is_soft=True,
    out_bin=True
)

# Object 2
object2 = Object(
    index=2,
    name='blue object',
    location=(203, 216),
    size=(366, 247),
    color='blue',
    object_type='object',
    is_fragile=True,
    is_foldable=True,
    out_bin=True
)

# Object 3
object3 = Object(
    index=3,
    name='black object',
    location=(496, 276),
    size=(142, 118),
    color='black',
    object_type='object',
    is_foldable=True,
    is_soft=True,
    in_bin=True
)

# Object 4
object4 = Object(
    index=4,
    name='brown object',
    location=(502, 168),
    size=(152, 128),
    color='brown',
    object_type='object',
    is_foldable=True,
    in_bin=True
)


class PyValidator:
    def __init__(self,
                 python_script,
                 planning_result,
                 rule,
                 goal):
        self.python_script = python_script
        self.planning_result = planning_result
        self.rule = rule
        self.goal = goal

        self.planning_error = {
            0: "SyntaxError",
            1: "ActionError",
            2: "GoalStateError",
            3: "RuleError"
        }

        if "Cannot" in planning_result:
            planning_error_type = self.planning_error[1]

    def validate_goal_state(self, init_state, expected_goal_state):
        init_state_parsing = {
            object1.name: {
                "in_bin": object1.in_bin,
                "is_soft": object1.is_soft,
                "is_fragile": object1.is_fragile
            },
            "object2": {},
            "object3": {},
            "object4": {},
            "bin1": {}
        }
        pass

    def planning_output_recon(self):
        pass


def main():
    pass





if __name__ == '__main__':
    main()