"""Main route views"""

import json
from typing import Self
from flask import Blueprint
from owlready2 import get_ontology, default_world, sync_reasoner_pellet, Imp
from pyshacl import validate
from rdflib import Graph, Namespace

main_bp = Blueprint('main_bp', __name__)

class Link:

    type_to_icon_map = {
        'Item': 'category',
        'Part': 'toys_and_games',
        'Procedure': 'receipt_long',
        'Step': 'stairs_2',
        'Tool': 'construction',
    }

    def __init__(self: Self, thing: any, title: str = None, subtitle: str = None, images: list[str] = [], hideContent: bool = False) -> None:
        self.ref = thing
        self.uri = thing.iri

        self.images = images
        self.hideContent = hideContent

        self.rdf_type = thing.is_a[0].name
        self.url = "/" + self.rdf_type + "/" + thing.iri.split("#")[-1]
        self.name = thing.iri.split("#")[-1]

        self.title = title or (len(thing.label) > 0 and thing.label[0]) or self.name
        self.subtitle = subtitle or self.rdf_type.capitalize()

        self.icon = self.type_to_icon_map.get(self.rdf_type, 'help')

ifixthat = get_ontology("../ontology.owl").load()

# Open swrl.txt and load the rules from each line
with open('../swrl.txt', 'r') as file:
    lines = file.readlines()

with ifixthat:
    for line in lines:
        imp = Imp()
        imp.set_as_rule(line)

# Run the reasoner
print("REASONER FINISHED")
sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
print("REASONER FINISHED")


# Create a graph from the ontology
g = default_world.as_rdflib_graph()

domain = "http://ifixthat.org/"
g.bind("ifixthat", domain)
g.bind("procedure", f"{domain}Procedure#")
g.bind("item", f"{domain}Item#")
g.bind("part", f"{domain}Part#")
g.bind("tool", f"{domain}Tool#")
g.bind("step", f"{domain}Step#")
g.bind("image", f"{domain}Image#")


# Perform SHACL validation
shacl = Namespace("http://www.w3.org/ns/shacl#")
shacl_graph = Graph()
shacl_graph.parse("shapes.ttl", format="turtle")

print("STARTING VALIDATION")
conforms, results_graph, results_text = validate(
    g,
    shacl_graph=shacl_graph,
    inference='none',
)
print("VALIDATION FINISHED")


# Collect the error results
print("COLLECTING RESULTS")
dup_shacl_results = []
for result in results_graph.subjects():
    shacl_result = {}

    # Skip the result if it only has one predicate (Which is a pass)
    severity = results_graph.value(subject=result, predicate=shacl.resultSeverity)

    if not (severity and severity == shacl.Violation):
        continue

    for predicate, obj in results_graph.predicate_objects(subject=result):
        if (predicate == shacl.focusNode):
            shacl_result[predicate.split("#")[-1] if "#" in predicate else predicate] = obj
        else:
            shacl_result[predicate.split("#")[-1] if "#" in predicate else predicate] = obj.split("#")[-1] if "#" in obj else obj

    if 'detail' in shacl_result:
        detail = {}
        for predicate, obj in results_graph.predicate_objects(subject=shacl_result['detail']):
            if (predicate == shacl.focusNode):
                detail[predicate.split("#")[-1] if "#" in predicate else predicate] = obj
            else:
                detail[predicate.split("#")[-1] if "#" in predicate else predicate] = obj.split("#")[-1] if "#" in obj else obj
        shacl_result['detail'] = detail

    dup_shacl_results.append(shacl_result)
shacl_results = list({json.dumps(d, sort_keys=True): d for d in dup_shacl_results}.values())
print("COLLECTION FINISHED")