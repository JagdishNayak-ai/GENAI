from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def create_rag_chain(retriever):

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash"
    )

    prompt = PromptTemplate(
        template="""
You are a helpful assistant answering questions
about a YouTube video.

Answer the question using ONLY the provided context.

If the answer cannot be found in the context,
say "I don't know based on the provided transcript."

Context:
{context}

Question:
{question}

Answer:
""",
        input_variables=["context", "question"]
    )

    def answer_question(question):

        docs = retriever.invoke(question)

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        final_prompt = prompt.invoke({
            "context": context,
            "question": question
        })
        response = llm.invoke(final_prompt)
        return response.text
    return answer_question