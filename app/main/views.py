"""Main route views"""
# By Heidi Leow (23643117) and James Frayne (23372032)

import json
from flask import Blueprint
from owlready2 import *
from pyshacl import validate
from rdflib import Graph, Namespace

main_bp = Blueprint('main_bp', __name__)

domain = "http://ifixthat.org/"
ifixthat = get_ontology("../ontology.owl").load()

g = None
shacl_results = []

def convert_onto_to_rdf():
    global g

    # Create a graph from the ontology
    g = default_world.as_rdflib_graph()

    g.bind("ifixthat", domain)
    g.bind("procedure", f"{domain}Procedure#")
    g.bind("item", f"{domain}Item#")
    g.bind("part", f"{domain}Part#")
    g.bind("tool", f"{domain}Tool#")
    g.bind("step", f"{domain}Step#")
    g.bind("image", f"{domain}Image#")

def run_reasoner():
    global g, ifixthat, shacl_results
    # Open swrl.txt and load the rules from each line
    with open('../swrl.txt', 'r') as file:
        lines = file.readlines()

    with ifixthat:
        for line in lines:
            imp = Imp()
            imp.set_as_rule(line)

    # Run the reasoner
    print("REASONER STARTED")
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    print("REASONER FINISHED")

    convert_onto_to_rdf()

    # Perform SHACL validation
    shacl = Namespace("http://www.w3.org/ns/shacl#")
    shacl_graph = Graph()
    shacl_graph.parse("../shapes.ttl", format="turtle")

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
    print(shacl_results)
    print("COLLECTION FINISHED")