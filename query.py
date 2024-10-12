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

# Query for 'What items have 10 or more guides written for them?'
queryTenOrMoreGuides = """
    SELECT ?category (COUNT(?guide) AS ?guideCount)
    WHERE {
        ?category rdf:type ifixit:category .
        ?guide ifixit:guideOf ?category .
    }
    GROUP BY ?category
    HAVING (COUNT(?guide) >= 10)
"""

print("\nQuery for 'What items have 10 or more guides written for them?'")
for row in g.query(queryTenOrMoreGuides):
    print(row)

# Query for 'What procedures include a tool that is never mentioned in the procedure steps?'
queryUnmentionedTools = """
    SELECT ?guide
    WHERE {
        ?guide rdf:type ifixit:guide .
        ?tool rdf:type ifixit:tool .
    
        MINUS {
            ?tool ifixit:toolOf ?guide .
        }

        ?step ifixit:stepOf ?guide .
        ?line ifixit:lineOf ?step .
        ?line ifixit:rawText ?rawText .

        FILTER(CONTAINS(?rawText, STR(?tool)))
    }
"""

print("\nQuery for 'What procedures include a tool that is never mentioned in the procedure steps?'")
for row in g.query(queryUnmentionedTools):
    print(row)