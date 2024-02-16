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

    # hanoi Predicates (max 3)
    is_on_peg: str or bool
    is_on_top: bool
    is_smaller_than: Object or bool
