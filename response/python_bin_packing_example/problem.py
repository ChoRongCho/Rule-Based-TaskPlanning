from domain import Object

obj_info = {
    "box": Object(index=0, name="box", location=(0, 0), size=(50, 50), color=None, object_type="bins", in_bin=True),
    "obj1": Object(index=1, name="obj1", location=(100, 100), size=(30, 20), color=None, object_type="objects", is_fragile=True),
    "obj2": Object(index=2, name="obj2", location=(130, 100), size=(20, 20), color=None, object_type="objects", is_soft=True, is_flexible=True),
    "obj3": Object(index=3, name="obj3", location=(100, 130), size=(30, 30), color=None, object_type="objects", is_flexible=True),
    "obj4": Object(index=4, name="obj4", location=(130, 130), size=(20, 20), color=None, object_type="objects", is_rigid=True),
}


class Problem:
    def __init__(self, obj_info):
        self.obj_info = obj_info


def main():
    # object list and its init state

    object_list = [""]


