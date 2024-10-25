from owlready2 import get_ontology, default_world

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

# Query for 'What are the Items that are second-level in the hierarchy of Items?'
query_top_level_items = """
    SELECT ?item ?label
    WHERE {
        ?topItem a ifixthat:Item .
        FILTER NOT EXISTS {
            ?topItem ifixthat:subCategoryOf ?parentItem .
        }

        ?item ifixthat:subCategoryOf ?topItem ;
            rdfs:label ?label .
    }
"""

print("\nQuery for 'What are the top level Items?'")
for row in graph.query(query_top_level_items):
    print(parse_output_row(row))

# Query for 'What are all the properties and their values for Procedure 1562?'
query_procedure_properties = """
    SELECT ?property ?value
    WHERE {
        procedure:1562 ?property ?value .
    }
"""

print("\nQuery for 'What are all the properties and their values for Procedure 1562?'")
for row in graph.query(query_procedure_properties):
    print(parse_output_row(row))

# Query for 'What are all the properties and their values for Step 18938?'
query_step_properties = """
    SELECT ?property ?value
    WHERE {
        step:18938 ?property ?value .
    }
"""

print("\nQuery for 'What are all the properties and their values for Step 18938?'")
for row in graph.query(query_step_properties):
    print(parse_output_row(row))

# Query for 'What are the Steps that have more than 2 distinct index in their corresponding Procedures?'
query_multi_index_steps = """
    SELECT ?step (COUNT(DISTINCT ?order) AS ?distinctOrders)
    WHERE {
        ?step rdf:type ifixthat:Step .
        ?orderedStep ifixthat:details ?step .
        ?orderedStep ifixthat:order ?order .
    }
    GROUP BY ?step
    HAVING (COUNT(DISTINCT ?order) > 2)
    ORDER BY DESC(?distinctOrders)
"""

print("\nQuery for 'What are the Steps that have more than 1 distinct index in their corresponding Procedures?'")
for row in graph.query(query_multi_index_steps):
    print(parse_output_row(row))

# Query for 'What are all the tools used in Procedures that are related to the Item and parts of 'Game Boy Pocket'?'
query_tools_for_item = """
    SELECT DISTINCT ?tool ?label
    WHERE {
        ?gameboy a ifixthat:Item ;
                rdfs:label "Game Boy Pocket" .

        ?part ifixthat:partOf+ ?gameboy .
        {
            ?procedure ifixthat:guideOf ?gameboy .
        }
        UNION
        {
            ?procedure ifixthat:guideOf ?part .
        }
        ?procedure ifixthat:requiresTool ?tool .
        ?tool rdfs:label ?label .
    }
"""

print("\nQuery for 'What are all the tools used in Procedures that are related to the Item and parts of 'Game Boy Pocket'?'")
for row in graph.query(query_tools_for_item):
    print(parse_output_row(row))

# Query for 'What images are used in more than 1 Tool or Part?'
query_images_for_tools_and_parts = """
    SELECT ?image ?url (COUNT(DISTINCT ?toolOrPart) AS ?usageCount)
    WHERE {
        ?toolOrPart ifixthat:hasImage ?image .
        ?toolOrPart a ?type .

        ?image ifixthat:dataUrl ?url .
    }
    GROUP BY ?image
    HAVING (COUNT(DISTINCT ?toolOrPart) > 1)
"""

print("\nQuery for 'What images are used in more than 1 Tool or Part?'")
for row in graph.query(query_images_for_tools_and_parts):
    print(parse_output_row(row))
