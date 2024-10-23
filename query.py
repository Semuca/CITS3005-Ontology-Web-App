from owlready2 import *

# Load the ontology as RDFLib graph
ifixthat = get_ontology("ontology.owl").load()
graph = default_world.as_rdflib_graph()

DOMAIN = "http://ifixthat.org/"
graph.bind("ifixthat", DOMAIN)
graph.bind("procedure", f"{DOMAIN}Procedure#")
graph.bind("item", f"{DOMAIN}Item#")
graph.bind("part", f"{DOMAIN}Part#")
graph.bind("tool", f"{DOMAIN}Tool#")
graph.bind("step", f"{DOMAIN}Step#")
graph.bind("image", f"{DOMAIN}Image#")

# Query for 'What Procedures have more than 6 steps?'
query_more_than_6_steps = """
    SELECT ?procedure (COUNT(?orderedStep) AS ?stepCount)
    WHERE {
        ?procedure a ifixthat:Procedure .
        ?procedure ifixthat:hasStep ?orderedStep .
    }
    GROUP BY ?procedure
    HAVING (COUNT(?orderedStep) > 6)
"""

print("\nQuery for 'What Procedures have more than 6 steps?'")
for row in graph.query(query_more_than_6_steps):
    print(row)

# Query for 'What are the step ids in order for Procedure 1562 and their actions?'
query_ordered_step_actions = """
    SELECT ?order ?step ?actions
    WHERE {
        procedure:1562 ifixthat:hasStep ?orderedStep .
        ?orderedStep ifixthat:details ?step .
        ?orderedStep ifixthat:order ?order .
        ?step ifixthat:actions ?actions .
    }
    ORDER BY ?order
"""

print("\nQuery for 'What are the step ids in order for Procedure 1562 and their actions?'")
for row in graph.query(query_ordered_step_actions):
    print(row)
    print("\n")

