print("STEP 25 RUNNING")

import glob
from sentence_transformers import SentenceTransformer, util
from tickets import create_ticket

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
        sources.append(path)

model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_vectors = model.encode(chunks)

def answer(question):
    scores = util.cos_sim(model.encode(question), chunk_vectors)[0]
    best = int(scores.argmax())
    score = float(scores[best])
    if score < THRESHOLD:
        ticket_id = create_ticket(question)
        return f"I couldn't find a reliable answer. I've raised ticket #{ticket_id} for IT support."
    return f"Source: {titles[best]} ({sources[best]})\n\n{chunks[best]}"

while True:
    q = input("\nAsk a question (or type quit): ").strip()
    if q.lower() == "quit":
        break
    if q:
        print(answer(q))