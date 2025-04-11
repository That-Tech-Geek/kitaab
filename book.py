import cohere
from docx import Document

# Set up Cohere API client
cohere_api_key = st.secrets("API_KEY")
co = cohere.Client(cohere_api_key)

# Get title and synopsis from user input
title = "How to become an enduring conglomerate ASAP"
synopsis = "This nonfiction work would dissect what makes companies not only great but also capable of scaling rapidly in today’s fast-paced market. It combines deep, data-backed research with actionable frameworks and strategies that entrepreneurs and business leaders can implement immediately."

# Step 1: Generate Outline
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

outline = generate_outline(title, synopsis)
print("\nBook Outline Generated:")
print(outline)

# Step 2: Write the Book Piece by Piece
def write_chapter(chapter_title):
    prompt = f"""You are a team of writers led by Chetan Bhagat, stephen king, ruskin bond and roald dahl (imagine, not really). Write a detailed chapter titled '{chapter_title}'.
    Make every tough concept easy to understand with simple, real-life examples. The chapter should be long and detailed, ensuring a compelling narrative, and as long as can be possible. I mean make it inhumanly long.
    This book is for MBA grads and Aspiring Entrepreneurs. So, go over all sorts of startegi, and test them with everything you got to find the ideal mix of strategies to achieve the fastest sustainable growth model.
    Write only the chapter content, no need to label the chapters as Chapter 1: content or anything, that is taken care of. Also ensure that each delves into great detail, with case studies, best practices, and more.
    (Print content only)."""
    
    response = co.generate(
        model='command-r-plus',
        prompt=prompt,
    )
    chapter_content = response.generations[0].text.strip()
    return chapter_content

# Extract chapter titles correctly
import re
chapter_pattern = re.findall(r'"(.*?)" - (.*)', outline)

book_content = {}
for chapter_title, chapter_summary in chapter_pattern:
    print(f"\nWriting Chapter: {chapter_title}")
    chapter_content = write_chapter(chapter_title)
    book_content[chapter_title] = chapter_content

# Step 3: Save the Content into a Word File
def save_to_word(book_content, title):
    doc = Document()
    doc.add_heading(title, level=1)

    for chapter, content in book_content.items():
        doc.add_heading(f"{chapter}", level=2)
        doc.add_paragraph(content)
        doc.add_page_break()

    doc.save(f"{title}.docx")
    print(f"\nBook saved as {title}.docx")

save_to_word(book_content, title)
