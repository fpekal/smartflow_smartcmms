#!/usr/bin/env python3
from flask import Flask, render_template, abort, send_file, request, redirect, \
    url_for
import json
import tempfile
import os
import subprocess
import time
import uuid
import psycopg2
import psycopg2.extras


app = Flask(__name__)

DB_PARAMS = {
    'dbname': 'test',
    'user': 'test',
    'password': 'test',
    'host': 'localhost'
}


def init_db():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    
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
            VALUES ('1.1', '1.1 Przegląd statku meteorologicznego v1', 1, 1, %s)
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


@app.route("/print_pdf/<form_idx>", methods=['POST'])
def print_pdf(form_idx):
    pdf_filename = f"form_{form_idx}_{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join('/tmp/', pdf_filename)

    temp_html_path = os.path.join('/tmp/', f"temp_{uuid.uuid4().hex}.html")

    forms = get_forms()
    form = next((f for f in forms if str(f['id']) == str(form_idx)), None)
    
    if not form:
        return "Protocol not found", 404

    rendered_html = render_template(
        "form.html.jinja",
        form_id=form_idx,
        title=form['name'],
        activities=form['activities'],
        print_mode=True,
        form_data=request.form
    )

    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    subprocess.run([
        'chromium',
        '--headless',
        '--no-pdf-header-footer',
        '--disable-gpu',
        '--print-to-pdf=' + pdf_path,
        'file://' + temp_html_path
    ], check=True, timeout=30)

    time.sleep(1)

    if os.path.exists(pdf_path):
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        fields_data = {
            "activities": form['activities'],
            "responses": {k: v for k, v in request.form.items() if k != 'csrf_token'}
        }
        
        cur.execute("""
            INSERT INTO protocols_filled (id, protocol_id, user_id, state, fields)
            VALUES (nextval('protocols_filled_id_seq'), %s, 1, 1, %s)
        """, (form_idx, json.dumps(fields_data)))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return send_file(pdf_path,
                         download_name=f"form_{form_idx}.pdf",
                         as_attachment=True)
    else:
        return "Failed to generate PDF", 500


@app.route("/form/<form_idx>")
def form(form_idx):
    forms = get_forms()
    print(f"Looking for form with ID: {form_idx}")
    print(f"Available form IDs: {[f['id'] for f in forms]}")
    
    form = next((f for f in forms if f['id'] == form_idx), None)
    
    if not form:
        return f"Protocol not found with ID: {form_idx}", 404
        
    return render_template("form.html.jinja", form_id=form_idx, title=form['name'], activities=form['activities'])


@app.route("/")
def index():
    forms = get_forms()
    print("Forms available in index:", [f['id'] for f in forms])
    return render_template("index.html.jinja", forms=forms)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
