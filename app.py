import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
prompt="You are the youtube video summarizer. your task is to summarize the entire video in way that all important points are covered and also provide the usecases if there else examples in 250 words"

def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text


def transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        print(video_id)
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript=" "
        for i in transcript_text:
            transcript +=" "+i["text"]
        return transcript

    except Exception as e:
         raise e

st.title("Youtube Transccript Summerizer")
youtube_link=st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=transcript_details(youtube_link)
    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("##Summerizer Content:")
        st.write(summary)


