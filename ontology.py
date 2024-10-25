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
    class subCategoryOf(ObjectProperty, TransitiveProperty):
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
def to_uri(string: str | int) -> str:
    string = str(string)
    return string.replace(" ", "_")

procedure_to_steps = {}
def load_procedure(procedure_json: dict[str, str]):
    # Create procedure and label
    procedure_id = to_uri(procedure_json["Guidid"])
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

def load_item(item_name: str, ancestors: list[str]):
    # Create item and label
    item_id = to_uri(item_name)
    item_instance = ifixthat.Item(item_id, namespace=item_ns)
    item_instance.label = item_name

    # subCategoryOf
    if ancestors[0] == "Root":
        return item_instance
    category_instance = load_item(ancestors[0], ancestors[1:])
    item_instance.subCategoryOf.append(category_instance)

    return item_instance

def load_part(item_name: str, part_name: str) -> Part:
    # Create part and label
    part_id = to_uri(f"{item_name} {part_name}")
    part_instance = ifixthat.Part(part_id, namespace=part_ns)
    part_instance.label = part_name

    # partOf
    item_instance = ifixthat.Item(to_uri(item_name), namespace=item_ns)
    part_instance.partOf.append(item_instance)

    return part_instance

def load_tool(tool_json: dict[str, str]) -> Tool:
    # Create tool and label
    tool_id = to_uri(tool_json["Name"])
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

    return tool_instance

def load_step(step_json: dict[str, str]) -> Step:
    # Create step and label
    step_id = to_uri(step_json["StepId"])
    step_instance = ifixthat.Step(step_id, namespace=step_ns)

    # hasImage
    for image in step_json["Images"]:
        image_instance = load_image(image)
        step_instance.hasImage.append(image_instance)

    # usesTool
    for tool in step_json["Tools_extracted"]:
        if tool == "NA":
            continue
        tool_instance = ifixthat.Tool(to_uri(tool), namespace=tool_ns)
        step_instance.usesTool.append(tool_instance)

    # actions
    step_instance.actions.append(step_json["Text_raw"])

    return step_instance

url_to_image = {}
def load_image(url: str) -> Image:
    # Check if image already exists
    if url in url_to_image:
        return url_to_image[url]

    # Create image
    image_instance = ifixthat.Image(namespace=image_ns)

    # dataUrl
    image_instance.dataUrl.append(url)

    url_to_image[url] = image_instance
    return image_instance

# Load JSON data into ontology
with open("Game Console.json") as file:
    for line in file:
        procedure_json = json.loads(line)
        load_procedure(procedure_json)

# Serialize ontology to file
ifixthat.save(file="ontology.owl")
