import os
import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags instantly.")

# Sidebar for API Key configuration
st.sidebar.header("Configuration")
api_key_input = st.sidebar.text_input("Enter Groq API Key:", type="password")

# Fallback to secrets or environment variables if sidebar is empty
groq_api_key = api_key_input or st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

# Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        content_type = st.selectbox(
            "Content Type", 
            ["Social Media Post", "Blog Intro", "Product Announcement", "Newsletter Snippet"]
        )
        platform = st.selectbox(
            "Platform", 
            ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "Threads"]
        )
        tone = st.selectbox(
            "Tone", 
            ["Professional", "Casual & Friendly", "Energetic & Hype", "Educational", "Persuasive"]
        )

    with col2:
        topic = st.text_input("Topic / Subject", placeholder="e.g., Remote work tips")
        target_audience = st.text_input("Target Audience", placeholder="e.g., Software engineers")

    submitted = st.form_submit_button("🚀 Generate Content", use_container_width=True)

# Generation Logic
if submitted:
    if not groq_api_key:
        st.error("Please provide a Groq API Key in the sidebar or Streamlit secrets.")
    elif not topic or not target_audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=groq_api_key)
            
            prompt = f"""
            You are an expert content creator. Write a high-converting {content_type} optimized for {platform}.
            
            Parameters:
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}
            
            Format the response clearly into these sections:
            1. **Main Post Content**
            2. **Caption / Ca
                
     ll to Action (CTA)**
            3. **Relevant Hashtags**
            """

            with st.spinner("Generating your content..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )           generated_text = response.choices[0].message.content

            st.success("Generated Successfully!")
            st.markdown("---")
            st.markdown(generated_text)

        except Exception as e:
            st.error(f"An error occurred: {e}")
