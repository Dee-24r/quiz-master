import streamlit as st
from streamlit_files.quiz import run_quiz
from streamlit_files.score import display_stats
from streamlit_files.utils import configure_quiz

st.set_page_config(page_title="QuizMe", page_icon="Q")

st.title("QuizMe")

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "state_game_config" not in st.session_state:
    st.session_state.state_game_config = {}


def choose_and_run_task():
    st.write("Welcome to QuizMe!!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Run Quiz"):
            st.session_state.current_page = "configure_quiz"

    with col2:
        if st.button("View Stats"):
            st.session_state.current_page = "display_stats"
            #display_stats()

def main():

    if st.session_state.current_page == "home":
        st.write("Welcome, Welcome! What would you like to do today?")
        choose_and_run_task()

    if st.session_state.current_page == "configure_quiz":
        configure_quiz()

    if st.session_state.current_page == "run_selected_quiz":
        run_quiz()

    if st.session_state.current_page == "display_stats":
        display_stats()


if __name__ == "__main__":
    main()

