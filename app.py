from flask import Flask
from controllers.programs_controller import programs_controller_bp
from controllers.disciplines_controller import disciplines_controller_bp

app = Flask(__name__)
app.register_blueprint(programs_controller_bp)
app.register_blueprint(disciplines_controller_bp)

if __name__ == "__main__":
    app.run(debug=True)
