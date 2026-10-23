## Retrieval experiment 1: keyword matching (22 Oct 2026)

- **What I built:** A simple keyword retriever in Python. It lowercases text, removes punctuation and filler words, scores each guide by how many words it shares with the question, and returns the best match. If no guide shares any words, it escalates to a ticket instead of guessing.

- **Problem 1 (punctuation):** Adding a full stop changed my score from 2 to 1. The computer treats `password` and `password.` as two different words, even though a human reads them as the same. Fix: strip punctuation from each word before comparing.

- **Problem 2 (filler words):** The pizza question scored 1, 2, 1 before I added stop words and 0, 0, 0 after. Words like `in` and `the` appear in almost every sentence, so they made an irrelevant question look like a partial match. Fix: ignore a list of common filler words.

- **Problem 3 (different wording):** "How do I connect to the Wi-Fi" found the Wi-Fi guide, but "I can't get online" did not. The guide exists, but no word in the question appears in it, so the score was 0 and the code escalated wrongly. The code only compares exact words, not meaning.

- **Problem 4 (spelling variants):** `wifi` did not match `wi-fi`. Lowercasing fixes capitals (WIFI, Wifi and wifi all become `wifi`), but the hyphen makes `wi-fi` a different string, and my code has no rule for hyphens or spaces. The right guide only won in that test because of one lucky shared word (`connect`).

- **What I learned:** Keyword matching is fragile. Small changes in wording change the result, and a correct escalation (pizza) and an incorrect one ("I can't get online") look identical to the code, both scoring 0, 0, 0.

- **Next:** Try meaning-based search (embeddings), so that "online" and "Wi-Fi" can match even without shared words.

- **Note for later:** In a real system, access control would decide who can see which guides.

## Retrieval experiment 2: embeddings with a threshold (22 Oct 2026)

- **What I built:** A retriever that uses a sentence-transformers embedding model (all-MiniLM-L6-v2) to compare a question with each guide by meaning, not by shared words. It picks the highest-scoring guide, and escalates to a ticket if the best score is below a threshold.

- **What an embedding does:** It turns a piece of text into a list of numbers, like a spot on a map, so that texts with similar meanings sit close together. The model learned this from a large amount of text, so I don't set the numbers by hand. A similarity score then measures how close the question is to each guide.

- **Results:**
  - "How do I reset my password": 0.73, correct guide, far ahead of the others.
  - "My laptop can't connect to the internet": 0.29, Wi-Fi guide correctly on top. This question also shares the word "connect" with the guide, so it is not a pure test of meaning.
  - "What's the best pizza in Sydney": -0.03, no relevant guide.
  - "I can't get online": 0.18 for the password guide, 0.14 for the Wi-Fi guide and 0.12 for the software guide. All were low and close together, and the wrong guide was on top.

- **Why I think wording mattered:** "I can't get online" is short and vague, and the model was not confident about any guide. A clearer question scored much higher for the right guide. I am not certain this is the whole reason, so I should test more phrasings.

- **Threshold:** I set it at 0.25. Before the threshold, "I can't get online" returned the password guide, a confident wrong answer. With the threshold it escalates instead. That is still a mistake, because a Wi-Fi guide exists, but it is a safe one.

- **Why a wrong escalation is safer than a wrong answer:** An escalated user reaches a human and nobody is misled. A wrong answer sends the user down a wrong path and may cause harm or make them more frustrated.

- **Limitation:** 0.25 fits my four examples, but one of them (0.29) clears it by only a small margin, so four questions cannot justify the number. I will choose the threshold using my 30-50 test questions and report how I chose it.

- **Next:** Write the five topic guides, split them into chunks, and search all of them. Then build the test question set.

## Retrieval experiment 3: searching the real guide (23 Oct 2026)

- **Clear questions worked:** "I forgot my password", "I'm locked out" and "new phone, can't approve sign-ins" scored 0.54 to 0.59 and found the right section. Pizza scored 0.01 and escalated.

- **Near-misses failed:** "set up MFA on a second phone" scored 0.56 and returned the lost-phone section, which does not answer it. "Change my password before it expires" scored 0.50 and returned the forgotten-password section, which has no steps for it.

- **Finding:** Right answers (0.54 to 0.59) and plausible-but-wrong answers (0.50 to 0.56) overlap, so a threshold alone cannot separate them.

- **Fix:** I added a "Change your password before it expires" section. The question that previously returned the wrong section (0.50) now returns the correct one (0.65). Some retrieval failures are gaps in the knowledge base, not the model.

- **Paraphrase tests:** "I need to update my password, I still know the old one" found the right section (0.55) but only just ahead of the runner-up (0.52). "My password is about to run out" returned the lockout section (0.50), which is wrong, because the guide says "expires" and the user said "run out".

- **What I think this means for my project:** The similarity score shows how related the topic is, not whether the section answers the question. I need to check answers against expected sections in a test set, not trust the score.

- **What I would try next:** Build a test set with expected answers, then measure whether changes help. Also test whether a small gap between the top two scores can flag likely failures.

## Evaluation 1: baseline on 18 questions (23 Oct 2026)

- **Setup:** Embedding search (all-MiniLM-L6-v2), threshold 0.25, over the password guide, tested on 18 questions.
- **Result:** 14 of 18 correct (78%).
- **Failures:** #5 (guide gap), #10 ("run out" vs "expires"), #11 (weak password, label debatable) and #18 ("cant sign in", vague). All scored above the threshold, so no threshold setting would have caught them.
- **Against my targets:** covered 82% (met), not-in-guide escalation 75% (missed), ambiguous 50% (missed), sensitive-data repetition not yet tested.
- **Caveat:** very small groups, and the set contains known failures, so this is a baseline, not a final score.
- **Next:** test whether a small gap between the top two scores flags likely failures.

## Evaluation 2: testing a gap rule (23 Oct 2026)

- **Hypothesis:** Wrong answers tend to win by a small margin over the runner-up, so escalating when the gap is small might catch them.
- **Evidence:** Three of four wrong answers had gaps of 0.06 or less, but two correct answers also had small gaps (0.04 and 0.03), and one wrong answer (#5, a missing section) had a gap of 0.16.
- **Result with gap rule 0.07:** 13 of 18 correct (down from 14). Wrong answers served fell from 4 to 1, but 4 questions were over-escalated.
- **Trade-off:** Fewer risky answers, but covered-question accuracy fell from 82% to 64%, below my 80% target.
- **Caveats:** The 0.07 value was chosen from the same 18 questions, so it is tuned to them. The sample is very small.
- **What I learned:** A single pass/fail total hides the difference between a wrong answer and an unnecessary escalation, so the script now reports both.
- **Next:** Try to reduce the confusion between sections, and test any change on fresh questions.

## Evaluation 3: adding the Wi-Fi guide (23 Oct 2026)

- **Change:** Added a Wi-Fi guide (3 sections), bringing the knowledge base to 8 sections.
- **Label change:** Row 16 ("wifi keeps dropping") was relabelled from escalate to its Wi-Fi section because the guide now exists, not because of a result.
- **Regression:** "My VPN won't connect" used to escalate (0.22) and now returns the office Wi-Fi section (0.34), because "connect" matches a Wi-Fi section.
- **Stable:** Results for the password questions did not change.
- **What I learned:** Adding content can change answers to unrelated questions, so every change to the knowledge base needs a re-run of the whole test set.
- **Next:** Add Wi-Fi test questions and re-run. A VPN guide would fix row 7 properly.

## Evaluation 3 result: Wi-Fi guide added (23 Oct 2026)

- **Result:** 16 of 21 correct (76%), 5 wrong answers served, 0 over-escalated (gap rule off).
- **Wi-Fi rows:** All four passed (#16, #19, #20, #21). #19 passed without containing the word "Wi-Fi". #20 is a multi-symptom question and a softer test.
- **Against my targets:** covered 87% (met), out-of-scope or gap escalation 33% (missed), ambiguous 50% (missed).
- **Finding:** The assistant answers covered questions well but does not escalate questions that are near a guide's topic without being answered by it. The threshold only catches unrelated questions.
- **Regression still open:** #7 ("My VPN won't connect") returns the office Wi-Fi section. A VPN guide would fix it properly.
- **Next:** Test the gap rule on this larger set, then write the remaining guides.

## Evaluation 4: gap rule on 21 questions (23 Oct 2026)

- **Result:** With the gap rule off: 16 correct, 5 wrong answers served, 0 over-escalated. With GAP_MIN = 0.07: 16 correct, 1 wrong answer served, 4 over-escalated.
- **What changed:** #7 and #18 went from wrong to correct. #9 and #12 went from correct to over-escalated. #10 and #11 went from wrong to over-escalated. #5 stayed wrong because the guide has no section for it.
- **Against targets (rule on):** covered 73% (missed), not-in-guide escalation 67% (missed, up from 33%), ambiguous 100% (met).
- **Pattern:** All four over-escalations were password questions, probably because the password sections overlap and score close together. This is untested.
- **Caveat:** 0.07 was chosen from earlier results, so this set is not a fair test of it.
- **Next:** Run a holdout set of fresh questions once, with no tuning afterwards.