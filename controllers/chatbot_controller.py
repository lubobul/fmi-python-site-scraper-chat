import logging
from typing import List

from flask import Blueprint, Flask, request, jsonify
from datetime import datetime
from controllers.util.controller_utils import parse_request
from models.models import ProgramLinkModel
from scrapers.fmi_specialization_scraper import scrape_specializations
from scrapers import fmi_discipline_scraper
import os
import logging

url = "https://fmi-plovdiv.org/index.jsp?ln=1&id=1384"
specializations = scrape_specializations(url)

chatbot_controller_bp = Blueprint('chatbot_controller_bp', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

selected_specialization_name = None


def load_disciplines(url):
    """Load and scrape disciplines from the given website URL."""
    return fmi_discipline_scraper.scrape_disciplines(url)


# Initialize the global data store
disciplines_data = load_disciplines("https://fmi-plovdiv.org/index.jsp?id=4789&ln=1")


# @chatbot_controller_bp.route('/api/help', methods=['GET'])
def help_info(question):
    """Endpoint that returns the content of the help_info.txt file."""
    try:
        # Determine the absolute path to help_info.txt
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'help_info.txt')

        # Open and read the content of help_info.txt
        with open(file_path, 'r', encoding='utf-8') as file:
            help_content = file.read()

        return jsonify({"message": help_content})
    except FileNotFoundError:
        logging.error("help_info.txt file not found.")
        return jsonify({"message": "Help information file not found."}), 404
    except Exception as e:
        logging.error(f"Error reading help_info.txt: {e}")
        return jsonify({"message": "Failed to retrieve help information."}), 500


@chatbot_controller_bp.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Main endpoint for handling chatbot questions."""
    question_data = parse_request(request)
    if not question_data:
        return error_response("Invalid request. Please provide a 'question' field.", 400)

    # if not disciplines_data:
    #     return error_response("За да продължите с тези въпроси, първо изберете програма, като попитате - какви програми имам?", 400)

    question = question_data.lower()

    # Define question handlers
    handlers = {
        "какви специалности има?": handle_specializations,
        "какви програми имам за специалност": handle_programs_for_specialization,
        "какви дисциплини имам за програма": handle_disciplines_list,
        "кой преподава дисциплината": handle_discipline_lecturers,
        "по кои дисциплини преподава": handle_lecturer_disciplines,
        "следващият час": handle_next_session,
        "/помощ": help_info
    }

    # Match question to handler
    for keyword, handler in handlers.items():
        if keyword in question:
            return handler(question)

    # Check for session type-specific queries
    if any(keyword in question for keyword in ["лекции", "лабораторни", "изпит", "поправка"]):
        return handle_session_query(question)

    return error_response("Не разбирам въпроса, за повече информация изберете /помощ", 404)


# Helper functions

def error_response(message, status_code):
    """Generate a standardized error response."""
    return jsonify({"message": message}), status_code


def handle_disciplines_list(question):
    """Handle 'какви дисциплини имам?' question."""
    global disciplines_data
    program_name = question.replace("какви дисциплини имам за програма", "").strip(" '?")
    program_name = program_name.capitalize()  # Capitalize the first letter of the discipline name

    selected_programs_for_specialization = get_programs_for_specialization_by_name(selected_specialization_name)
    program_link = get_program_link_by_program_name(program_name, selected_programs_for_specialization)

    program_url = "https://fmi-plovdiv.org/" + program_link.replace("../", "");
    disciplines_data = load_disciplines(program_url)
    discipline_names = [discipline.disciplineName for discipline in disciplines_data]
    return jsonify({
        "message": f"Дисциплините, които имате за програма {program_name} са:",
        "items": discipline_names
    })


def handle_discipline_lecturers(question):
    """Handle 'кой преподава дисциплината' question."""
    discipline_name = question.replace("кой преподава дисциплината", "").strip(" '?")
    discipline_name = discipline_name.capitalize()  # Capitalize the first letter of the discipline name

    lecturers = get_discipline_lecturers(discipline_name)

    # Check if lecturers list contains only empty strings
    if not lecturers or all(lecturer == '' for lecturer in lecturers):
        return error_response(f"Дисциплината '{discipline_name}' няма преподаватели или не беше намерена.", 404)

    readable_list = ", ".join(lecturers)
    return jsonify(
        {
            "message": f"По '{discipline_name}' преподават:",
            "items": lecturers
        })


def handle_lecturer_disciplines(question):
    """Handle 'по кои дисциплини преподава' question."""
    lecturer_name = question.replace("по кои дисциплини преподава", "").strip(" ?")
    lecturer_name = lecturer_name.capitalize()  # Capitalize the first letter of the lecturer's name

    matching_disciplines = get_disciplines_by_lecturer(lecturer_name)
    if matching_disciplines:
        return jsonify({
            "message": f"Преподавателят води следните дисциплини:",
            "items": matching_disciplines
        })

    return error_response(f"Не бяха намерени дисциплини за преподавател '{lecturer_name}'.", 404)


def handle_session_query(question):
    """Handle queries about specific session types (лекции, лабораторни, изпит, поправка)."""
    session_type = get_session_type(question)
    if not session_type:
        return error_response("Unsupported session type.", 400)

    discipline_name = question.replace(f"кога имам {session_type} по", "").strip(" '?")
    sessions = get_sessions_for_discipline(discipline_name, session_type)
    if sessions:
        session_info = sessions[0]  # Assume we are interested in the first session for simplicity

        # Check if the cabinet is empty and set to '457' if so
        cabinet = session_info.get('cabinet', '').strip()
        if not cabinet:
            cabinet = '457'

        # Check if the lecturer is empty or only spaces
        lecturer = session_info.get('lecturer', '').strip()
        if lecturer:
            return jsonify({
                "message": f"Имаш {session_type} по {discipline_name.capitalize()} на {session_info['time']} в кабинет {cabinet} с {lecturer.capitalize()}."
            })
        else:
            return jsonify({
                "message": f"Имаш {session_type} по {discipline_name.capitalize()} на {session_info['time']} в кабинет {cabinet}."
            })

    return error_response(f"Дисциплината '{discipline_name}' не беше намерена или няма {session_type} часове.", 404)


def handle_next_session(question):
    """Handle queries about the next university session."""
    next_session = get_next_session()
    if next_session:
        # Check if the cabinet is empty, contains only spaces, or is None
        cabinet = next_session.get('cabinet', '').strip()
        if not cabinet:
            cabinet = '547 к.з.'  # Replace with the default cabinet value

        return jsonify({"message": f"Следващият час е на: {next_session['time']} по дисциплината {next_session['discipline']} в кабинет {cabinet}"})
    return error_response("Не бяха намерени предстоящи часове.", 404)


def handle_specializations(question):
    specialization_names = [specialization.specialization_name for specialization in specializations]
    return jsonify(
        {
            "message": "Вашите специалности са:",
            "items": specialization_names
        }
    )


def handle_programs_for_specialization(question):
    """Handle 'какви курсове имам за' question."""
    global selected_specialization_name

    specialization_name = question.replace("какви програми имам за специалност", "").strip(" '?")

    selected_specialization_name = specialization_name

    programs = get_programs_for_specialization_by_name(specialization_name)
    program_titles = [program.program_name for program in programs]

    return jsonify(
        {
            "message": f"Вашите прoграми за специалност {specialization_name} са:",
            "items": program_titles
        }
    )


def get_programs_for_specialization_by_name(specialization_name):
    for specialization in specializations:
        if specialization_name.lower() in specialization.specialization_name.lower():
            return specialization.programs
    return []


def get_program_link_by_program_name(program_name, programs: List[ProgramLinkModel]):
    for program in programs:
        if program_name.lower() in program.program_name.lower():
            if program.summer_link:
                return program.summer_link
            else:
                return program.winter_link
    return None


def get_discipline_lecturers(discipline_name):
    """Retrieve lecturers for a specific discipline."""
    lecturers = []
    for discipline in disciplines_data:
        if discipline.disciplineName.lower() == discipline_name.lower():
            lecturers.extend(variant.lecturer for variant in discipline.disciplineList)
    return list(set(lecturers))


def get_disciplines_by_lecturer(lecturer_name):
    """Retrieve disciplines taught by a specific lecturer."""
    lecturer_name_lower = lecturer_name.lower()
    matching_disciplines = set()
    for discipline in disciplines_data:
        for variant in discipline.disciplineList:
            if lecturer_name_lower in variant.lecturer.lower():
                matching_disciplines.add(discipline.disciplineName)
    return list(matching_disciplines)


def get_session_type(question):
    """Determine session type from the question."""
    for session_type in ["лекции", "лабораторни", "изпит", "поправка"]:
        if session_type in question:
            return session_type
    return None


def get_sessions_for_discipline(discipline_name, session_type):
    """Retrieve sessions for a specific discipline and type."""
    sessions = []
    for discipline in disciplines_data:
        if discipline.disciplineName.lower() == discipline_name.lower():
            sessions.extend(
                {
                    "discipline": discipline.disciplineName,
                    "time": variant.time,
                    "lecturer": variant.lecturer,
                    "cabinet": variant.cabinetNumber
                }
                for variant in discipline.disciplineList
                if variant.type.lower() == session_type
            )
    return sessions


def get_next_session():
    """Find the next upcoming session."""
    now = datetime.now()
    next_session = None
    for discipline in disciplines_data:
        for variant in discipline.disciplineList:
            try:
                session_date = datetime.strptime(variant.time.split(",")[0].strip()[:10], "%d.%m.%Y")
                if session_date > now and (
                        not next_session or session_date < datetime.strptime(next_session['time'], "%d.%m.%Y")):
                    next_session = {
                        "discipline": discipline.disciplineName,
                        "time": session_date.strftime("%d.%m.%Y"),
                        "lecturer": variant.lecturer,
                        "cabinet": variant.cabinetNumber
                    }
            except ValueError:
                logging.error(f"Invalid date format: {variant.time}")
                continue
    return next_session
