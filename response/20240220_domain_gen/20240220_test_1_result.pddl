Based on the provided information and the image, I will fill out the Object class for each item:

```python
# White box
object0 = Object(
    index=0,
    name="white box",
    location=(509, 210),
    size=(231, 323),
    color="white",
    object_type="box",
    is_rigid=False,
    is_flexible=False,
    is_soft=False,
    is_foldable=False,
    in_bin=True,
    out_bin=False,
    is_stackable=False,
    is_bigger_than_bin=False,
    on_the_object=False
)

# Blue object
object1 = Object(
    index=1,
    name="blue object",
    location=(204, 220),
    size=(361, 247),
    color="blue",
    object_type="object",
    is_rigid=True,
    is_flexible=False,
    is_soft=False,
    is_foldable=False,
    in_bin=False,
    out_bin=True,
    is_stackable=False,
    is_bigger_than_bin=False,
    on_the_object=False
)

# Yellow object
object2 = Object(
    index=2,
    name="yellow object",
    location=(83, 158),
    size=(135, 216),
    color="yellow",
    object_type="object",
    is_rigid=False,
    is_flexible=False,
    is_soft=False,
    is_foldable=True,
    in_bin=False,
