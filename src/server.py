import json
from flask import Flask, Response, jsonify, request
from .payslip_runner import generate_payslips

app = Flask(__name__, static_folder="static", static_url_path="")


def error_response(message: str, code: int) -> Response:
    """Build an error answer for the web page."""
    response = jsonify(error = message)
    response.status_code = code
    return response


@app.get("/")
def home() -> Response:
    return app.send_static_file("index.html")


@app.post("/api/process")
def process() -> Response:
    try:
        excel_bytes = request.files["excel"].read()
        year = request.form["year"]
        employee_folders = json.loads(request.form["folders"])

        return jsonify(generate_payslips(excel_bytes, employee_folders, year))
    except (KeyError, ValueError) as error:
        return error_response(str(error), 400) # bad request
    except Exception as error:
        app.logger.exception("Processing failed")
        return error_response(str(error), 500) # server error