print("STEP 9 RUNNING")

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

guides = [
    "To reset your password, go to the sign-in page and choose Forgot password. You will need your phone for MFA.",
    "To connect to the office Wi-Fi, select the network named Northwind-Staff and sign in with your work email.",
    "To install approved software, open the Software Centre and click Install next to the app.",
]

question = "How do I reset my password"

guide_vectors = model.encode(guides)
question_vector = model.encode(question)
scores = util.cos_sim(question_vector, guide_vectors)[0]

THRESHOLD = 0.25

best_index = int(scores.argmax())
best_score = float(scores[best_index])

print("Best score:", round(best_score, 2))
if best_score < THRESHOLD:
    print("No relevant guide found - escalate to a ticket")
else:
    print("Best match:", guides[best_index])