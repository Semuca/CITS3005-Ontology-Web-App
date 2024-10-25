from flask import render_template, redirect
from rdflib import URIRef

from .links import Link
from .views import main_bp, ifixthat

@main_bp.route("/Item/<item>")
def item_page(item: str) -> str:
    """The item page"""
    from main.views import shacl_results

    item_instance = ifixthat.search_one(type=ifixthat.Item, iri=f"*#{item}")
    if item_instance is None:
        return redirect('/')

    uri = URIRef(item_instance.iri)
    errors = list(filter(lambda shacl_result: shacl_result.get('focusNode', None) == uri, shacl_results))

    label = item_instance.label[0]
    parents = [Link(parent, 'http://ifixthat.org/subCategoryOf', parent_uri=item_instance.iri) for parent in item_instance.subCategoryOf]

    children_of_item = ifixthat.search(type=ifixthat.Item, subCategoryOf=item_instance)
    children = [Link(child, 'http://ifixthat.org/subCategoryOf', child_uri=item_instance.iri) for child in children_of_item]

    parts_of_item = ifixthat.search(type=ifixthat.Part, partOf=item_instance)
    parts = [Link(part, 'http://ifixthat.org/partOf', child_uri=item_instance.iri) for part in parts_of_item]

    procedures_for_item = ifixthat.search(type=ifixthat.Procedure, guideOf=item_instance)
    procedures = [Link(procedure, 'http://ifixthat.org/guideOf', child_uri=item_instance.iri) for procedure in procedures_for_item]

    return render_template('item.html', errors=errors, uri=item_instance.iri, label=label, categoryParents=parents, categoryChildren=children, parts=parts, procedures=procedures)
