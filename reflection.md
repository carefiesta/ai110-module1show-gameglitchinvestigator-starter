# 💭 Reflection: Game Glitch Investigator

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

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Normal, secret 17, guess 25, Show hint checked | Hint says too high / go lower. Attempts becomes 1. Score stays 0. | History is `[25]`, Attempts is 2, Score is 5. No yellow hint remains after the page settles. | none |
| Correct secret, then New Game, then another number and Submit Guess | New game starts and Submit Guess compares the new number. | New Game changes the secret. Submit Guess does nothing after the win. | none |
| New Game while a game is in progress | Secret stays in the sidebar range, attempts reset, and a visible "New game started" message remains. | Secret changes, including off the Easy/Hard range because New Game always rolls 1 to 100. The success message does not stay, because `st.rerun()` wipes it. | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
