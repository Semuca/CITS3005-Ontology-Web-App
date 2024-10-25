"""Sets up the api blueprint to be used by the app, avoiding circular imports"""
# By Heidi Leow (23643117) and James Frayne (23372032)

from flask import Blueprint

api_bp = Blueprint('api_bp', __name__)