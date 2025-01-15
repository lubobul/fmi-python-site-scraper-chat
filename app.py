from flask import Flask
from flask_cors import CORS
from controllers.chatbot_controller import chatbot_controller_bp

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
app.register_blueprint(chatbot_controller_bp)

if __name__ == "__main__":
    app.run(debug=True)
