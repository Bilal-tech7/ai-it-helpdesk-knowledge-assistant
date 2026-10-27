print("ASSISTANT MODULE LOADED")

import re
import markdown
import glob
import os
from sentence_transformers import SentenceTransformer, util
from experiments.tickets import create_ticket

THRESHOLD = 0.25

chunks = []
titles = []
sources = []
for path in sorted(glob.glob("knowledge_base/*.md")):
    if path.endswith("system-facts.md"):
        continue
    with open(path, encoding="utf-8") as f:
        text = f.read()
    for chunk in text.split("\n## ")[1:]:
        chunks.append(chunk)
        titles.append(chunk.split("\n")[0].strip())
        sources.append(os.path.basename(path))

model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_vectors = model.encode(chunks)

def to_html(text):
    # drop the title line, since the page already shows it as a heading
    body = text.split("\n", 1)[1] if "\n" in text else text
    # Markdown needs a blank line before the first numbered step
    body = re.sub(r"\n(\d+\. )", r"\n\n\1", body, count=1)
    return markdown.markdown(body)

def ask(question):
    scores = util.cos_sim(model.encode(question), chunk_vectors)[0]
    best = int(scores.argmax())
    score = float(scores[best])
    if score < THRESHOLD:
        ticket_id = create_ticket(question)
        return {"kind": "ticket", "ticket_id": ticket_id}
    return {
        "kind": "answer",
        "title": titles[best],
        "source": sources[best],
        "html": to_html(chunks[best]),
        "score": round(score, 2),
    }