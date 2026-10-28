print("STEP 35 RUNNING")

from flask import Flask, request, render_template_string, redirect, url_for
from assistant import ask
from experiments.tickets import list_tickets, update_status, STATUSES

app = Flask(__name__)

HEAD = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<style>
:root { --bg:#eaf4fb; --bg-grad:linear-gradient(135deg,#e3f2fd 0%,#e0f7fa 50%,#ede7f6 100%); --card:#ffffff; --text:#1d2433; --muted:#667085; --brand:#0f7bff; --line:#d5e3f0; --warn:#fff4d6; --warn-text:#7a5400; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#0b1220; --bg-grad:linear-gradient(135deg,#0b1220 0%,#0e1f33 50%,#1a1033 100%); --card:#121a2b; --text:#e8ebf2; --muted:#98a2b3; --brand:#5cc8ff; --line:#25324a; --warn:#3a2f10; --warn-text:#ffd98a; }
}
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); background-image:var(--bg-grad); background-attachment:fixed; color:var(--text); font-family: system-ui, -apple-system, "Segoe UI", sans-serif; line-height:1.55; }
header { background:var(--card); border-bottom:1px solid var(--line); }
.bar { max-width:900px; margin:0 auto; padding:14px 20px; display:flex; justify-content:space-between; align-items:center; }
.brand { font-weight:700; font-size:1.1rem; }
nav a { margin-left:18px; color:var(--muted); text-decoration:none; font-weight:500; }
nav a:hover, nav a.active { color:var(--brand); }
main { max-width:900px; margin:0 auto; padding:28px 20px 60px; }
.card { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:22px 24px; margin-bottom:20px; box-shadow:0 4px 20px rgba(0,0,0,0.06); }
.notice { background:var(--warn); color:var(--warn-text); border-radius:10px; padding:12px 16px; margin-bottom:20px; font-size:0.95rem; }
.ask { display:flex; gap:10px; }
.ask input { flex:1; padding:12px 14px; font-size:1rem; border:1px solid var(--line); border-radius:10px; background:var(--bg); color:var(--text); }
.ask input:focus { outline:2px solid var(--brand); }
button, .btn { background:var(--brand); color:#fff; border:0; border-radius:10px; padding:12px 20px; font-size:1rem; cursor:pointer; }
.chips { margin-top:14px; display:flex; flex-wrap:wrap; gap:8px; }
.chips button { background:transparent; color:var(--brand); border:1px solid var(--line); border-radius:999px; padding:6px 14px; font-size:0.9rem; }
.chips button:hover { border-color:var(--brand); }
.meta { color:var(--muted); font-size:0.9rem; margin-top:-6px; }
h1 { margin-top:0; } h2 { margin-top:0; }
table { width:100%; border-collapse:collapse; }
th, td { text-align:left; padding:10px 8px; border-bottom:1px solid var(--line); vertical-align:middle; }
th { color:var(--muted); font-size:0.85rem; text-transform:uppercase; letter-spacing:0.04em; }
.badge { display:inline-block; padding:2px 10px; border-radius:999px; font-size:0.85rem; font-weight:600; }
.s-new { background:#fde8e8; color:#b42318; }
.s-in-progress { background:#fff4d6; color:#7a5400; }
.s-resolved { background:#dcf5e4; color:#1a6b3a; }
.stats { display:flex; gap:12px; margin-bottom:20px; flex-wrap:wrap; }
.stat { flex:1; min-width:120px; background:var(--card); border:1px solid var(--line); border-radius:12px; padding:14px 18px; }
.stat b { font-size:1.6rem; display:block; }
select { padding:6px; border-radius:8px; border:1px solid var(--line); background:var(--bg); color:var(--text); }
.small { padding:6px 12px; font-size:0.9rem; }
</style>
</head>
<body>
<header><div class="bar">
  <span class="brand">Northwind IT Helpdesk</span>
  <nav><a href="/" class="{{ 'active' if page == 'home' else '' }}">Assistant</a>
       <a href="/tickets" class="{{ 'active' if page == 'tickets' else '' }}">Tickets</a></nav>
</div></header>
<main>
"""

TAIL = """
</main>
</body>
</html>
"""

PAGE = HEAD + """
<div class="notice"><strong>Never share passwords, MFA codes or personal details here.</strong> IT will never ask for them.</div>

<div class="card">
  <h1>How can we help?</h1>
  <form method="post" class="ask">
    <input name="question" value="{{ question }}" placeholder="Describe your IT problem" autofocus>
    <button type="submit">Ask</button>
  </form>
  <form method="post" class="chips">
    {% for example in examples %}
    <button type="submit" name="question" value="{{ example }}">{{ example }}</button>
    {% endfor %}
  </form>
</div>

{% if result %}
<div class="card">
  {% if result.kind == "ticket" %}
    <h2>No reliable answer found</h2>
    <p>I couldn't match this to an approved guide, so I've raised <strong>ticket #{{ result.ticket_id }}</strong> for IT support.</p>
    <p><a href="/tickets">View tickets</a></p>
  {% else %}
    <h2>{{ result.title }}</h2>
    <p class="meta">Source: {{ result.source }}</p>
    <details class="meta"><summary>Technical details</summary>
      Similarity score: {{ result.score }}. This measures how related the guide section is to your question, not whether it answers it.
    </details>
    <div>{{ result.html|safe }}</div>
  {% endif %}
</div>
{% endif %}
""" + TAIL

TICKETS_PAGE = HEAD + """
<h1>Ticket dashboard</h1>
<div class="stats">
  {% for s in statuses %}
  <div class="stat"><b>{{ counts[s] }}</b>{{ s }}</div>
  {% endfor %}
</div>
<div class="card">
<table>
  <tr><th>ID</th><th>Question</th><th>Status</th><th>Change</th><th>Created (UTC)</th></tr>
  {% for t in tickets %}
  <tr>
    <td>{{ t[0] }}</td>
    <td>{{ t[1] }}</td>
    <td><span class="badge s-{{ t[2]|lower|replace(' ', '-') }}">{{ t[2] }}</span></td>
    <td>
      <form method="post" action="/tickets/{{ t[0] }}/status">
        <select name="status">
          {% for s in statuses %}
          <option value="{{ s }}" {% if s == t[2] %}selected{% endif %}>{{ s }}</option>
          {% endfor %}
        </select>
        <button type="submit" class="small">Update</button>
      </form>
    </td>
    <td>{{ t[3] }}</td>
  </tr>
  {% endfor %}
</table>
</div>
""" + TAIL

EXAMPLES = [
    "How do I reset my password",
    "VPN keeps dropping",
    "Printer says printed but nothing comes out",
    "I need Slack on my laptop",
]

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    question = ""
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            result = ask(question)
    return render_template_string(PAGE, title="Northwind IT Helpdesk Assistant", page="home",
                                  result=result, question=question, examples=EXAMPLES)

@app.route("/tickets")
def tickets():
    rows = list_tickets()
    counts = {s: sum(1 for t in rows if t[2] == s) for s in STATUSES}
    return render_template_string(TICKETS_PAGE, title="Ticket dashboard", page="tickets",
                                  tickets=rows, statuses=STATUSES, counts=counts)

@app.route("/tickets/<int:ticket_id>/status", methods=["POST"])
def set_status(ticket_id):
    update_status(ticket_id, request.form.get("status", ""))
    return redirect(url_for("tickets"))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)