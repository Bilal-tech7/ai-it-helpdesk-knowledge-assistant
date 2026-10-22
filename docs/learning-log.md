## Retrieval experiment 1: keyword matching (22 Oct 2026)

- **What I built:** A simple keyword retriever in Python. It lowercases text, removes punctuation and filler words, scores each guide by how many words it shares with the question, and returns the best match. If no guide shares any words, it escalates to a ticket instead of guessing.

- **Problem 1 (punctuation):** Adding a full stop changed my score from 2 to 1. The computer treats `password` and `password.` as two different words, even though a human reads them as the same. Fix: strip punctuation from each word before comparing.

- **Problem 2 (filler words):** The pizza question scored 1, 2, 1 before I added stop words and 0, 0, 0 after. Words like `in` and `the` appear in almost every sentence, so they made an irrelevant question look like a partial match. Fix: ignore a list of common filler words.

- **Problem 3 (different wording):** "How do I connect to the Wi-Fi" found the Wi-Fi guide, but "I can't get online" did not. The guide exists, but no word in the question appears in it, so the score was 0 and the code escalated wrongly. The code only compares exact words, not meaning.

- **Problem 4 (spelling variants):** `wifi` did not match `wi-fi`. Lowercasing fixes capitals (WIFI, Wifi and wifi all become `wifi`), but the hyphen makes `wi-fi` a different string, and my code has no rule for hyphens or spaces. The right guide only won in that test because of one lucky shared word (`connect`).

- **What I learned:** Keyword matching is fragile. Small changes in wording change the result, and a correct escalation (pizza) and an incorrect one ("I can't get online") look identical to the code, both scoring 0, 0, 0.

- **Next:** Try meaning-based search (embeddings), so that "online" and "Wi-Fi" can match even without shared words.

- **Note for later:** In a real system, access control would decide who can see which guides.