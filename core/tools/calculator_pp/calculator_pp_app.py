"""
calculator_pp_app.py - Streamlit Web UI for Calculator++
"""
import streamlit as st

def main():
    # Set page configuration
    st.set_page_config(page_title="Calculator++", page_icon="🧮", layout="centered")
    
    # Print the tool name and a welcome message
    st.title("🧮 Calculator++")
    st.markdown("### Welcome to the Web UI of Calculator++")
    st.divider()
    
    # For now, just a placeholder showing it works
    st.success("Streamlit UI successfully launched from the PyNIX Framework!")
    st.write("In the future, full graphical calculator logic will go here.")

# Streamlit scripts run top-to-bottom, so we call main() directly
if __name__ == "__main__":
    main()