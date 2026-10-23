print("STEP 14 RUNNING")

import csv
from sentence_transformers import SentenceTransformer, util

THRESHOLD = 0.25

# Load the guide and split it into chunks (same as before)
with open("knowledge_base/password-reset.md", encoding="utf-8") as f:
    text = f.read()
chunks = text.split("\n## ")[1:]
titles = [chunk.split("\n")[0].strip() for chunk in chunks]

model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_vectors = model.encode(chunks)

# NEW: load the test questions
with open("tests/test_questions.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

correct = 0
for row in rows:
    question_vector = model.encode(row["question"])
    scores = util.cos_sim(question_vector, chunk_vectors)[0]
    best_index = int(scores.argmax())
    best_score = float(scores[best_index])

    if best_score < THRESHOLD:
        answer = "escalate"
    else:
        answer = titles[best_index]

    expected = row["expected"].strip()
    passed = answer == expected
    if passed:
        correct += 1

    result = "PASS" if passed else "FAIL"
    print(result, row["id"], row["type"], round(best_score, 2), "| got:", answer, "| expected:", expected)

print(correct, "of", len(rows), "correct")