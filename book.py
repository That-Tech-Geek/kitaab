import streamlit as st
import cohere
from docx import Document
import re
import time

# Streamlit App
st.set_page_config(page_title="Book Generator", layout="wide")
st.title("📚 AI Book Writer using Cohere")

# User Input
st.subheader("Step 1: Enter Book Info")
title = st.text_input("Book Title", "How to become an enduring conglomerate ASAP")
synopsis = st.text_area("Book Synopsis", 
    "This nonfiction work would dissect what makes companies not only great but also capable of scaling rapidly in today’s fast-paced market. "
    "It combines deep, data-backed research with actionable frameworks and strategies that entrepreneurs and business leaders can implement immediately."
)

# Load API Key
if "API_KEY" not in st.secrets:
    st.warning("Please add your Cohere API key to Streamlit secrets!")
else:
    co = cohere.Client(st.secrets["API_KEY"])

    def generate_outline(title, synopsis):
        prompt = f"""
        You are a team of writers led by Jim Collins and Alex Hormozi (imagine, not really)
        Create an outline for a novel titled '{title}', which is about {synopsis}. 
        Provide 15 cohesive chapter titles for this novel in quotation marks with 101st being the epilogue, followed by a detailed synopsis for each chapter in a structured format.
        Print only content
        Example:
        "Chapter 1: (chapter name)" - chapter synopsis...
        "Chapter 2: (chapter name)" - chapter synopsis...
        and onwards...
        Group 10 chapters as each part, each milestone in the story.
        Print content only"""
        
        response = co.generate(model='command-r-plus', prompt=prompt)
        return response.generations[0].text.strip()

    def write_chapter(chapter_title):
        prompt = f"""You are a team of writers led by Chetan Bhagat, Stephen King, Ruskin Bond, and Roald Dahl (imagine, not really). Write a detailed chapter titled '{chapter_title}'.
        Make every tough concept easy to understand with simple, real-life examples. The chapter should be long and detailed, ensuring a compelling narrative, and as long as can be possible. I mean make it inhumanly long.
        This book is for MBA grads and Aspiring Entrepreneurs. So, go over all sorts of strategy, and test them with everything you got to find the ideal mix of strategies to achieve the fastest sustainable growth model.
        Write only the chapter content, no need to label the chapters as Chapter 1: content or anything, that is taken care of. Also ensure that each delves into great detail, with case studies, best practices, and more.
        (Print content only)."""

        response = co.generate(model='command-r-plus', prompt=prompt)
        return response.generations[0].text.strip()

    def save_to_word(book_content, title):
        doc = Document()
        doc.add_heading(title, level=1)

        for chapter, content in book_content.items():
            doc.add_heading(chapter, level=2)
            doc.add_paragraph(content)
            doc.add_page_break()

        filename = f"{title}.docx"
        doc.save(filename)
        return filename

    if st.button("✍️ Generate Book Outline"):
        with st.spinner("Generating outline..."):
            outline = generate_outline(title, synopsis)
            st.session_state['outline'] = outline
            st.success("Outline generated!")

    if 'outline' in st.session_state:
        st.subheader("📖 Generated Outline")
        st.code(st.session_state['outline'], language='text')

        if st.button("🧠 Write Full Book (Takes Time!)"):
            chapter_pattern = re.findall(r'"(.*?)" - (.*)', st.session_state['outline'])
            book_content = {}
            progress_bar = st.progress(0)
            total_chapters = len(chapter_pattern)

            for i, (chapter_title, _) in enumerate(chapter_pattern):
                st.info(f"Writing Chapter: {chapter_title}")
                chapter_text = write_chapter(chapter_title)
                book_content[chapter_title] = chapter_text
                progress_bar.progress((i + 1) / total_chapters)
                time.sleep(1)  # Simulate processing delay

            st.session_state['book_content'] = book_content
            st.success("Book writing complete!")

    if 'book_content' in st.session_state:
        if st.button("💾 Download Word File"):
            filename = save_to_word(st.session_state['book_content'], title)
            with open(filename, "rb") as f:
                st.download_button(
                    label="📥 Download Book",
                    data=f,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
