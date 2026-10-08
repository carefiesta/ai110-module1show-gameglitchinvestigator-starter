import random


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIXME: starter Hard range was 1-50, easier than Normal.
    # FIX: Hard is now 1-200. AI suggested the swap; kept Easy and Normal as labeled.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: moved from app.py so the UI does not own validation.
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(raw.strip())
    except (TypeError, ValueError):
        return False, None, "That is not a whole number."

    return True, value, None


def check_guess(guess, secret):
    """Compare guess to secret and return 'Win', 'Too High', or 'Too Low'.

    Starter tests expect this string, not a tuple.
    """
    # FIXME: starter compared int to str on even attempts and attached the wrong hint.
    # FIX: compare ints only. Hint text is hint_for_outcome, reviewed against a 60 vs 50 case.
    try:
        guess = int(guess)
        secret = int(secret)
    except (TypeError, ValueError):
        return "Too Low"

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def hint_for_outcome(outcome: str) -> str:
    """Return the hint the player should see for an outcome."""
    # FIX: starter said Go HIGHER on Too High. AI draft kept that; rejected it.
    if outcome == "Win":
        return "Correct!"
    if outcome == "Too High":
        return "Too High. Go lower."
    if outcome == "Too Low":
        return "Too Low. Go higher."
    return ""


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: starter added 5 points on an even Too High guess. Wrong guesses now cost 5.
    if outcome == "Win":
        points = 100 - 10 * max(attempt_number - 1, 0)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score


def roll_secret(difficulty: str) -> int:
    """Pick a new secret inside the difficulty range."""
    low, high = get_range_for_difficulty(difficulty)
    return random.randint(low, high)
