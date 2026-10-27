print("STEP  RUNNING")

import csv
from sentence_transformers import SentenceTransformer, util

THRESHOLD = 0.25
GAP_MIN = 0.0
TEST_FILE = "tests/test_questions.csv"
import glob

chunks = []
titles = []
for path in sorted(glob.glob("knowledge_base/*.md")):
    if path.endswith("system-facts.md"):
        continue
    with open(path, encoding="utf-8") as f:
        text = f.read()
    for chunk in text.split("\n## ")[1:]:
        chunks.append(chunk)
        titles.append(chunk.split("\n")[0].strip())

print("Chunks loaded:", len(chunks))
print("Test file:", TEST_FILE)

model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_vectors = model.encode(chunks)

# NEW: load the test questions
with open(TEST_FILE, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

correct = 0
wrong_answer = 0
over_escalated = 0

for row in rows:
    question_vector = model.encode(row["question"])
    scores = util.cos_sim(question_vector, chunk_vectors)[0]
    best_index = int(scores.argmax())
    best_score = float(scores[best_index])

    sorted_scores = sorted((float(s) for s in scores), reverse=True)
    gap = sorted_scores[0] - sorted_scores[1]

    if best_score < THRESHOLD or gap < GAP_MIN:
        answer = "escalate"
    else:
        answer = titles[best_index]

    expected = row["expected"].strip()

    if answer == expected:
        result = "PASS"
        correct += 1
    elif answer == "escalate":
        result = "OVER-ESCALATED"
        over_escalated += 1
    else:
        result = "WRONG ANSWER"
        wrong_answer += 1

    print(result, row["id"], row["type"], round(best_score, 2), "gap", round(gap, 2), "| got:", answer, "| top:", titles[best_index], "| expected:", expected)

print("Correct:", correct, "| Wrong answer served:", wrong_answer, "| Over-escalated:", over_escalated, "of", len(rows))