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

    # bin_packing Predicates (max 3)
    in_bin: bool
    fits_in_bin: bool
    on_top_of: Object or bool
