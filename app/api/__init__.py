"""This module sets up the api blueprint to be used by the app"""
# By Heidi Leow (23643117) and James Frayne (23372032)

from .bp import api_bp
from . import create, delete, edit

__all__ = ['api_bp', 'create', 'delete', 'edit']
