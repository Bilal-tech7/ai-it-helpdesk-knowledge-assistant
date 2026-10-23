print("STEP 11 RUNNING")

from sentence_transformers import SentenceTransformer, util

# NEW: load the real guide and split it into chunks
with open("knowledge_base/password-reset.md", encoding="utf-8") as f:
    text = f.read()

pieces = text.split("\n## ")
chunks = pieces[1:]   # NEW: skip the title piece

model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_vectors = model.encode(chunks)

THRESHOLD = 0.25
question = "It's not working"

question_vector = model.encode(question)
scores = util.cos_sim(question_vector, chunk_vectors)[0]

for chunk, score in zip(chunks, scores):
    print(round(float(score), 2), "-", chunk.split("\n")[0])

best_index = int(scores.argmax())
best_score = float(scores[best_index])
print("Best score:", round(best_score, 2))
if best_score < THRESHOLD:
    print("No relevant guide found - escalate to a ticket")
else:
    print("Best match:", chunks[best_index].split("\n")[0])