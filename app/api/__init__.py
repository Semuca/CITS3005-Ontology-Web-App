"""This module sets up the api blueprint to be used by the app"""

from .bp import api_bp
from . import create, delete, edit

__all__ = ['api_bp', 'create', 'delete', 'edit']
