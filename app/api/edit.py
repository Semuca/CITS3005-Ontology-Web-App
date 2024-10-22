"""Defines endpoint for creating entries"""

from .bp import api_bp

@api_bp.route('/', methods=['PATCH'])
def edit_entry():
    """Edit an entry"""
    return 'Entry edited', 200