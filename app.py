from flask import Flask
from flask_cors import CORS
from controllers.programs_controller import programs_controller_bp
from controllers.disciplines_controller import disciplines_controller_bp

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
app.register_blueprint(programs_controller_bp)
app.register_blueprint(disciplines_controller_bp)

if __name__ == "__main__":
    app.run(debug=True)
