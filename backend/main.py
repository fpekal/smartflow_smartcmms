#!/usr/bin/env python3
from flask import Flask, render_template, abort
import json

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
      "Inspekcja filtrów powietrza, wody i elementów systemu chłodzenia."
    ]
  }
]


@app.route("/form/<form_idx>")
def form(form_idx):
    form = forms[int(form_idx)]
    # TODO: enable autoescape
    return render_template("form.html.jinja", form_id=form_idx, title=form['name'], activities=form['activities'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
