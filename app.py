import streamlit as st
from modules.validator import check_ambiguity
from modules.prioritizer import calculate_priority
from modules.generator import generate_test_cases

st.set_page_config(page_title="NLP Test Case Generator", layout="wide")

st.title("NLP-Based Automated Test Case Generator")
st.markdown("Enter a User Story below to generate Gherkin Test Cases.")

# Input Section
user_story = st.text_area("User Story", height=150, placeholder="As a user, I want to login so that I can access my dashboard.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Check Ambiguity"):
        if user_story:
            warnings = check_ambiguity(user_story)
            if warnings:
                st.warning("Ambiguity Detected:")
                for w in warnings:
                    st.write(f"- {w}")
            else:
                st.success("No ambiguous terms found!")
        else:
            st.error("Please enter a user story first.")

with col2:
    if st.button("Generate Test Cases"):
        if user_story:
            with st.spinner("Generating test cases..."):
                # 1. Generate
                generated_gherkin = generate_test_cases(user_story)
                
                # 2. Calculate Priority
                priority = calculate_priority(generated_gherkin, user_story)
                
                # Display Results
                st.subheader("Generated Test Cases")
                st.code(generated_gherkin, language="gherkin")
                
                st.subheader("Priority Assessment")
                if priority == "High":
                    st.error(f"Priority: {priority}")
                elif priority == "Medium":
                    st.warning(f"Priority: {priority}")
                else:
                    st.success(f"Priority: {priority}")
        else:
            st.error("Please enter a user story first.")

st.markdown("---")
st.caption("Final Year Project - NLP-Based Automated Test Case Generator")
