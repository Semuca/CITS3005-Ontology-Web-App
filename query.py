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

# Helper functions
def parse_output_row(row):
    return [value.toPython() for value in row]

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
    print(parse_output_row(row))

# Query for 'What Items have more than 10 procedures written for them?'
query_more_than_10_procedures = """
    SELECT ?item (COUNT(?procedure) AS ?procedureCount)
    WHERE {
        ?item a ifixthat:Item .
        ?procedure ifixthat:guideOf ?item .
    }
    GROUP BY ?item
    HAVING (COUNT(?procedure) > 10)
"""

print("\nQuery for 'What Items have more than 10 procedures written for them?'")
for row in graph.query(query_more_than_10_procedures):
    print(parse_output_row(row))

# Query for 'What procedures include a tool that is never included in its steps?'
query_unmentioned_tools = """
    SELECT ?procedure ?tool
    WHERE {
        ?procedure a ifixthat:Procedure .
        ?procedure ifixthat:requiresTool ?tool .
        FILTER NOT EXISTS {
            ?procedure ifixthat:hasStep ?orderedStep .
            ?orderedStep ifixthat:details ?step .
            ?step ifixthat:usesTool ?tool .
        }
    }
"""

print("\nQuery for 'What procedures include a tool that is never included in its steps?'")
for row in graph.query(query_unmentioned_tools):
    print(parse_output_row(row))

# Query for 'What procedures include the words 'careful' or 'dangerous' in their steps?'
query_careful_or_dangerous = """
    SELECT ?procedure ?step ?actions
    WHERE {
        ?procedure a ifixthat:Procedure .
        ?procedure ifixthat:hasStep ?orderedStep .
        ?orderedStep ifixthat:details ?step .
        ?step ifixthat:actions ?actions .
        FILTER(CONTAINS(?actions, 'careful') || CONTAINS(?actions, 'dangerous'))
    }
"""

print("\nQuery for 'What procedures include the words 'careful' or 'dangerous' in their steps?'")
for row in graph.query(query_careful_or_dangerous):
    print(parse_output_row(row))

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
    print(parse_output_row(row))

