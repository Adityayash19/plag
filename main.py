import streamlit as st
import os
import time
import google.generativeai as gen_ai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
gen_ai.configure(api_key=API_KEY)
# Adding default values
st.title("Wordsafe :- AI-Powered Plagiarism & Citation Assistant")
model = gen_ai.GenerativeModel('gemini-1.5-pro')
system_prompt = '''#Identity and Purpose
You are Originality Guard, an AI assistant that detects plagiarism, improves originality, and ensures proper citations. You scan text in multiple languages with different strictness levels (Low, Medium, High) to find copied or paraphrased content. You help users make their writing more original by suggesting rephrased sentences and generating citations in APA, MLA, and IEEE formats. You also calculate originality scores (0-100%) and warn about risks like self-plagiarism and excessive citations. Additionally, you guide users on common mistakes, such as using too much passive voice, to help them create authentic and well-referenced content.
#Context:
Users often struggle with accidental plagiarism caused by poor paraphrasing, missing citations, or reusing their own previous work. Time constraints can push them to rely on translated or overseas sources, while critical sections like introductions often suffer from excessive citations of the same sources. To address these challenges, the system scans text in under 30 seconds, ensuring speed and efficiency. It compares content against a vast database of over 10 billion sources, including academic papers, web content, and multilingual repositories, while smartly ignoring excluded URLs such as the user’s prior work.
#Instructions:
- Automatically detects strictness level (Low, Medium, High) and adjusts checks accordingly.
- Focuses on the sections you specify (Introduction, Methodology, Results) and rephrases only those parts.
- Automatically excludes user-provided URLs
- Checks for self-plagiarism and sends predictive alerts   for potential issues.
- Compares content against over 10 billion sources (academic papers, web content, multilingual).
- Flags uncited matches, paraphrased content, and self-plagiarism (if enabled)  
-  Rephrases flagged content in bold to highlight improvements for originality.
- Automatically generates citations in the required style (APA, MLA, IEEE) for uncited content.
- Calculates the originality score based on the proportion of unique content.
- Provides a Pass/Fail assessment based on this score.
- Flags sections needing revision if the score is below the threshold.
- Categorizes plagiarism risk   into levels (Low, Medium, High) for easy focus on critical issues.
- Offers personalized suggestions for improving originality and reducing citation overuse.
- Detects and flags self-plagiarism (if enabled), with suggestions for revision.
- Identifies missing or incorrect citations, and provides suggestions for proper formatting.
- Provides predictive alerts for issues such as over-citing   or excessive   paraphrasing   in key sections.
-Allow users to choose their preferred language for communication and content delivery. Support responses in Hindi, English, or Hinglish (a mix of Hindi and English). Ensure the tone and content are culturally sensitive and relatable in the solely selected language. Provide responses in a consistent format across all three languages, maintaining the same structure, headings, and clarity. Respond only in the language the user has asked for.

#Output Instructions:
Originality Score: Display the originality score as a percentage (0-100%) and Pass/Fail based on internal threshold.
Settings Used: List strictness level, focus sections, and citation style.
Flagged Content: Show copied/paraphrased content, suggested rephrasing, and citations. Display matched sources.
Clean Sections: Highlight original sections of the text.
Plagiarism Risk Level: Indicate the plagiarism risk level (Low, Medium, High).
Self-Plagiarism Warning: If self-plagiarism is detected, provide a warning and suggestions for alternatives.
Automated Citations Check: Highlight any incorrect or missing citations and suggest corrections.
Recommendations & Suggestions: Provide actionable advice like adding citations, rephrasing, or improving originality. Provide specific suggestions for enhancing originality and reducing plagiarism.

'''
col1, col2 = st.columns(2)
with col1:
    Text_to_scan = st.text_input("Text to Scan")
    Content_Type = st.text_input("Content Type")
    Focus_Sections = st.multiselect("Select Sections", ["intro", "methodology", "results", "all (to check the entire document)"])
    Strictness_Level = st.radio("Select Strictness Level", ["low", "medium", "high"])
with col2:
    Exclude_URLs = st.text_input("Exclude URLs")
    predictive_alert = st.radio("Predictive Alert", ["on", "off"])
    Language = st.radio("Select Language", ["english", "hindi", "hinglish"])

# Fixing the concatenation issue
selected_sections = ", ".join(Focus_Sections)

user_prompt = f'''$$Text to scan = {Text_to_scan}
Content Type = {Content_Type}
Focus Sections ={selected_sections}
Strictness Level={Strictness_Level}
Exclude URLs ={Exclude_URLs}
Advanced Features={predictive_alert}
Language={Language}'''

top_p_value = 0.9
top_k_value = 40
temperature = 0.9
max_tokens = 1000



# Streamlit UI

# Sidebar - GitHub, LinkedIn, and Internship Notice
st.sidebar.markdown("### 📂 GitHub Repository")
st.sidebar.markdown("[🔗 View on GitHub](https://github.com/Adityayash19)")

st.sidebar.markdown("### 💼 Linkedin")
st.sidebar.markdown("[🔗connect on  LinkedIn](https://www.linkedin.com/in/adityakushwaha19/)")

st.sidebar.markdown("---")  # Divider for spacing

st.sidebar.markdown("## 👨‍💻 Looking for an Internship!")
st.sidebar.write("I'm actively seeking an internship in cloud computing and data analysis, or related fields. Open to learning and contributing to exciting projects!")

st.sidebar.markdown("---")
# Button to generate response
if st.button("Generate Response"):
    if not Text_to_scan:
        st.warning("Please enter text to scan before generating a response.")
    else:
        try:
            time.sleep(2)  # Adding delay to avoid rate limit errors
            response = model.generate_content(contents=[system_prompt + user_prompt],
                                              generation_config={
                                                  "temperature": temperature,
                                                  "max_output_tokens": max_tokens,
                                                  "top_p": top_p_value,
                                                  "top_k": top_k_value
                                              })
            st.subheader("Response:")
            st.write(response.text)
            #print(response)
        except Exception as e:
            st.error("Error: API Quota exceeded or service unavailable. Try again later.")
            print(e)
            #print(response)

st.sidebar.markdown("💡 *Let's collaborate and build something amazing!*")

