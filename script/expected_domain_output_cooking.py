"""
The definition for domain input
1. task name
2. robot action, state: available action: give the constraint and pre-condition and effect
3. object list, state: from LLMs and images, get predicates
4. predicates:

"""
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

    # bin_packing predicates
    on_item: bool
    left_item: bool
    right_item: bool
    top_item: bool
    bottom_item: bool
    is_flexible: bool
    is_rigid: bool
    is_fragile: bool
    is_soft: bool
    out_bin: bool
    in_bin: bool = False
