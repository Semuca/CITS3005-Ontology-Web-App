from flask import render_template
from .views import main_bp, Link, domain, g

@main_bp.route("/item/<item>")
def item_page(item: str) -> str:
    """The item page"""

    uri = f"<{domain}item/{item}>"

    label = list(g.query(f"""
        SELECT ?label
        WHERE {{
            {uri} rdfs:label ?label .
        }}
    """))[0][0]

    categoryParentsQuery = f"""
        SELECT ?category ?label
        WHERE {{
            {uri} props:subCategoryOf ?category .
            ?category rdfs:label ?label .
        }}
    """

    categoryParents = []
    for ref, category_label in g.query(categoryParentsQuery):
        categoryParents.append(Link(ref, title=category_label))

    categoryChildrenQuery = f"""
        SELECT ?subCategory ?label
        WHERE {{
            ?subCategory props:subCategoryOf {uri} .
            ?subCategory rdfs:label ?label .
        }}
    """

    categoryChildren = []
    for ref, subCategory_label in g.query(categoryChildrenQuery):
        categoryChildren.append(Link(ref, title=subCategory_label))

    partsQuery = f"""
        SELECT ?part ?label
        WHERE {{
            ?part props:partOf {uri} .
            ?part rdfs:label ?label .
        }}
    """

    parts = []
    for ref, part_label in g.query(partsQuery):
        parts.append(Link(ref, title=part_label))

    proceduresQuery = f"""
        SELECT ?procedure ?label
        WHERE {{
            ?procedure props:guideOf {uri} .
            ?procedure rdfs:label ?label .
        }}
    """

    procedures = []
    for ref, procedure_label in g.query(proceduresQuery):
        procedures.append(Link(ref, title=procedure_label))

    return render_template('item.html', label=label, categoryParents=categoryParents, categoryChildren=categoryChildren, parts=parts, procedures=procedures)