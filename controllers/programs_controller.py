import logging
from flask import Blueprint, Flask, request, jsonify
from scrapers.fmi_degrees_scraper import scrape_degrees
from controllers.util.controller_utils import parse_request

programs_controller_bp = Blueprint('programs_controller_bp', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@programs_controller_bp.route('/api/chatbot/programs', methods=['POST'])
def chatbot():
    """Main endpoint for handling chatbot questions."""
    question_data = parse_request(request)
    if not question_data:
        return error_response("Invalid request. Please provide a 'question' field.", 400)

    question = question_data.lower()

    # Define question handlers
    handlers = {
        "какви програми имам?": handle_programs,
    }

    # Match question to handler
    for keyword, handler in handlers.items():
        if keyword in question:
            return handler(question)

    return error_response("Unsupported question.", 400)

def handle_programs(question):
    url = "https://fmi-plovdiv.org/index.jsp?ln=1&id=1384"
    programs = scrape_degrees(url)
    program_names = [program.program_name for program in programs]
    return jsonify({"programs": program_names})

def error_response(message, status_code):
    """Generate a standardized error response."""
    return jsonify({"error": message}), status_code