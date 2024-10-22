"""Main route views"""

from flask import Blueprint, render_template

main_bp = Blueprint('main_bp', __name__)

class Link:

    type_to_icon_map = {
        'Item': 'category',
        'Part': 'toys_and_games',
        'Procedure': 'receipt_long',
        'Step': 'stairs_2',
        'Tool': 'construction',
    }

    def __init__(self, name: str, rdf_type: str, url: str) -> None:
        self.name = name
        self.rdf_type = rdf_type
        self.url = url

        self.icon = self.type_to_icon_map.get(rdf_type, 'help')


items = [
    Link('Item 1', 'Item', '/item/1'),
]

parts = [
    Link('Part 1', 'Part', '/part/1'),
]

procedures = [
    Link('Procedure 1', 'Procedure', '/procedure/1'),
]

steps = [
    Link('Step 1', 'Step', '/step/1'),
]

tools = [
    Link('Tool 1', 'Tool', '/tool/1'),
]

@main_bp.route("/")
def search_page() -> str:
    """The search page"""

    return render_template('search.html', results=items+parts+procedures+steps+tools)

@main_bp.route("/item/<item>")
def item_page(item: str) -> str:
    """The item page"""

    return render_template('item.html', procedures=procedures)

@main_bp.route("/part/<part>")
def part_page(part: str) -> str:
    """The part page"""

    return render_template('part.html', procedures=procedures)

@main_bp.route("/procedure/<procedure>")
def procedure_page(procedure: str) -> str:
    """The procedure page"""

    return render_template('procedure.html', steps=steps, items=items, parts=parts, tools=tools)

@main_bp.route("/step/<step>")
def step_page(step: str) -> str:
    """The step page"""

    return render_template('step.html', procedures=procedures)

@main_bp.route("/tool/<tool>")
def tool_page(tool: str) -> str:
    """The tool page"""

    return render_template('tool.html', procedures=procedures)
