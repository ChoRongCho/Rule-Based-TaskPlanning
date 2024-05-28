from dataclasses import dataclass


@dataclass
class Object:
    pass


class WorldDomain:
    """
    1. object
    2. actions
    3. current state
    4. goal state
    5. transition functions
    """
    def __init__(self):
        self.object_list = []
        self.actions = []
        self.map = []
        self.task = "bin_packing"
        self.obstacle = []

