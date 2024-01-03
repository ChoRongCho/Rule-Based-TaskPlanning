import json

my_dict_1 = {"index": 3,
             "role": "user",
             "content": "hi",
             "image_path": False}

my_dict_2 = {"index": 2,
             "role": "system",
             "content": "hi there",
             "image_path": False}

prompt = [my_dict_1, my_dict_2]
prompt_dict = {"prompt": prompt}

json_obj = json.dumps(prompt_dict, indent=4)
with open(r"../../response/test.json", "w") as f:
    f.write(json_obj)
