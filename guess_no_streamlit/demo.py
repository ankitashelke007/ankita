import streamlit as st

def main():
    st.title("My Streamlit App")
    
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "About", "Upload File"])
    
    if page == "Home":
        st.header("Welcome to My Streamlit App!")
        name = st.text_input("Enter your name:")
        if st.button("Submit"):
            st.success(f"Hello, {name}! Welcome to my app.")
    
    elif page == "About":
        st.header("About This App")
        st.write("This is a simple Streamlit application demonstrating navigation and user input handling.")
    
    elif page == "Upload File":
        st.header("File Upload")
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            st.write("File Uploaded Successfully!")
            st.write(f"Filename: {uploaded_file.name}")

if __name__ == "__main__":
    main()