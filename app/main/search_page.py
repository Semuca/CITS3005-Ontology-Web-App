from flask import render_template
import rdflib

from .views import main_bp, Link

@main_bp.route("/")
def search_page() -> str:
    """The search page"""

    g = rdflib.Graph()
    g.parse("../graph.rdf", format="xml")

    query = """
        SELECT DISTINCT ?step ?actions
        WHERE {
            ?step rdf:type ?type .
            ?step props:actions ?actions .
        }
        LIMIT 10
    """

    results = []
    for ref, actions in g.query(query):
        id = ref.split('/')[-1]
        results.append(Link(ref, actions, 'Step', f'/step/{id}'))

    return render_template('search.html', results=results)