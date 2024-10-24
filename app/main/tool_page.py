from flask import render_template

from .views import main_bp, Link, ifixthat

@main_bp.route("/Tool/<tool>")
def tool_page(tool: str) -> str:
    """The tool page"""
    tool_instance = ifixthat.search_one(type=ifixthat.Tool, iri=f"*{tool}")

    label = tool_instance.label[0]
    supplier_url = tool_instance.supplierUrl[0]

    procedures_requiring_tool = ifixthat.search(type=ifixthat.Procedure, requiresTool=tool_instance)
    procedures = [Link(procedure) for procedure in procedures_requiring_tool]

    images = [Link(has_image, images=has_image.dataUrl, hideContent=True) for has_image in tool_instance.hasImage]

    return render_template('tool.html', label=label, images=images, supplier_url=supplier_url, procedures=procedures)
