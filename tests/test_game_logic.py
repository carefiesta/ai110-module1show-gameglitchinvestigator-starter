from logic_utils import check_guess, hint_for_outcome, parse_guess, update_score, get_range_for_difficulty


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_too_high_hint_says_go_lower():
    # The 60 vs 50 bug: outcome is Too High, and the hint must point down.
    assert check_guess(60, 50) == "Too High"
    assert hint_for_outcome("Too High") == "Too High. Go lower."


def test_too_low_hint_says_go_higher():
    assert check_guess(40, 50) == "Too Low"
    assert hint_for_outcome("Too Low") == "Too Low. Go higher."


def test_wrong_guess_does_not_add_points():
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too Low", 1) == -5


def test_parse_guess_rejects_blank_and_words():
    assert parse_guess("")[0] is False
    assert parse_guess("nope")[0] is False
    assert parse_guess(" 60 ") == (True, 60, None)


def test_hard_range_is_wider_than_normal():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 200)
