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
say:
"I don't know based on the provided transcript."

RESPONSE FORMAT:
- Always answer point-wise.
- Use numbered points for main concepts.
- Use bullet points for details under each concept.
- Do not use Markdown headings such as ###.
- Do not write one long paragraph.
- Keep the answer clear, concise, and easy to read.
- Maintain proper spaces between words and sentences.
- Do not repeat the question.
- Do not add information that is not present in the context.

Example format:

1. Concept Name
   - Point one.
   - Point two.
   - Point three.

2. Another Concept
   - Point one.
   - Point two.
   - Point three.

Context:
{context}

Question:
{question}

Answer:
""",
        input_variables=["context", "question"]
    )

    def answer_question(question):

        # Retrieve relevant chunks
        docs = retriever.invoke(question)

        # Combine retrieved chunks
        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        # Generate final prompt
        final_prompt = prompt.invoke({
            "context": context,
            "question": question
        })

        # Get Gemini response
        response = llm.invoke(final_prompt)

        # Return only plain text
        return response.text

    return answer_question