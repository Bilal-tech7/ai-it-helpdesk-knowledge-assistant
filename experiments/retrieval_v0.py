print("STEP 7 RUNNING")

STOP_WORDS = {"the", "in", "to", "a", "and", "of", "for", "with", "how", "do", "i", "my", "your", "you"}

def words(text):
    result = set()
    for word in text.lower().split():
        cleaned = word.strip(".,?!")
        if cleaned not in STOP_WORDS:
            result.add(cleaned)
    return result

guides = [
    "To reset your password, go to the sign-in page and choose Forgot password. You will need your phone for MFA.",
    "To connect to the office Wi-Fi, select the network named Northwind-Staff and sign in with your work email.",
    "To install approved software, open the Software Centre and click Install next to the app.",
]

question = "I can't get online"

print("Question words:", words(question))
for guide in guides:
    score = len(words(question) & words(guide))
    print(score, "-", guide)

best_score = 0
best_guide = None

for guide in guides:
    score = len(words(question) & words(guide))
    if score > best_score:
        best_score = score
        best_guide = guide

if best_guide is None:
    print("No relevant guide found - escalate to a ticket")
else:
    print("Best match:", best_guide)

