from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_transcript(transcript):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.create_documents([transcript])

    return chunks