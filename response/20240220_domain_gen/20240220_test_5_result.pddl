Here is how you can fill the object class using the provided information:

```python
# Object 1
object1 = Object(
    index=0,
    name='white box',
    location=(509, 210),
    size=(231, 323),
    color='white',
    object_type='box',
    in_bin=True
)

# Object 2
object2 = Object(
    index=1,
    name='blue object',
    location=(204, 220),
    size=(361, 247),
    color='blue',
    object_type='object',
    is_fragile=True,
    is_rigid=True,
    out_bin=True
)

# Object 3
object3 = Object(
    index=2,
    name='yellow object',
    location=(83, 158),
    size=(135, 216),
    color='yellow',
    object_type='object',
    is_foldable=True,
    out_bin=True
)

# Object 4
object4 = Object(
    index=3,
    name='brown object',
    location=(257, 95),
    size=(139, 148),
    color='brown',
    object_type='object',
    is_rigid=True,
    out_bin=True
)
```

In this case, we have assumed that the 'white box' is the bin and all other objects are outside the bin. The physical properties of the objects are assigned based on the provided information. If no information is provided for a certain property, it is assumed to be False.