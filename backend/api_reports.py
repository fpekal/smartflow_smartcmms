from flask import Blueprint, jsonify, render_template, abort, request

api_reports = Blueprint('api_reports', __name__, url_prefix='/reports')

REPORT_TYPES = [
    {
        "id": "test_form",
        "name": "Raport testowy",
        "template": "form.html.jinja"
    }
    # Kolejne raporty dodajemy w formacie:
    # {"id": "twoj_raport", "name": "Nazwa raportu", "template": "twoj_raport.html.jinja"}
]

@api_reports.route('/', methods=['GET'])
def list_reports():
    payload = [
        {"id": rpt['id'], "name": rpt['name']} for rpt in REPORT_TYPES
    ]
    return jsonify(payload), 200

@api_reports.route('/<report_id>', methods=['GET'])
def get_report(report_id):
    rpt = next((r for r in REPORT_TYPES if r['id'] == report_id), None)
    if not rpt:
        abort(404, description=f"Raport '{report_id}' nie istnieje.")

    data = {
        "title": rpt['name'],
        "items": [
            {"field1": "Przykład 1", "field2": "Wartość 1"},
            {"field1": "Przykład 2", "field2": "Wartość 2"},
        ]
    }

    html = render_template(rpt['template'], data=data)

    return jsonify({
        "id": rpt['id'],
        "name": rpt['name'],
        "html": html
    }), 200
