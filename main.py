import streamlit as st
from few_shot import FewShotPosts
def main():
    st.title("Linkedin Post Generator")
    col1,col2,col3 = st.columns(3)
    fs = FewShotPosts()
    with col1:
        st.selectbox("Title", options=fs.get_tags())

if __name__ == "__main__":
    main()