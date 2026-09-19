import streamlit as st
from dotenv import load_dotenv

from transcript import get_transcript
from chunking import split_transcript
from embeddings import create_vector_store
from retrieval import create_retriever
from rag import create_rag_chain

load_dotenv()

st.title("🎥 YouTube RAG Chatbot")
st.write("Ask questions about any YouTube video.")

youtube_url = st.text_input(
    "YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

question = st.text_input(
    "Ask a question",
    placeholder="What is this video about?"
)

if st.button("Ask Question"):

    if not youtube_url or not question:
        st.warning("Please enter both a YouTube URL and a question.")

    else:

        # Extract video ID
        if "v=" in youtube_url:
            video_id = youtube_url.split("v=")[1].split("&")[0]
        else:
            st.error("Please enter a valid YouTube URL.")
            st.stop()

        try:

            # Fetch transcript
            with st.spinner("Fetching transcript..."):
                transcript = get_transcript(video_id)

            # Create chunks
            with st.spinner("Creating chunks..."):
                chunks = split_transcript(transcript)

            # Create vector store
            with st.spinner("Creating vector store..."):
                vector_store = create_vector_store(chunks)

            # Create retriever
            retriever = create_retriever(vector_store)

            # Create RAG chain
            rag_chain = create_rag_chain(retriever)

            # Generate answer
            with st.spinner("Generating answer..."):
                answer = rag_chain(question)

            st.subheader("Answer")
            st.write(answer)

        except Exception as e:
            st.error(str(e))