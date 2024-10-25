from flask import render_template, redirect
from rdflib import URIRef

from .links import Link
from .views import main_bp, ifixthat

@main_bp.route("/Part/<part>")
def part_page(part: str) -> str:
    """The part page"""
    from main.views import shacl_results

    part_instance = ifixthat.search_one(type=ifixthat.Part, iri=f"*#{part}")
    if part_instance is None:
        return redirect('/')

    uri = URIRef(part_instance.iri)
    errors = list(filter(lambda shacl_result: shacl_result.get('focusNode', None) == uri, shacl_results))

    label = part_instance.label[0]
    items = [Link(item, 'http://ifixthat.org/partOf', parent_uri=part_instance.iri) for item in part_instance.partOf]

    procedures_for_part = ifixthat.search(type=ifixthat.Procedure, guideOf=part_instance)
    procedures = [Link(procedure, 'http://ifixthat.org/guideOf', child_uri=part_instance.iri) for procedure in procedures_for_part]

    return render_template('part.html', errors=errors, uri=part_instance.iri, label=label, items=items, procedures=procedures)
