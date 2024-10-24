from flask import render_template, request

from .views import main_bp, Link, g

@main_bp.route("/")
def search_page() -> str:
    """The search page"""

    rdf_type = request.args.get('rdf_type', '?type')
    search = request.args.get('name', '')
    limit = request.args.get('limit', 20)

    # Oooooooh sparql injections can be done here spoooooky
    query = f"""
        SELECT DISTINCT ?entity ?label
        WHERE {{
            ?entity rdf:type {rdf_type} .
            ?entity rdfs:label ?label .
            FILTER REGEX(?label, "{search}", "i")
        }}
        LIMIT {limit}
    """

    results = []
    for ref, label in g.query(query):
        result_rdf_type = ref.split('/')[-2]
        id = ref.split('/')[-1]
        results.append(Link(ref, label, result_rdf_type, f'/{result_rdf_type.lower()}/{id}'))

    return render_template('search.html', results=results)