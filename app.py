import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    hint_for_outcome,
    parse_guess,
    roll_secret,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("Game Glitch Investigator")
st.caption("Number guessing game. Hints and new games should now agree with the secret.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


def start_round(selected_difficulty: str, reset_score: bool = False):
    """Reset the round so New Game can be played again."""
    # FIXME: starter New Game changed the secret but left status on won/lost.
    # FIX: status goes back to playing, secret stays in the difficulty range.
    st.session_state.secret = roll_secret(selected_difficulty)
    st.session_state.attempts = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_message = ""
    st.session_state.difficulty = selected_difficulty
    if reset_score or "score" not in st.session_state:
        st.session_state.score = 0


if "secret" not in st.session_state:
    start_round(difficulty, reset_score=True)

if st.session_state.get("difficulty") != difficulty:
    start_round(difficulty)

st.subheader("Make a guess")
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("Status:", st.session_state.status)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.attempts}_{st.session_state.status}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess")
with col2:
    new_game = st.button("New Game")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_round(difficulty)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")

if st.session_state.last_message and show_hint:
    st.warning(st.session_state.last_message)

if submit and st.session_state.status == "playing":
    st.session_state.attempts += 1
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.last_message = err
        st.error(err)
    else:
        st.session_state.history.append(guess_int)
        # FIX: removed the even-attempt str(secret) cast. It made a correct guess miss.
        outcome = check_guess(guess_int, st.session_state.secret)
        message = hint_for_outcome(outcome)
        st.session_state.last_message = message
        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )
        elif show_hint:
            st.warning(message)

st.divider()
st.caption("Guess logic lives in logic_utils.py.")
