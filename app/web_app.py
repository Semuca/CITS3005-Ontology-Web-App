from flask import Flask

from api import api_bp
from main import main_bp

flask_app = Flask(__name__)

flask_app.register_blueprint(api_bp, url_prefix='/api')
flask_app.register_blueprint(main_bp)

flask_app.run("0.0.0.0", port=5000, debug=True)