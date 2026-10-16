import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

length_options = ["Short","Medium","Long"]
language_options =["English","Banglish"]

def main():
    st.title("Linkedin Post Generator")
    col1,col2,col3 = st.columns(3)
    fs = FewShotPosts()
    with col1:
        selected_tags=st.selectbox("Topic", options=fs.get_tags())
    with col2:
        selected_length = st.selectbox("length", options=length_options)
    with col3:
        selected_language=st.selectbox("language", options=language_options)


    if st.button("Generate"):
        post = generate_post(selected_length, selected_language, selected_tags)
        st.write(post)


if __name__ == "__main__":
    main()