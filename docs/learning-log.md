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

## Evaluation 5: holdout run (24 Oct 2026)
- **Setup:** 8 fresh questions written by my supervisor after the gap rule (0.07) was chosen. Run once, then diagnosed with a print of the top pick.
- **Result:** 5 correct, 1 wrong answer served, 2 over-escalated. Without the gap rule it would have been 7 correct, 1 wrong, 0 over-escalated.
- **H1 and H8:** the top pick was correct, and the gap rule escalated them because two password sections scored close together.
- **H7 ("my account is broken"):** wrong answer served (lockout section, gap 0.10). Neither the threshold nor the gap rule catches it.
- **H5 and H6:** wrong top pick (office Wi-Fi), caught by the 0.25 threshold.
- **Conclusion:** The gap rule worked on the 21 questions it was tuned on but did not generalise (overfitting). Small gaps between overlapping sections of one guide do not mean a wrong answer.
- **Decision:** Set GAP_MIN = 0.0 by default. This decision was made after seeing the holdout, so that holdout is now used and any further tuning needs fresh questions.
- **Open problem:** Vague questions ("my account is broken", "cant sign in") land on the lockout section. Needs a different mechanism, such as asking a clarifying question.
- **Caveat:** Only 8 questions, written by someone who knew the guides.

## Ticket storage and redaction (27 Oct 2026)

- **Problem:** Escalated questions are saved as tickets, so a pasted password would be stored in the database.
- **First version:** A pattern that removed the word after "password is". It mangled "my password is not working" into "my password [removed] working", which nearly reverses the meaning.
- **Fix:** Stopped matching "isn't", and excluded common non-secret words such as "not" and "working".
- **Result:** Common patterns are redacted and harmless sentences are untouched.
- **Limit:** "Summer2026 is my password" still slips through, and a random string typed alone would too. A word list will always be incomplete.
- **Trade-off:** Too aggressive damages the ticket's meaning, and too loose lets secrets through.
- **Next:** Warn users in the interface not to share passwords, since filtering alone does not prevent it.

## Evaluation 6: VPN guide added (27 Oct 2026)

- **Change:** Added a VPN guide (3 sections), so the knowledge base has 11 sections. Row 7 was relabelled from escalate to its VPN section because the guide now exists, not because of a result. Rows 22 to 24 were added.
- **Result:** 20 of 24 correct (83%), 4 wrong answers served, 0 over-escalated (gap rule off).
- **Regression check:** No Wi-Fi or password question that passed before now fails.
- **Remaining failures:** #5 (missing section), #10 and #11 (overlapping password sections, #11's label is debatable), #18 (vague question).
- **Against targets:** covered 89% (met), not-in-guide escalation 50% (missed, only two questions), ambiguous 50% (missed).
- **Caveat:** The VPN section titles and test rows were written together, so the new passes are easier than fresh questions would be.
- **Next:** Write the software and printing guides, then test on a fresh batch of questions.

## Evaluation 7: all five topics written (27 Oct 2026)

- **Change:** Added software and printing guides (5 sections), bringing the knowledge base to 16 sections and all five scope topics. Added rows 25 to 29.
- **Result:** 24 of 29 correct (83%), 5 wrong answers served, 0 over-escalated (gap rule off).
- **New regression:** #8 ("It's not working") used to escalate (0.22) and now returns the printer section (0.36), because the new guide gave the vague question something to match.
- **Unchanged failures:** #5 (missing section), #10 and #11 (overlapping password sections, #11's label debatable), #18 (vague).
- **Against targets:** covered 92% (met), not-in-guide escalation 50% (missed, only two questions), ambiguous 0% (missed).
- **Pattern:** Vague questions get worse as the knowledge base grows, and a threshold does not fix it.
- **Caveat:** The new test rows were written around the new sections, so they are easier than fresh questions.
- **Next:** A fresh holdout that includes questions outside the five topics, then a mechanism for vague questions.

## Evaluation 8: second holdout (27 Oct 2026)

- **Setup:** 12 fresh questions written by my supervisor before any further changes, run once with all five topic guides (16 sections), threshold 0.25, gap rule off.
- **Result:** 7 of 12 correct, 5 wrong answers served, 0 over-escalated.
- **Covered questions:** 6 of 7 passed. J5 ("cant reach the intranet while working from my kitchen") went to office Wi-Fi instead of VPN, a plausible mistake.
- **Out-of-scope and vague questions:** Only 1 of 5 escalated. Wrong answers scored 0.26 to 0.35, above the 0.25 threshold, so a confident wrong section was returned for email setup, a broken monitor, "something is wrong with my computer" and "it wont let me in".
- **Against targets:** covered 86% (met), not-in-guide escalation 33% (missed), ambiguous 0% (missed).
- **Finding:** The similarity score measures topic closeness, not whether a section answers the question. Wrong answers (up to 0.35) overlap with correct ones (as low as 0.40 to 0.45), so no single threshold separates them cleanly.
- **Hypothesis, untested:** A higher threshold (about 0.35 to 0.40) would catch these but would also escalate some correct answers. Needs a fresh batch to test.
- **Caveat:** Questions were written by someone who knew the guides, and the sample is small.
- **Next:** Try a clarifying-question step for vague requests, and test a higher threshold on a new batch.

## Web interface (27 Oct 2026)

- **Built:** A Flask page with a question box, cited answers, a "never share passwords" notice, and ticket creation when no reliable answer is found.
- **Security check:** A question containing `<b>hello</b>` was shown as plain text, because Flask escapes user input.
- **Observed limit:** Junk input still creates tickets. Rate limiting and duplicate detection are future work.
- **Note for the dashboard:** Ticket text is user-written, so it must be escaped when displayed to staff.
- **Formatting:** Guide text is converted from Markdown to HTML and marked safe, which is only acceptable because the guides are written by the project owner.