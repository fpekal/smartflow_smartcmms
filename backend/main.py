#!/usr/bin/env python3
from flask import Flask, render_template, abort, send_file, request, redirect, \
    url_for, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
import tempfile
import os
import subprocess
import time
import sys
import uuid
import psycopg2
import psycopg2.extras
from datetime import datetime
from api_reports import api_reports
from email_send import send_email


app = Flask(__name__)
CORS(app)

IDC = os.environ.get('IN_DOCKER_CONTAINER')
IDC_cond = False if IDC is None else IDC == "1"

DB_PARAMS = {
    'dbname': os.environ.get('POSTGRES_DB', 'test'),
    'user': os.environ.get('POSTGRES_USER', 'test'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'test'),
    'host': 'db' if IDC_cond else 'localhost'
}

CURRENT_USER_ID = 1

def get_db_connection():
    conn = psycopg2.connect(**DB_PARAMS)
    return conn


def dict_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def init_db():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
    	id int NOT NULL,
    	name varchar(128) NOT NULL,
    	surname varchar(128) NOT NULL,
    	email varchar(128) NOT NULL,
    	hashed_pass varchar(64) NOT NULL,
    	role int NOT NULL, -- bit 0 - osoba zewnętrzna, bit 1 - technik, bit 2 - kierownik budynku, bit 3 - administrator
    	state int NOT NULL, -- bit 0 - czy konto jest usunięte (fałsz - aktywne, prawda - usunięte)
    
    	PRIMARY KEY (id)
    );
    
    CREATE TABLE IF NOT EXISTS users_change (
    	id int NOT NULL,
    	user_id int NOT NULL,
    	new_role int, -- Nowa wartość, która będzie wpisana w pole `role` w tabeli `users`; NULL jeżeli bez zmian
    	new_state int, -- Nowa wartość, która będzie wpisana w pole `state` w tabeli `users`; NULL jeżeli bez zmian
    	commit_date date NOT NULL, -- Kiedy ta zmiana powinna zostać wdrożona do systemu
    
    	FOREIGN KEY (user_id) REFERENCES users(id),
    	PRIMARY KEY (id)
    );
    
    CREATE TABLE IF NOT EXISTS protocols (
    	id varchar(16) NOT NULL, -- np. 1.1.1 4.2.5
    	name varchar(256) NOT NULL,
    	author_id int NOT NULL, -- Osoba, która utworzyła dany protokół
    	state int NOT NULL, -- bit 0 - czy protokół jest obowiązujący (prawda - obowiązuje; fałsz - nieobowiązuje)
    	fields json NOT NULL, -- edytowalne pola w protokole zapisane jako json
    
    	FOREIGN KEY (author_id) REFERENCES users(id),
    	PRIMARY KEY (id)
    );
    
    CREATE TABLE IF NOT EXISTS protocols_change (
    	id int NOT NULL,
    	protocol_id varchar(16) NOT NULL,
    	new_state int, -- Nowa wartość, która będzie wpisana w pole `state` w tabeli `protocols`; NULL jeżeli bez zmian
    	commit_date date NOT NULL, -- Kiedy ta zmiana powinna zostać wdrożona do systemu
    
    	FOREIGN KEY (protocol_id) REFERENCES protocols(id),
    	PRIMARY KEY (id)
    );
    
    CREATE TABLE IF NOT EXISTS protocols_filled ( -- Protokoły wypełniane/wypełnione przez technika
    	id int NOT NULL,
    	protocol_id varchar(16) NOT NULL,
    	user_id int NOT NULL, -- osoba, która wypełniła protokół
    	state int NOT NULL, -- bit 0 - czy w pełni wypełniony, bit 1 - czy podpisany przez technika, bit 2 - czy podpisany przez odbiorcę
    
    	fields json NOT NULL, -- wypełnione pola, razem z notatkami
    
    	FOREIGN KEY (protocol_id) REFERENCES protocols(id),
    	FOREIGN KEY (user_id) REFERENCES users(id),
    	PRIMARY KEY (id)
    );
    
    CREATE TABLE IF NOT EXISTS protocol_sign (
    	id int NOT NULL,
    	protocol_filled_id int NOT NULL,
    
    	-- TODO: Jakieś dodatkowe dane o podpisie
    
    	FOREIGN KEY (protocol_filled_id) REFERENCES protocols_filled(id),
    	PRIMARY KEY (id)
    );
    
    CREATE TABLE IF NOT EXISTS schedules (
    	id int NOT NULL,
    	protocol_id varchar(16) NOT NULL,
    	user_id int NOT NULL, -- Technik, któremu wyświetli się powiadomienie, że musi wypełnić nowy protokół
    	week_interval int NOT NULL, -- Co ile tygodni będzie trzeba wypełnić ten protokół
    	next date NOT NULL, -- Data następnego cyklicznego wypełniania protokołu
    
    	FOREIGN KEY (protocol_id) REFERENCES protocols(id),
    	FOREIGN KEY (user_id) REFERENCES users(id),
    	PRIMARY KEY (id)
    );
    """)
    
    cur.execute("SELECT COUNT(*) FROM protocols")
    count = cur.fetchone()[0]
    
    if count == 0:
        cur.execute("""
            INSERT INTO users (id, name, surname, email, hashed_pass, role, state) 
            VALUES (1, 'Admin', 'User', 'admin@example.com', 'dummy_hash', 7, 0)
            ON CONFLICT DO NOTHING
        """)
        
        example_activities = json.dumps([
            "Sprawdzenie stanu kadłuba i nadbudówki.",
            "Ocena stanu instalacji elektrycznej i hydraulicznej.",
            "Kontrola poziomu paliwa, oleju i innych płynów eksploatacyjnych.",
            "Uruchomienie systemów pomiarowych i sprawdzenie poprawności odczytów.",
            "Test działania systemów awaryjnych i alarmowych.",
            "Sprawdzenie czasu reakcji systemów automatycznych.",
            "Ocena stanu zasilania awaryjnego (baterie, agregaty).",
            "Sprawdzenie stanu i kalibracja urządzeń meteorologicznych (np. anemometr, barometr, radar pogodowy).",
            "Kontrola uszczelek, połączeń i pokryw zabezpieczających.",
            "Inspekcja filtrów powietrza, wody i elementów systemu chłodzenia.",
            "Sprawdzenie stanu kadłuba i nadbudówki.",
            "Ocena stanu instalacji elektrycznej i hydraulicznej.",
            "Kontrola poziomu paliwa, oleju i innych płynów eksploatacyjnych.",
            "Uruchomienie systemów pomiarowych i sprawdzenie poprawności odczytów.",
            "Test działania systemów awaryjnych i alarmowych.",
            "Sprawdzenie czasu reakcji systemów automatycznych.",
            "Ocena stanu zasilania awaryjnego (baterie, agregaty).",
            "Sprawdzenie stanu i kalibracja urządzeń meteorologicznych (np. anemometr, barometr, radar pogodowy).",
            "Kontrola uszczelek, połączeń i pokryw zabezpieczających.",
            "Inspekcja filtrów powietrza, wody i elementów systemu chłodzenia."
        ])
        
        fields_json = json.dumps({
            "activities": json.loads(example_activities)
        })
        
        cur.execute("""
            INSERT INTO protocols (id, name, author_id, state, fields)
            VALUES ('1', '1 Przegląd statku meteorologicznego v1', 1, 1, %s)
            ON CONFLICT DO NOTHING
        """, (fields_json,))
    
    conn.commit()
    cur.close()
    conn.close()
    
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM protocols")
    protocols = cur.fetchall()
    print("Available protocols:")
    for p in protocols:
        print(f"ID: {p[0]}, Name: {p[1]}")
    cur.close()
    conn.close()


@app.route('/protocols', methods=['GET'])
def get_protocols():
    """Get all active protocols"""
    conn = get_db_connection()
    cur = dict_cursor(conn)

    cur.execute("""
        SELECT p.id, p.name, p.author_id, p.state, p.fields, u.name as author_name, u.surname as author_surname
        FROM protocols p
        JOIN users u ON p.author_id = u.id
        WHERE (p.state & 1) = 1
        ORDER BY p.id
    """)

    protocols = []
    for row in cur.fetchall():
        protocols.append({
            'id': row['id'],
            'name': row['name'],
            'author_id': row['author_id'],
            'author_name': f"{row['author_name']} {row['author_surname']}",
            'state': row['state'],
            'fields': row['fields']
        })

    cur.close()
    conn.close()

    return jsonify({
        'success': True,
        'data': protocols,
        'count': len(protocols)
    })


@app.route('/protocols/<protocol_id>', methods=['GET'])
def get_protocol(protocol_id):
    """Get specific protocol by ID"""
    conn = get_db_connection()
    cur = dict_cursor(conn)

    cur.execute("""
        SELECT p.id, p.name, p.author_id, p.state, p.fields, u.name as author_name, u.surname as author_surname
        FROM protocols p
        JOIN users u ON p.author_id = u.id
        WHERE p.id = %s AND (p.state & 1) = 1
    """, (protocol_id,))

    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Protocol not found'}), 404

    protocol = {
        'id': row['id'],
        'name': row['name'],
        'author_id': row['author_id'],
        'author_name': f"{row['author_name']} {row['author_surname']}",
        'state': row['state'],
        'fields': row['fields']
    }

    cur.close()
    conn.close()

    return jsonify({
        'success': True,
        'data': protocol
    })


# Example json it takes:
# {
#   "id": "2",
#   "name": "Safety Check Protocol",
#   "fields": {
#     "activities": [
#       "Check fire extinguisher",
#       "Test emergency alarm"
#     ]
#   }
# }
@app.route('/protocols', methods=['POST'])
def create_protocol():
    """Create new protocol"""
    data = request.get_json()

    if not data or 'id' not in data or 'name' not in data or 'fields' not in data:
        return jsonify({'success': False, 'error': 'Missing required fields: id, name, fields'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if protocol ID already exists
    cur.execute("SELECT id FROM protocols WHERE id = %s", (data['id'],))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Protocol ID already exists'}), 409

    cur.execute("""
        INSERT INTO protocols (id, name, author_id, state, fields)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data['id'],
        data['name'],
        CURRENT_USER_ID,
        data.get('state', 1),
        json.dumps(data['fields'])
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Protocol created successfully',
        'data': {'id': data['id']}
    }), 201


@app.route('/protocols/<protocol_id>', methods=['DELETE'])
def delete_protocol(protocol_id):
    """Delete protocol (set state bit 0 to 0)"""
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if protocol exists
    cur.execute("SELECT id, state FROM protocols WHERE id = %s", (protocol_id,))
    result = cur.fetchone()
    if not result:
        cur.close()
        conn.close()
        return jsonify({'success': False, 'error': 'Protocol not found'}), 404

    new_state = result[1] & ~1

    cur.execute("UPDATE protocols SET state = %s WHERE id = %s", (new_state, protocol_id))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Protocol deactivated successfully'
    })


def get_forms():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute("SELECT id, name, fields FROM protocols WHERE (state & 1) = 1")
    db_protocols = cur.fetchall()
    
    forms = []
    for protocol in db_protocols:
        protocol_id = protocol['id']
        fields = protocol['fields']

        activities = fields.get('activities', [])
        
        forms.append({
            "id": protocol_id,
            "name": protocol['name'],
            "activities": activities
        })
    
    cur.close()
    conn.close()
    return forms


def generate_pdf(form_idx, form_data) -> str | None:
    pdf_filename = f"form_{form_idx}_{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join('/tmp/', pdf_filename)

    temp_html_path = os.path.join('/tmp/', f"temp_{uuid.uuid4().hex}.html")

    forms = get_forms()
    form = next((f for f in forms if str(f['id']) == str(form_idx)), None)
    
    if not form:
        return None

    rendered_html = render_template(
        "form.html.jinja",
        form_id=form_idx,
        title=form['name'],
        activities=form['activities'],
        print_mode=True,
        form_data=form_data
    )

    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    subprocess.run([
        'google-chrome' if IDC_cond else 'chromium',
        '--no-sandbox' if IDC_cond else '',
        '--headless',
        '--no-pdf-header-footer',
        '--disable-gpu',
        '--print-to-pdf=' + pdf_path,
        'file://' + temp_html_path
    ], check=True, timeout=30)

    time.sleep(1)

    return pdf_path


@app.route("/print_pdf/<form_idx>", methods=['POST', 'GET'])
def print_pdf(form_idx):
    pdf_path = generate_pdf(form_idx, request.form)

    if pdf_path is None:
        return "Protocol not found", 404

    if os.path.exists(pdf_path):
        return send_file(pdf_path,
                         download_name=f"form_{form_idx}.pdf",
                         as_attachment=True)
    else:
        return "Failed to generate PDF", 500


# Przyjmowany JSON:
# {
#   "recitipent": mail do kogo wysłać,
#   "form_data": ten sam form_data, co wchodzi do jinja
# }
@app.route("/send_email/<form_idx>", methods=['POST'])
def send_email_protocol(form_idx):
    pdf_path = generate_pdf(form_idx, request.get_json()['form_data'])

    if pdf_path is None:
        return "Protocol not found", 404

    send_email(os.environ.get('EMAIL_EMAIL', ''), os.environ.get('EMAIL_TOKEN', ''), request.get_json()['recipient'], "Protokół", "", pdf_path)

    # Tutaj pewnie przydałoby się jakieś wykrywanie czy udało się wysłać maila, idk

    return jsonify({'message': 'Email sent'}), 200


@app.route("/form/<form_idx>")
def form(form_idx):
    forms = get_forms()
    print(f"Looking for form with ID: {form_idx}")
    print(f"Available form IDs: {[f['id'] for f in forms]}")
    
    form = next((f for f in forms if f['id'] == form_idx), None)
    
    if not form:
        return f"Protocol not found with ID: {form_idx}", 404
        
    return render_template("form.html.jinja", form_id=form_idx, title=form['name'], activities=form['activities'])


@app.route('/upload-protocols', methods=['POST'])
def upload_protocols():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    filename = secure_filename(file.filename)

    # TODO
    
    return jsonify({'message': 'File uploaded successfully'}), 200


@app.route("/")
def index():
    forms = get_forms()
    print("Forms available in index:", [f['id'] for f in forms])
    return render_template("index.html.jinja", forms=forms)


app.register_blueprint(api_reports)

init_db()
# if __name__ == "__main__":
#     import sys
#     print("INITTTTT")
#     print("INITTTTTTER", file=sys.stderr)
    
#     init_db()
#     app.run(debug=True)
