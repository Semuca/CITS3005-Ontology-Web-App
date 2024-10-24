from flask import render_template
from .views import main_bp, Link, ifixthat

@main_bp.route("/Item/<item>")
def item_page(item: str) -> str:
    """The item page"""
    item_instance = ifixthat.search_one(type=ifixthat.Item, iri=f"*{item}")

    label = item_instance.label[0]
    parents = [Link(parent) for parent in item_instance.subCategoryOf]

    children_of_item = ifixthat.search(type=ifixthat.Item, subCategoryOf=item_instance)
    children = [Link(child) for child in children_of_item]

    parts_of_item = ifixthat.search(type=ifixthat.Part, partOf=item_instance)
    parts = [Link(part) for part in parts_of_item]

    procedures_for_item = ifixthat.search(type=ifixthat.Procedure, guideOf=item_instance)
    procedures = [Link(procedure) for procedure in procedures_for_item]

    return render_template('item.html', label=label, categoryParents=parents, categoryChildren=children, parts=parts, procedures=procedures)
