from flask import render_template
import rdflib

from .views import main_bp, domain, Link

@main_bp.route("/tool/<tool>")
def tool_page(tool: str) -> str:
    """The tool page"""

    g = rdflib.Graph()
    g.parse("../graph.rdf", format="xml")

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
        ref = result[0]
        id = ref.split('/')[-1]
        procedures.append(Link(ref, id, 'Procedure', f'/procedure/{id}'))

    return render_template('tool.html', label=label, supplier_url=supplier_url, procedures=procedures)