from owlready2 import *
from rdflib import Graph, Namespace

PROPS = Namespace("http://iFixthat.org/properties")

#TODO Load the knowledge graph
# myFixit = Graph()
# myFixit.parse("data.rdf", format="xml")

# Create the ontology
onto = get_ontology("http://iFixthat.org/onto.owl")

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

    #TODO: hasSteps

    class requiresTool(ObjectProperty):
        domain = [Procedure]
        range = [Tool]
    class hasImage(ObjectProperty):
        domain = [Procedure | Tool | Step]
        range = [Image]

    class procedureOf(ObjectProperty):
        domain = [Procedure]
        range = [Item]
    class difficulty(DataProperty, FunctionalProperty):
        domain = [Procedure]
        range = [str]
    #TODO: timeEstimate
    class introduction(DataProperty):
        domain = [Procedure]
        range = [str]
    class conclusion(DataProperty):
        domain = [Procedure]
        range = [str]

    # Item schema
    class subItemOf(ObjectProperty, TransitiveProperty):
        domain = [Item]
        range = [Item]

    # Part schema
    class partOf(ObjectProperty, TransitiveProperty):
        domain = [Part]
        range = [Part | Item]

    # Tool schema
    # class hasImage(ObjectProperty): - Defined in Procedure schema
    #     domain = [Procedure | Tool | Step]
    #     range = [Image]

    # Step schema
    #TODO: hasActions
    # class hasImage(ObjectProperty): - Defined in Procedure schema
    #     domain = [Procedure | Tool | Step]
    #     range = [Image]

    # Image schema
    class dataUrl(DataProperty):
        domain = [Image]
        range = [str]

onto.save("ontology.owl")
