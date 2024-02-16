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
    is_rigid: bool
    is_fragile: bool
    is_foldable: bool
    is_soft: bool

    # bin_packing Predicates (max 6)
    in_bin: bool
    out_bin: bool
    is_stackable: bool
    is_bigger_than_bin: bool
    on_the_object: Object or bool
    is_packed: bool
