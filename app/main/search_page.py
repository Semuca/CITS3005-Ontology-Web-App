from flask import render_template, request

from .views import main_bp, Link, g

@main_bp.route("/")
def search_page() -> str:
    """The search page"""

    rdf_type = request.args.get('rdf_type', '')
    parsed_rdf_type = f'props:{rdf_type}' if rdf_type else '?type'
    limit = request.args.get('limit', 10)

    # Oooooooh sparql injections can be done here spoooooky
    query = f"""
        SELECT DISTINCT ?entity
        WHERE {{
            ?entity rdf:type {parsed_rdf_type} .
        }}
        LIMIT {limit}
    """

    results = []
    for result in g.query(query):
        result_rdf_type = result[0].split('/')[-2]
        id = result[0].split('/')[-1]
        results.append(Link(result[0], result[0], result_rdf_type, f'/{result_rdf_type.lower()}/{id}'))

    return render_template('search.html', results=results)