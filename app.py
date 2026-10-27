print("STEP 31 RUNNING")

from flask import Flask, request, render_template_string
from assistant import ask

app = Flask(__name__)

PAGE = """
<!doctype html>
<title>Northwind IT Helpdesk Assistant</title>
<body style="font-family: sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem;">
<h1>Northwind IT Helpdesk Assistant</h1>
<p><strong>Never share passwords, MFA codes or personal details here.</strong>
IT will never ask for them.</p>

<form method="post">
  <input name="question" value="{{ question }}" placeholder="Describe your IT problem"
         style="width: 80%; padding: 0.5rem;" autofocus>
  <button type="submit" style="padding: 0.5rem 1rem;">Ask</button>
</form>

{% if result %}
  {% if result.kind == "ticket" %}
    <h2>No reliable answer found</h2>
    <p>I've raised ticket #{{ result.ticket_id }} for IT support.</p>
  {% else %}
    <h2>{{ result.title }}</h2>
    <p><em>Source: {{ result.source }} (match score {{ result.score }})</em></p>
    <pre style="white-space: pre-wrap; font-family: inherit;">{{ result.text }}</pre>
  {% endif %}
{% endif %}
</body>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    question = ""
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            result = ask(question)
    return render_template_string(PAGE, result=result, question=question)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)