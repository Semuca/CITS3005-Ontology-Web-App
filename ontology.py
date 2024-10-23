from owlready2 import *
from rdflib import Graph, Namespace

PROPS = Namespace("http://ifixthat.org/properties")

#TODO Load the knowledge graph
# g = Graph()
# g.parse("graph.rdf", format="xml")

# Create the ontology
onto = get_ontology("http://ifixthat.org/onto.owl")

with onto:
    class Procedure(Thing): pass
    class Item(Thing): pass
    class Part(Thing): pass
    class Tool(Thing): pass
    class Step(Thing): pass
    class Image(Thing): pass

    # Procedure schema
    class subProcedureOf(ObjectProperty, TransitiveProperty):
        domain = [Procedure]
        range = [Procedure]

    class requiresTool(ObjectProperty):
        domain = [Procedure]
        range = [Tool]

    class guideOf(ObjectProperty):
        domain = [Procedure]
        range = [Item | Part]

    class hasSteps(ObjectProperty):
        domain = [Procedure]
        range = [Step] # Actually a list of steps

    # Item schema
    class subCategoryOf(ObjectProperty, TransitiveProperty):
        domain = [Item]
        range = [Item]

    # Part schema
    class partOf(ObjectProperty, TransitiveProperty):
        domain = [Part]
        range = [Part | Item]

    # Tool schema
    class hasImage(ObjectProperty):
        domain = [Tool | Step]
        range = [Image]

    class supplierUrl(DataProperty):
        domain = [Tool]
        range = [str]


    # Step schema
    # class hasImage(ObjectProperty): - already defined in Tool schema
    #     domain = [Tool | Step]
    #     range = [Image]

    class usesTool(ObjectProperty):
        domain = [Step]
        range = [Tool]

    class actions(DataProperty):
        domain = [Step]
        range = [str]

    # Image schema
    class dataUrl(DataProperty):
        domain = [Image]
        range = [str]

onto.save("ontology.owl")
