
from rdflib import Graph
from pyshacl import validate
from owlready2 import get_ontology, default_world

get_ontology("ontology.owl").load()
knowledge_graph = default_world.as_rdflib_graph()

shacl_graph = Graph()
shacl_graph.parse("shapes.ttl", format="turtle")

conforms, results_graph, results_text = validate(
    knowledge_graph,
    shacl_graph=shacl_graph,
    inference='none',
)

print(f"\n{results_text}")
