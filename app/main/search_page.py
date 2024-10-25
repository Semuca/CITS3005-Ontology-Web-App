from flask import render_template, request

from .views import main_bp, Link
from owlready2 import default_world

@main_bp.route("/")
def search_page() -> str:
    """The search page"""

    # Parameters
    rdf_type = request.args.get('rdf_type', '?type')
    search = request.args.get('name', '')

    pageSize = int(request.args.get('pageSize', 20))
    page = int(request.args.get('page', 1))

    # Query
    query = f"""
        PREFIX ifixthat: <http://ifixthat.org/>
        SELECT DISTINCT ?entity
        WHERE {{
            ?entity rdf:type {rdf_type} .
            ?entity rdfs:label ?label .
            FILTER REGEX(?label, "{search}", "i")
        }}
        LIMIT {pageSize} OFFSET {(page - 1) * pageSize}
    """

    results = []
    for row in default_world.sparql(query):
        results.append(Link(row[0], None))

    return render_template('search.html', results=results)

