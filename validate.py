# By Heidi Leow (23643117) and James Frayne (23372032)

import json
from rdflib import Graph, Namespace
from pyshacl import validate
from owlready2 import get_ontology, default_world, sync_reasoner_pellet, Imp

ifixthat = get_ontology("ontology.owl").load()

# Open swrl.txt and load the rules from each line
with open('swrl.txt', 'r') as file:
    lines = file.readlines()

with ifixthat:
    for line in lines:
        imp = Imp()
        imp.set_as_rule(line)

# Perform reasoning
print("STARTING REASONER")
sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
print("REASONER FINISHED")

# Create SHACL graph
knowledge_graph = default_world.as_rdflib_graph()

shacl = Namespace("http://www.w3.org/ns/shacl#")
shacl_graph = Graph()
shacl_graph.parse("shapes.ttl", format="turtle")


# Perform SHACL validation
print("STARTING VALIDATION")
conforms, results_graph, results_text = validate(
    knowledge_graph,
    shacl_graph=shacl_graph,
    inference='none',
)
print("VALIDATION FINISHED")

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

print(shacl_results)
print(len(shacl_results))