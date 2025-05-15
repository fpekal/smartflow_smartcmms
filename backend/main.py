#!/usr/bin/env python3
from flask import Flask, render_template, abort, send_file, request, redirect, \
    url_for
import json
import tempfile
import os
import subprocess
import time
import uuid


app = Flask(__name__)

# Load form definitions
# with open("forms.json") as f:
#     FORM_DEFINITIONS = json.load(f)
#
forms = [
    {
        "name": "1.1 Przegląd statku meteorologicznego v1",
        "activities": [
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
            "Inspekcja filtrów powietrza, wody i elementów systemu chłodzenia.",
        ]
    }
]


@app.route("/print_pdf/<form_idx>", methods=['POST'])
def print_pdf(form_idx):
    pdf_filename = f"form_{form_idx}_{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join('/tmp/', pdf_filename)

    temp_html_path = os.path.join('/tmp/', f"temp_{uuid.uuid4().hex}.html")

    form = forms[int(form_idx)]
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
        '--disable-gpu',
        '--print-to-pdf=' + pdf_path,
        'file://' + temp_html_path
    ], check=True, timeout=30)

    time.sleep(1)

    if os.path.exists(pdf_path):
        return send_file(pdf_path,
                         download_name=f"form_{form_idx}.pdf",
                         as_attachment=True)
    else:
        return "Failed to generate PDF", 500



@app.route("/form/<form_idx>")
def form(form_idx):
    form = forms[int(form_idx)]
    return render_template("form.html.jinja", form_id=form_idx, title=form['name'], activities=form['activities'])


if __name__ == "__main__":
    app.run(debug=True)
