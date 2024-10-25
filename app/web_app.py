from flask import Flask

from api import api_bp
from main.views import main_bp, run_reasoner, convert_onto_to_rdf

RUN_REASONER = True

if (RUN_REASONER):
    run_reasoner()
else:
    convert_onto_to_rdf()

flask_app = Flask(__name__)

flask_app.register_blueprint(api_bp, url_prefix='/api')
flask_app.register_blueprint(main_bp)

flask_app.run("0.0.0.0", port=5000)