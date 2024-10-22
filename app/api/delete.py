"""Defines endpoint for creating entries"""

from .bp import api_bp

@api_bp.route('/', methods=['DELETE'])
def delete_entry():
    """Delete an entry"""
    return 'Entry deleted', 200