import rdflib

# Load the ontology into RDFLib
g = rdflib.Graph()
g.parse("data.rdf", format="xml")

# Query for 'What guides have 6 or more steps?'
querySixOrMoreParts = """
    SELECT ?guide (COUNT(?step) AS ?stepCount)
    WHERE {
        ?step rdf:type ifixit:step .
        ?step ifixit:stepOf ?guide .
    }
    GROUP BY ?guide
    HAVING (COUNT(?step) >= 6)
"""

print("\nQuery for 'What guides have 6 or more steps?'")
for row in g.query(querySixOrMoreParts):
    print(row)