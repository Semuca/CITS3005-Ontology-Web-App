from owlready2 import *

# Create the ontology
onto = get_ontology("http://example.org/ifixit_ontology.owl")

with onto:
    class Procedure(Thing): pass
    class Item(Thing): pass
    class Part(Item): pass
    class Part(Thing): pass
    class Tool(Thing): pass
    class Step(Thing): pass
    class Image(Thing): pass

    class part_of(Item >> Item, TransitiveProperty): pass
    class uses_tool(Step >> Tool): pass
    class has_toolbox(Procedure >> Tool): pass
    class has_step(Procedure >> Step): pass
    class sub_procedure_of(Procedure >> Procedure): pass
    class has_image(Step >> Image): pass

onto.save("ifixit_ontology.owl")