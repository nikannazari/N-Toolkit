"""
calculator++_app.py - Streamlit Web UI for Calculator++
"""
import streamlit as st

def main():
    st.set_page_config(page_title="Calculator++", page_icon="🧮", layout="centered")
    st.title("🧮 Calculator++")
    st.markdown("### Welcome to the Web UI of Calculator++")
    st.divider()
    st.success("Streamlit UI successfully launched from the N-Toolkit Framework!")

if __name__ == "__main__":
    main()