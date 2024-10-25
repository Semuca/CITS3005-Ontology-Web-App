from flask import render_template
from rdflib import URIRef
from .views import main_bp, Link, ifixthat, shacl_results

@main_bp.route("/Part/<part>")
def part_page(part: str) -> str:
    """The part page"""
    part_instance = ifixthat.search_one(type=ifixthat.Part, iri=f"*{part}")

    uri = URIRef(part_instance.iri)
    errors = list(filter(lambda shacl_result: shacl_result.get('focusNode', None) == uri, shacl_results))

    label = part_instance.label[0]
    items = [Link(item) for item in part_instance.partOf]

    procedures_for_part = ifixthat.search(type=ifixthat.Procedure, guideOf=part_instance)
    procedures = [Link(procedure) for procedure in procedures_for_part]

    return render_template('part.html', errors=errors, uri=part_instance.iri, label=label, items=items, procedures=procedures)
