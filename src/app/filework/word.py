import json
from docxtpl import DocxTemplate
import os
import uuid

async def create_file(data_json, path, old_name, new_name):
    data_json_1 = data_json["documentTables"]
    data_json_2 = data_json["documentValues"]
    data = dict(data_json_1)
    data.update(data_json_2)
    doc = DocxTemplate(os.path.join(path, old_name))
    doc.render(data)
    if not new_name:
        new_name = str(uuid.uuid4())
    new_path = os.path.join(path, new_name)
    doc.save(new_path)
    return new_path
