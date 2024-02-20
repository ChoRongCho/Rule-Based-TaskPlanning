Here is how you can fill the object class using the provided information:

```python
object1 = Object(
    index=0,
    name='white box',
    location=(509, 210),
    size=(231, 323),
    color='white',
    object_type='box',
    in_bin=True
)

object2 = Object(
    index=1,
    name='blue object',
    location=(204, 220),
    size=(361, 247),
    color='blue',
    object_type='object',
    out_bin=True,
    is_fragile=True,
    is_rigid=True
)

object3 = Object(
    index=2,
    name='yellow object',
    location=(83, 158),
    size=(135, 216),
    color='yellow',
    object_type='object',
    out_bin=True,
    is_foldable=True
)

object4 = Object(
    index=3,
    name='brown object',
    location=(257, 95),
    size=(139, 148),
    color='brown',
    object_type='object',
    out_bin=True,
    is_rigid=True
)
```

In this example, I have assumed that the location and size are represented as tuples of two integers. The color is represented as a string or a boolean value. The object type is represented as a string. The physical properties and bin packing predicates are represented as boolean values. If a predicate is not provided for an object, it is assumed to be False. If the values of the predicates for an object overlap with the default values, they are not written down.