import json
from owlready2 import Thing, get_ontology, ObjectProperty, TransitiveProperty, DataProperty

# Set up ontology classes and properties
DOMAIN = "http://ifixthat.org/"
ifixthat = get_ontology(DOMAIN)

procedure_ns = ifixthat.get_namespace(DOMAIN + "Procedure")
item_ns = ifixthat.get_namespace(DOMAIN + "Item")
part_ns = ifixthat.get_namespace(DOMAIN + "Part")
tool_ns = ifixthat.get_namespace(DOMAIN + "Tool")
step_ns = ifixthat.get_namespace(DOMAIN + "Step")
image_ns = ifixthat.get_namespace(DOMAIN + "Image")

with ifixthat:
    class Procedure(Thing):
        pass
    class Item(Thing):
        pass
    class Part(Thing):
        pass
    class Tool(Thing):
        pass
    class Step(Thing):
        pass
    class Image(Thing):
        pass

    # To connect procedures to ordered steps
    class OrderedStep(Thing):
        pass

    # To keep track of iris manually - so we can set guide and step iris
    class lastIri(DataProperty):
        domain = [Thing]
        range = [int]

    # Procedure schema
    class subProcedureOf(ObjectProperty, TransitiveProperty):
        domain = [Procedure]
        range = [Procedure]

    class requiresTool(ObjectProperty):
        domain = [Procedure]
        range = [Tool]

    class guideOf(ObjectProperty):
        domain = [Procedure]
        range = [Item | Part]

    class hasStep(ObjectProperty):
        domain = [Procedure]
        range = [OrderedStep]

    class order(DataProperty):
        domain = [OrderedStep]
        range = [int]

    class details(ObjectProperty):
        domain = [OrderedStep]
        range = [Step]

    # Item schema
    class subCategoryOf(ObjectProperty):
        domain = [Item]
        range = [Item]

    # Part schema
    class partOf(ObjectProperty, TransitiveProperty):
        domain = [Part]
        range = [Part | Item]

    # Tool schema
    class hasImage(ObjectProperty):
        domain = [Tool | Step]
        range = [Image]

    class supplierUrl(DataProperty):
        domain = [Tool]
        range = [str]


    class usesTool(ObjectProperty):
        domain = [Step]
        range = [Tool]

    class actions(DataProperty):
        domain = [Step]
        range = [str]

    # Image schema
    class dataUrl(DataProperty):
        domain = [Image]
        range = [str]

# Entity loading functions
id_tracker = { ifixthat.Tool: 0, ifixthat.Item: 0, ifixthat.Part: 0, ifixthat.Image: 0, ifixthat.Procedure: 0, ifixthat.Step: 0 }

procedure_to_steps = {}
def load_procedure(procedure_json: dict[str, str]):
    # Create procedure and label
    procedure_id = str(procedure_json["Guidid"])
    procedure_instance = ifixthat.Procedure(procedure_id, namespace=procedure_ns)
    procedure_instance.label = procedure_json["Title"]

    # requiresTool
    for tool in procedure_json["Toolbox"]:
        tool_instance = load_tool(tool)
        procedure_instance.requiresTool.append(tool_instance)

    # guideOf
    subject = procedure_json["Subject"]
    category = procedure_json["Category"]
    category_instance = load_item(category, procedure_json["Ancestors"])
    if subject:
        part_instance = load_part(category, subject)
        procedure_instance.guideOf.append(part_instance)
    else:
        procedure_instance.guideOf.append(category_instance)

    # hasStep
    steps_list = []
    for step in procedure_json["Steps"]:
        step_instance = load_step(step)
        steps_list.append(step_instance)

        order = step["Order"]
        ordered_step_instance = ifixthat.OrderedStep()
        ordered_step_instance.details.append(step_instance)
        ordered_step_instance.order.append(order)
        procedure_instance.hasStep.append(ordered_step_instance)

    # subProcedureOf
    steps_set = set(steps_list)
    for other_procedure_instance, other_steps_set in procedure_to_steps.items():
        if steps_set.issubset(other_steps_set):
            procedure_instance.subProcedureOf.append(other_procedure_instance)
        elif other_steps_set.issubset(steps_set):
            other_procedure_instance.subProcedureOf.append(procedure_instance)
    procedure_to_steps[procedure_instance] = steps_set

    if int(procedure_id) > id_tracker[ifixthat.Procedure]:
        id_tracker[ifixthat.Procedure] = int(procedure_id)

name_to_item = {}
def load_item(item_name: str, ancestors: list[str]):
    # Check if item already exists
    if item_name in name_to_item:
        return name_to_item[item_name]

    # Create item and label
    id_tracker[ifixthat.Item] += 1
    item_id = str(id_tracker[ifixthat.Item])
    item_instance = ifixthat.Item(item_id, namespace=item_ns)
    item_instance.label = item_name

    # subCategoryOf
    if ancestors[0] == "Root":
        return item_instance
    category_instance = load_item(ancestors[0], ancestors[1:])
    item_instance.subCategoryOf.append(category_instance)

    name_to_item[item_name] = item_instance
    return item_instance

name_to_part = {}
def load_part(item_name: str, part_name: str) -> Part:
    # Check if part already exists
    if f"{item_name} {part_name}" in name_to_part:
        return name_to_part[f"{item_name} {part_name}"]

    # Create part and label
    id_tracker[ifixthat.Part] += 1
    part_id = str(id_tracker[ifixthat.Part])
    part_instance = ifixthat.Part(part_id, namespace=part_ns)
    part_instance.label = part_name

    # partOf
    if item_name in name_to_item:
        item_instance = name_to_item[item_name]
    else:
        id_tracker[ifixthat.Item] += 1
        item_instance = ifixthat.Item(str(id_tracker[ifixthat.Item]), namespace=item_ns)
    part_instance.partOf.append(item_instance)

    name_to_part[f"{item_name} {part_name}"] = part_instance
    return part_instance

name_to_tool = {}
def load_tool(tool_json: dict[str, str]) -> Tool:
    # Check if tool already exists
    if tool_json["Name"] in name_to_tool:
        return name_to_tool[tool_json["Name"]]

    # Create tool and label
    id_tracker[ifixthat.Tool] += 1
    tool_id = str(id_tracker[ifixthat.Tool])
    tool_instance = ifixthat.Tool(tool_id, namespace=tool_ns)
    tool_instance.label = tool_json["Name"]

    # hasImage
    thumbnail = tool_json["Thumbnail"]
    if thumbnail:
        image_instance = load_image(thumbnail)
        tool_instance.hasImage.append(image_instance)

    # supplierUrl
    url = tool_json["Url"]
    if url:
        tool_instance.supplierUrl.append(tool_json["Url"])

    name_to_tool[tool_json["Name"]] = tool_instance
    return tool_instance

def load_step(step_json: dict[str, str]) -> Step:
    # Create step and label
    step_id = str(step_json["StepId"])
    step_instance = ifixthat.Step(step_id, namespace=step_ns)

    # hasImage
    for image in step_json["Images"]:
        image_instance = load_image(image)
        step_instance.hasImage.append(image_instance)

    # usesTool
    for tool in step_json["Tools_extracted"]:
        if tool == "NA":
            continue
        if tool in name_to_tool:
            tool_instance = name_to_tool[tool]
        else:
            id_tracker[ifixthat.Tool] += 1
            tool_instance = ifixthat.Tool(str(id_tracker[ifixthat.Tool]), namespace=tool_ns)
        step_instance.usesTool.append(tool_instance)

    # actions
    step_instance.actions.append(step_json["Text_raw"])

    if int(step_id) > id_tracker[ifixthat.Step]:
        id_tracker[ifixthat.Step] = int(step_id)

    return step_instance

url_to_image = {}
def load_image(url: str) -> Image:
    # Check if image already exists
    if url in url_to_image:
        return url_to_image[url]

    # Create image
    id_tracker[ifixthat.Image] += 1
    image_id = str(id_tracker[ifixthat.Image])
    image_instance = ifixthat.Image(image_id, namespace=image_ns)

    # dataUrl
    image_instance.dataUrl.append(url)

    url_to_image[url] = image_instance
    return image_instance

# Load JSON data into ontology
with open("Game Console.json") as file:
    for line in file:
        procedure_json = json.loads(line)
        load_procedure(procedure_json)

for class_instance, last_id in id_tracker.items():
    class_instance.lastIri = last_id

# Serialize ontology to file
ifixthat.save(file="ontology.owl")
