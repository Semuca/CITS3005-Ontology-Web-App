import json
from rdflib import Graph, Literal, Namespace, RDF, RDFS, XSD

# Set up graph and namespaces
domain = "http://ifixthat.org"

PROCEDURE = Namespace(domain + "/procedure/")
ITEM = Namespace(domain + "/item/")
PART = Namespace(domain + "/part/")
TOOL = Namespace(domain + "/tool/")
STEP = Namespace(domain + "/step/")
IMAGE = Namespace(domain + "/image/")
PROPS = Namespace(domain + "/properties/")

g = Graph()
g.bind("procedure", PROCEDURE)
g.bind("item", ITEM)
g.bind("part", PART)
g.bind("tool", TOOL)
g.bind("step", STEP)
g.bind("image", IMAGE)
g.bind("props", PROPS)

# Helper functions
def to_uri(string: str | int) -> str:
    string = str(string)
    return string.replace(" ", "_")

# Entity loading functions
procedure_first_to_rest = {}
def load_procedure(procedure_json: dict[str, str]):
    # Create procedure and label
    procedure_uri = PROCEDURE[to_uri(procedure_json["Guidid"])]
    g.add((procedure_uri, RDF.type, PROPS.Procedure))
    g.add((procedure_uri, RDFS.label, Literal(procedure_json["Title"])))

    # requiresTool
    for tool in procedure_json["Toolbox"]:
        tool_uri = load_tool(tool)
        g.add((procedure_uri, PROPS.requiresTool, tool_uri))

    # guideOf
    subject = procedure_json["Subject"]
    category = procedure_json["Category"]
    category_uri = load_item(category, procedure_json["Ancestors"])
    if subject:
        part_uri = load_part(category, subject)
        g.add((procedure_uri, PROPS.guideOf, part_uri))
    else:
        g.add((procedure_uri, PROPS.guideOf, category_uri))

    # prerequisiteOf
    steps_list = []
    for step in procedure_json["Steps"]:
        load_step(step, procedure_json["Guidid"])
        steps_list.append(step["StepId"])

    first_step = steps_list[0]
    rest = steps_list[1:]
    if first_step in procedure_first_to_rest:
        for (other_id, other_rest) in procedure_first_to_rest.get(first_step, []):
            if rest == other_rest[:len(rest)]: # this is a prefix of the other
                g.add((procedure_uri, PROPS.prerequisiteOf, PROCEDURE[to_uri(other_id)]))
            elif other_rest == rest[:len(other_rest)]: # the other is a prefix of this
                g.add((PROCEDURE[to_uri(other_id)], PROPS.prerequisiteOf, procedure_uri))

    procedure_first_to_rest[first_step] = procedure_first_to_rest.get(first_step, []) + [(procedure_json["Guidid"], rest)]

def load_item(item_name: str, ancestors: list[str]):
    # Create item and label
    item_uri = ITEM[to_uri(item_name)]
    g.add((item_uri, RDF.type, PROPS.Item))
    g.add((item_uri, RDFS.label, Literal(item_name)))

    # subCategoryOf
    if ancestors[0] == "Root":
        return item_uri
    category_uri = load_item(ancestors[0], ancestors[1:])
    g.add((item_uri, PROPS.subCategoryOf, category_uri))

    return item_uri

def load_part(item_name: str, part_name: str):
    # Create part and label
    part_uri = PART[to_uri(f"{item_name} {part_name}")]
    g.add((part_uri, RDF.type, PROPS.Part))
    g.add((part_uri, RDFS.label, Literal(part_name)))

    # partOf
    g.add((part_uri, PROPS.partOf, ITEM[to_uri(item_name)]))

    return part_uri

def load_tool(tool_json: dict[str, str]):
    # Create tool and label
    tool_uri = TOOL[to_uri(tool_json["Name"])]
    g.add((tool_uri, RDF.type, PROPS.Tool))
    g.add((tool_uri, RDFS.label, Literal(tool_json["Name"])))

    # hasImage
    thumbnail = tool_json["Thumbnail"]
    if thumbnail:
        image_uri = load_image(tool_json["Thumbnail"])
        g.add((tool_uri, PROPS.hasImage, image_uri))

    # supplierUrl
    g.add((tool_uri, PROPS.supplierUrl, Literal(tool_json["Url"])))

    return tool_uri

def load_step(step_json: dict[str, str], procedure: int) -> str:
    # Create step
    step_uri = STEP[to_uri(step_json["StepId"])]
    g.add((step_uri, RDF.type, PROPS.Step))

    # stepOf
    g.add((step_uri, PROPS.stepOf, PROCEDURE[to_uri(procedure)]))

    # hasImage
    for image in step_json["Images"]:
        image_uri = load_image(image)
        g.add((step_uri, PROPS.hasImage, image_uri))

    # usesTool
    for tool in step_json["Tools_extracted"]:
        g.add((step_uri, PROPS.usesTool, TOOL[to_uri(tool)]))
        # Q: Need to check for tool existence?

    # index
    g.add((step_uri, PROPS.number, Literal(step_json["Order"], datatype=XSD.integer)))

    # actions
    g.add((step_uri, PROPS.actions, Literal(step_json["Text_raw"])))

    return step_uri

def load_image(url: str):
    # Create image and label
    image_uri = IMAGE[to_uri(url)]
    g.add((image_uri, RDF.type, PROPS.Image))

    # dataUrl
    g.add((image_uri, PROPS.dataUrl, Literal(url)))

    return image_uri

# Load JSON data from file
with open("Game Console.json") as file:
    count = 0
    for line in file:
        procedure_json = json.loads(line)
        load_procedure(procedure_json)

# Serialize graph to file
g.serialize("graph.rdf", format="xml", encoding="utf-8")


