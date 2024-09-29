import rdflib

# Load the ontology into RDFLib
graph = rdflib.Graph()
graph.parse("ifixit_ontology.owl", format="xml")

# Query the data using SPARQL
query = """"""
results = graph.query(query)

for row in results:
    print(row)