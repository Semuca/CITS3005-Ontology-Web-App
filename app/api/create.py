"""Defines endpoint for creating entries"""

from .bp import api_bp

@api_bp.route('/', methods=['POST'])
def create_entry():
    """Create an entry"""
    return 'Entry created', 201