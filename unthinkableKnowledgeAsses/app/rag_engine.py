import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def get_qa_chain():
    # 1. Load PDFs from the documents folder
    doc_path = os.path.join(os.getcwd(), "documents")
    if not os.path.exists(doc_path):
        os.makedirs("documents")
        
    loader = DirectoryLoader(doc_path, glob="./*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    if not documents:
        print("⚠️ Please put a PDF file in the 'documents' folder first!")
        return None
    
    # 2. Local Embeddings (Turns text into numbers)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 3. Create the Search Index (Vector Store)
    vectorstore = FAISS.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()
    
    # 4. Connect to your local Ollama model
    llm = ChatOllama(model="llama3.2:1b", temperature=0)

    template = """Answer the question based only on the following context:
    {context}
    
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 5. Build the Chain (Modified for Source Tracking)
    from langchain_core.runnables import RunnableParallel

    # Helper function to format the text for the LLM
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # This part handles the actual "Thinking"
    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    # This part preserves the "Documents" so we can see the Filenames later
    chain = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)
    
    return chain