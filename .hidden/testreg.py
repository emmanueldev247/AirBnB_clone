#!/c/Users/user/AppData/Local/Programs/Python/Python311/python
import re

input_strings = [
    'BaseModel "0ce69ff8-e48d-4313-b184-077caf565cff", {"attr_n": "attr_v"}',
    'BaseModel 849b7fa7-7f50-4cd5-be3d-ba70e0b4b766{"attr_name": "attr_value"}',
    'Place 9100dda7-1b0e-4341-82c2-8c2b5a94e91b, {"latitude": 9.8}',
    'Place e489bc54-9d91-4233-b8f8-58bb72a278c1 {"latitude": 9.8})'
]

pattern = r'(\w+)\s+("[^"]+"|[^\s,]+)\s*,?\s*({.*?})?\s*\)?$'

for input_string in input_strings:
    match = re.match(pattern, input_string)
    if match:
        class_name = match.group(1)
        class_id = match.group(2)
        dict_repr = match.group(3)
        print(f"Class Name: {class_name}, Class ID: {class_id}, Dictionary: {dict_repr}")
    else:
        print(f"No match for: {input_string}")

