import streamlit as st
from dotenv import load_dotenv

from transcript import get_transcript
from chunking import split_transcript
from embeddings import create_vector_store
from retrieval import create_retriever
from rag import create_rag_chain

load_dotenv()

st.set_page_config(
    page_title="VideoMind",
    page_icon="🎥",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    line-height: 1.2;
    margin: 0 0 5px 0;
}

.subtitle {
    text-align: center;
    color: #999;
    font-size: 15px;
    margin: 0 0 20px 0;
}

.status-card {
    background: #1e222b;
    color: #fff;
    border: 1px solid #3a3f4b;
    border-radius: 8px;
    padding: 9px 12px;
    margin-bottom: 6px;
    font-size: 14px;
}

.answer-box {
    background: #1e222b;
    color: #fff;
    border-left: 4px solid #ff4b4b;
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown(
    '<div class="main-title">🎥 VideoMind</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered YouTube Video Q&A using Retrieval-Augmented Generation'
    '</div>',
    unsafe_allow_html=True
)


# =========================
# SESSION STATE
# =========================

defaults = {
    "retriever": None,
    "rag_chain": None,
    "video_id": None,
    "chunks": None,
    "messages": [],
    "selected_question": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================
# FUNCTIONS
# =========================

def extract_video_id(url):

    if "v=" in url:
        return url.split("v=")[1].split("&")[0]

    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    return None


# =========================
# ADD VIDEO
# =========================

st.subheader("🔗 Add a YouTube Video")

youtube_url = st.text_input(
    "Paste YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

if st.button("🚀 Process Video", use_container_width=True):

    if not youtube_url:

        st.warning("Please enter a YouTube URL.")

    else:

        video_id = extract_video_id(youtube_url)

        if not video_id:

            st.error("Please enter a valid YouTube URL.")

        else:

            try:

                st.session_state.video_id = video_id

                with st.spinner("📄 Fetching transcript..."):
                    transcript = get_transcript(video_id)

                with st.spinner("🧩 Creating text chunks..."):
                    chunks = split_transcript(transcript)
                    st.session_state.chunks = chunks

                with st.spinner(
                    "🔎 Creating embeddings and FAISS index..."
                ):
                    vector_store = create_vector_store(chunks)

                st.session_state.retriever = create_retriever(
                    vector_store
                )

                with st.spinner(
                    "🤖 Preparing Gemini RAG pipeline..."
                ):
                    st.session_state.rag_chain = create_rag_chain(
                        st.session_state.retriever
                    )

                st.session_state.messages = []
                st.session_state.selected_question = ""

                st.success("✅ Video processed successfully!")

            except Exception as e:

                st.error(str(e))


# =========================
# VIDEO + PIPELINE
# =========================

if st.session_state.video_id:

    st.divider()

    # 50 / 50 layout
    video_col, pipeline_col = st.columns(
        [1, 1],
        gap="large"
    )

    # -------------------------
    # VIDEO
    # -------------------------

    with video_col:

        st.subheader("🎬 Video Preview")

        video_url = (
            "https://www.youtube.com/watch?v="
            + st.session_state.video_id
        )

        st.video(video_url)


    # -------------------------
    # PIPELINE
    # -------------------------

    with pipeline_col:

        st.subheader("📊 RAG Pipeline")

        pipeline = [
            "📄 <b>Transcript</b> — Ready",
            "🧩 <b>Chunking</b> — Completed",
            "🔎 <b>Embeddings</b> — Created",
            "🗂️ <b>FAISS</b> — Ready",
            "🟢 <b>RAG Pipeline</b> — Ready"
        ]

        for item in pipeline:

            st.markdown(
                f'<div class="status-card">{item}</div>',
                unsafe_allow_html=True
            )

        if st.session_state.chunks:

            st.metric(
                "🧩 Number of Chunks",
                len(st.session_state.chunks)
            )


# =========================
# SUGGESTED QUESTIONS
# =========================

if st.session_state.rag_chain:

    st.divider()

    st.subheader("💡 Try asking")

    questions = [
        "What is this video about?",
        "What are the main points discussed in the video?",
        "What are the most important concepts explained in the video?"
    ]

    cols = st.columns(3)

    for col, question in zip(cols, questions):

        with col:

            if st.button(
                question,
                use_container_width=True
            ):

                st.session_state.selected_question = question


# =========================
# ASK THE VIDEO
# =========================

if st.session_state.rag_chain:

    st.divider()

    st.subheader("💬 Ask the Video")

    question = st.text_input(
        "Your question",
        value=st.session_state.selected_question,
        placeholder="Ask anything about the video..."
    )

    if st.button(
        "🤖 Ask Question",
        use_container_width=True
    ):

        if not question:

            st.warning("Please enter a question.")

        else:

            with st.spinner(
                "🔍 Searching transcript and generating answer..."
            ):

                try:

                    answer = st.session_state.rag_chain(
                        question
                    )

                    st.session_state.messages.append({
                        "question": question,
                        "answer": answer
                    })

                    st.session_state.selected_question = ""

                except Exception as e:

                    st.error(str(e))


# =========================
# CONVERSATION
# =========================

if st.session_state.messages:

    st.divider()

    st.subheader("💬 Conversation")

    for message in st.session_state.messages:

        st.markdown(
            f"**🧑 You:** {message['question']}"
        )

        st.markdown(
            f"""
            <div class="answer-box">
                <strong>🤖 VideoMind</strong>
                <br><br>
                {message["answer"]}
            </div>
            """,
            unsafe_allow_html=True
        )