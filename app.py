import streamlit as st
from terminal_files.quiz import run_quiz
from terminal_files.score import display_stats

st.set_page_config(page_title="QuizMe", page_icon="Q")

st.title("QuizMe")
st.write("Welcome to QuizMe!! Pick a game mode!")

def choose_and_run_task():
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Run Quiz"):
            run_quiz()
    with col2:
        if st.button("View Stats"):
            display_stats()
    with col3:
        if st.button("Exit"):
            print("Thank you for playing! Goodbye!")
            return False
    return True

def main():
    st.write("Welcome, Welcome! What would you like to do today?")
    choose_and_run_task()
    st.write("What would you like to do next?")
    #pass


if __name__ == "__main__":
    main()