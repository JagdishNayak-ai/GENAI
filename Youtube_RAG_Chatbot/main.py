from dotenv import load_dotenv

from transcript import get_transcript
from chunking import split_transcript
from embeddings import create_vector_store
from retrieval import create_retriever
from rag import create_rag_chain
# Load environment variables
load_dotenv()

# --------------------------------
# 1. YouTube Video
# --------------------------------
video_id = "E0Hmnixke2g"
# --------------------------------
# 2. Get Transcript
# --------------------------------
print("Fetching transcript...")
transcript = get_transcript(video_id)
print("Transcript length:", len(transcript))

# --------------------------------
# 3. Split Transcript
# --------------------------------
print("\nCreating chunks...")
chunks = split_transcript(transcript)
print("Number of chunks:", len(chunks))

# --------------------------------
# 4. Create Vector Store
# --------------------------------
print("\nCreating FAISS vector store...")

vector_store = create_vector_store(chunks)

print("FAISS vector store created!")

# --------------------------------
# 5. Create Retriever
# --------------------------------
print("\nCreating retriever...")
retriever = create_retriever(vector_store)
print("Retriever created!")
# --------------------------------
# 6. Create RAG Chain
# --------------------------------
rag_chain = create_rag_chain(retriever)
# --------------------------------
# 7. Ask Question
# --------------------------------
question = input("\nAsk a question about the video: ")
answer = rag_chain(question)
print("\nAnswer:")
print(answer)