from flask import render_template
from rdflib import URIRef

from .views import main_bp, Link, ifixthat, shacl_results

@main_bp.route("/Tool/<tool>")
def tool_page(tool: str) -> str:
    """The tool page"""
    tool_instance = ifixthat.search_one(type=ifixthat.Tool, iri=f"*{tool}")

    uri = URIRef(tool_instance.iri)
    errors = list(filter(lambda shacl_result: shacl_result.get('focusNode', None) == uri, shacl_results))

    label = tool_instance.label[0]
    supplier_url = tool_instance.supplierUrl[0] if len(tool_instance.supplierUrl) > 0 else ""

    procedures_requiring_tool = ifixthat.search(type=ifixthat.Procedure, requiresTool=tool_instance)
    procedures = [Link(procedure) for procedure in procedures_requiring_tool]

    images = [Link(has_image, images=has_image.dataUrl, hideContent=True) for has_image in tool_instance.hasImage]

    return render_template('tool.html', errors=errors, uri=tool_instance.iri, label=label, images=images, supplier_url=supplier_url, procedures=procedures)
