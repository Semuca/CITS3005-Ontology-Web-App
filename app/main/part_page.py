from flask import render_template
from .views import main_bp, Link, ifixthat

@main_bp.route("/Part/<part>")
def part_page(part: str) -> str:
    """The part page"""
    part_instance = ifixthat.search_one(type=ifixthat.Part, iri=f"*{part}")

    label = part_instance.label[0]
    items = [Link(item) for item in part_instance.partOf]

    procedures_for_part = ifixthat.search(type=ifixthat.Procedure, guideOf=part_instance)
    procedures = [Link(procedure) for procedure in procedures_for_part]

    return render_template('part.html', label=label, items=items, procedures=procedures)
