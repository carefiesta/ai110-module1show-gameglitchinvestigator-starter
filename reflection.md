# Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first run looked like a normal Streamlit number guesser: a difficulty sidebar, a guess box, Submit Guess, New Game, and a Developer Debug Info expander. Normal mode said the range was 1 to 100. The game was not playable past a win, and the debug panel did not match what one guess should do.

On the first finished guess, the secret in Developer Debug Info was 17 and I entered 25. History stored only `[25]`, but Attempts jumped to 2 and Score became 5. A too-high guess should say to go lower and should not add points. There was no yellow hint left on the page afterward. The secret was visible in the debug panel, and the only green text was a success-style message, not a lasting hint.

After a correct guess, New Game did change the secret, but Submit Guess stopped doing anything. The guess box could still be typed in, and no new guess was processed. Restarting Streamlit was the only way to get a fresh session.

Concrete bugs at the start:

- One guess is counted as 2 attempts, and that wrong guess raised the score from 0 to 5.
- The hint does not stay on screen. `st.warning` runs only inside the Submit click, so the next rerun erases it.
- New Game changes the secret but does not set status back to `"playing"`, so after a win Submit Guess is ignored.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Normal, secret 17, guess 25, Show hint checked | Hint says too high / go lower. Attempts becomes 1. Score stays 0. | History is `[25]`, Attempts is 2, Score is 5. No yellow hint remains after the page settles. | none |
| Correct secret, then New Game, then another number and Submit Guess | New game starts and Submit Guess compares the new number. | New Game changes the secret. Submit Guess does nothing after the win. | none |
| New Game while a game is in progress | Secret stays in the sidebar range, attempts reset, and a visible "New game started" message remains. | Secret changes, including off the Easy/Hard range because New Game always rolls 1 to 100. The success message does not stay, because `st.rerun()` wipes it. | none |

---

## 2. How did you use AI as a teammate?

I used Grok in the chat while the project was open on my Mac. I did not paste the AI output into the game without checking the running app and the debug panel.

One correct suggestion was the New Game failure. The AI said the button rolled a new secret but never set status back to `playing`, so the next rerun stopped before Submit Guess. I verified that after the fix: New Game cleared attempts and history, showed a new secret, and Submit Guess worked again.

One suggestion I did not accept was the first hint draft. It still told a too-high guess to go higher, which was the original bug with a new function name. I rejected that wording. A guess of 91 against secret 84 then showed "Too High. Go lower." in the app, and the pytest case for 60 against 50 checks the same rule.

---

## 3. Debugging and testing your fixes

I treated a bug as fixed only when the browser matched the rule, not when the code looked right. The debug panel was useful, but it is rendered before Submit runs, so on the winning click it still said `playing` and score -10 while the green line said "You won! The secret was 84. Final score: 80."

The pytest run reported 8 passed. The starter tests still expect `check_guess(60, 50)` to return the string `"Too High"`. The added test also checks that the hint says to go lower. A manual play confirmed the same path: 91 was too high, 84 won, and New Game started a fresh round.

The AI wrote those pytest cases. I kept the starter return type as a string instead of a tuple, because changing it would have broken the tests that were already in the repo.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the whole script on every click. A variable created in the script is new each time, so the secret has to live in `st.session_state` or it changes every Submit. Session state is the notebook that survives the rerun: secret, attempts, score, and status.

A message such as `st.warning` does not survive by itself. That is why the first hint disappeared. New Game also has to write status back to `playing`, or the next rerun stops and ignores the button.

---

## 5. Looking ahead: your developer habits

I want to keep the habit of writing the bug down with the input, the expected result, and the actual panel before editing. The 17 / 25 / attempts 2 / score 5 note made the later fix easy to check.

Next time I would run one fresh game before trusting a debug panel from the middle of a click. I would also reset the score on New Game so a carried penalty does not look like a new bug.

This project changed how I treat AI-generated code. Code that runs can still lie about hints, score, and state, so the AI is a teammate that proposes a cause, and the browser plus pytest decide whether it is true.
