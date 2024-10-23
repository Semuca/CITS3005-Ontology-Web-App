"""Main route views"""

from flask import Blueprint, render_template
import rdflib

main_bp = Blueprint('main_bp', __name__)

class Link:

    type_to_icon_map = {
        'Item': 'category',
        'Part': 'toys_and_games',
        'Procedure': 'receipt_long',
        'Step': 'stairs_2',
        'Tool': 'construction',
    }

    def __init__(self, name: str, rdf_type: str, url: str) -> None:
        self.name = name
        self.rdf_type = rdf_type
        self.url = url

        self.icon = self.type_to_icon_map.get(rdf_type, 'help')


items = [
    Link('Item 1', 'Item', '/item/1'),
]

parts = [
    Link('Part 1', 'Part', '/part/1'),
]

procedures = [
    Link('Procedure 1', 'Procedure', '/procedure/1'),
]

steps = [
    Link('Step 1', 'Step', '/step/1'),
]

tools = [
    Link('Tool 1', 'Tool', '/tool/1'),
]


domain = "http://ifixthat.org/"
g = rdflib.Graph()
g.parse("../graph.rdf", format="xml")

@main_bp.route("/")
def search_page() -> str:
    """The search page"""

    query = """
        SELECT DISTINCT ?step ?actions
        WHERE {
            ?step rdf:type ?type .
            ?step props:actions ?actions .
        }
        LIMIT 10
    """

    results = []
    for uri, actions in g.query(query):
        id = uri.split('/')[-1]
        results.append(Link(actions, 'Step', f'/step/{id}'))

    return render_template('search.html', results=results)

@main_bp.route("/item/<item>")
def item_page(item: str) -> str:
    """The item page"""

    query = f"""
        SELECT ?procedure
        WHERE {{
            ?procedure props:guideOf <{domain}item/{item}> .
        }}
    """

    procedures = []
    for result in g.query(query):
        uri = result[0]
        id = uri.split('/')[-1]
        procedures.append(Link(id, 'Procedure', f'/procedure/{id}'))

    return render_template('item.html', procedures=procedures)

@main_bp.route("/part/<part>")
def part_page(part: str) -> str:
    """The part page"""

    query = f"""
        SELECT ?procedure
        WHERE {{
            <{domain}part/{part}> props:stepOf ?procedure .
        }}
    """

    procedures = []
    for result in g.query(query):
        uri = result[0]
        id = uri.split('/')[-1]
        procedures.append(Link(id, 'Procedure', f'/procedure/{id}'))

    return render_template('part.html', procedures=procedures)

@main_bp.route("/procedure/<procedure>")
def procedure_page(procedure: str) -> str:
    """The procedure page"""

    uri = f"<{domain}procedure/{procedure}>"

    stepsQuery = f"""
        SELECT ?step
        WHERE {{
            ?step props:stepOf {uri} .
        }}
    """

    steps = []
    for result in g.query(stepsQuery):
        id = result[0].split('/')[-1]
        steps.append(Link(id, 'Step', f'/step/{id}'))

    itemsQuery = f"""
        SELECT ?item
        WHERE {{
            {uri} props:guideOf ?item .
        }}
    """

    items = []
    for result in g.query(itemsQuery):
        id = result[0].split('/')[-1]
        items.append(Link(id, 'Item', f'/item/{id}'))

    partsQuery = f"""
        SELECT ?part
        WHERE {{
            {uri} props:guideOf ?part .
        }}
    """

    parts = []
    for result in g.query(partsQuery):
        id = result[0].split('/')[-1]
        parts.append(Link(id, 'Part', f'/part/{id}'))

    toolsQuery = f"""
        SELECT ?tool
        WHERE {{
            {uri} props:requiresTool ?tool .
        }}
    """

    tools = []
    for result in g.query(toolsQuery):
        id = result[0].split('/')[-1]
        tools.append(Link(id, 'Tool', f'/tool/{id}'))

    return render_template('procedure.html', steps=steps, items=items, parts=parts, tools=tools)

@main_bp.route("/step/<step>")
def step_page(step: str) -> str:
    """The step page"""

    uri = f"<{domain}step/{step}>"

    stepDetails = f"""
        SELECT ?actions
        WHERE {{
            {uri} props:actions ?actions .
        }}
    """

    actions = list(g.query(stepDetails))[0][0]

    procedureQuery = f"""
        SELECT ?procedure
        WHERE {{
            {uri} props:stepOf ?procedure .
        }}
    """

    procedures = []
    for result in g.query(procedureQuery):
        id = result[0].split('/')[-1]
        procedures.append(Link(id, 'Procedure', f'/procedure/{id}'))

    toolQuery = f"""
        SELECT ?tool
        WHERE {{
            {uri} props:usesTool ?tool .
        }}
    """

    tools = []
    for result in g.query(toolQuery):
        id = result[0].split('/')[-1]
        tools.append(Link(id, 'Tool', f'/tool/{id}'))

    return render_template('step.html', actions=actions, procedures=procedures, tools=tools)

@main_bp.route("/tool/<tool>")
def tool_page(tool: str) -> str:
    """The tool page"""

    uri = f"<{domain}tool/{tool}>"

    label = list(g.query(f"""
        SELECT ?label
        WHERE {{
            {uri} rdfs:label ?label .
        }}
    """))[0][0]

    supplier_url = list(g.query(f"""
        SELECT ?supplierUrl
        WHERE {{
            {uri} props:supplierUrl ?supplierUrl .
        }}
    """))[0][0]

    query = f"""
        SELECT ?procedure
        WHERE {{
            ?procedure props:requiresTool {uri} .
        }}
    """

    procedures = []
    for result in g.query(query):
        id = result[0].split('/')[-1]
        procedures.append(Link(id, 'Procedure', f'/procedure/{id}'))

    return render_template('tool.html', label=label, supplier_url=supplier_url, procedures=procedures)
