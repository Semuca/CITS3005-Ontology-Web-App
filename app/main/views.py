"""Main route views"""

from flask import Blueprint, render_template

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/")
def search_page():
    """The search page"""

    return render_template('search.html', results=['test1', 'test2'])

