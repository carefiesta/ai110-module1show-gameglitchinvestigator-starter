# Game Glitch Investigator: The Impossible Guesser

A Streamlit number-guessing game that shipped with AI-generated bugs. This repo finds those bugs, moves the rules into `logic_utils.py`, and checks the fixes with pytest.

## Setup

```bash
pip install -r requirements.txt
python -m streamlit run app.py
pytest
```

On this machine the interpreter is `python3` from the Python 3.13 framework, not `python`.

## Document Your Experience

The game asks for a number inside a difficulty range and answers too high, too low, or correct. The starter version lied about direction, dropped a win on even attempts, and left New Game unable to accept another guess.

Bugs found in play:

- A guess of 25 against secret 17 was stored once, but Attempts became 2 and Score became 5.
- The hint did not stay on the page. It was drawn only inside the Submit run.
- After a win, New Game changed the secret and Submit Guess did nothing, because status stayed on `won`.

Fixes applied:

- `check_guess`, `parse_guess`, `hint_for_outcome`, and `update_score` live in `logic_utils.py`.
- A guess above the secret says "Too High. Go lower." A guess below says "Too Low. Go higher."
- The secret stays an int on every attempt, so a correct guess can win.
- New Game sets status back to `playing` and rolls inside the difficulty range.
- A wrong guess costs 5 points. Hard is 1 to 200.

## Demo Walkthrough

1. User opens Developer Debug Info. Secret is 84. Attempts left is 7.
2. User enters 91 and clicks Submit Guess.
3. Game returns "Too High. Go lower." History is `[91]`. Attempts is 1. Score is negative because an earlier wrong guess also cost 5.
4. User enters 84.
5. Game returns "You won! The secret was 84. Final score: 80." The 80 is the carried -10 plus 90 points for a win on attempt 2.
6. The debug panel on that same click still says `playing` and score -10, because it is rendered before Submit is applied.
7. User clicks New Game. Attempts, history, and status clear, and a new secret is ready for Submit Guess.

## Test Results

```
........                                                                 [100%]
8 passed in 0.02s
```

The new case is a guess of 60 against a secret of 50. It must return "Too High" and the hint must say to go lower.
