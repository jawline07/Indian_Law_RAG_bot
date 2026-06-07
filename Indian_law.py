import os
import json
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

# Load environment variables
load_dotenv()

# Initialize OpenAI API
st.title("⚖️ Indian Law Assistant")
st.subheader(
    "Understanding Indian Constitution, IPC, and CrPC in Simple Terms")
with st.sidebar:
    st.title("provide your API key")
    api_key = st.text_input("enter Api key", type="password")
if not api_key:
    st.info("Enter your Api key to continue")
    st.stop()


def load_json_documents(file_path: str, source_name: str) -> list:
    """
    Load Q&A pairs from JSON file and convert to Document objects.

    Args:
        file_path: Path to the JSON file
        source_name: Source identifier (IPC, CRPC, or Constitution)

    Returns:
        List of Document objects
    """
    documents = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for idx, item in enumerate(data):
            if isinstance(item, dict) and 'answer' in item:
                # Create content combining question and answer if question exists
                question = item.get('question', 'General Information')
                answer = item.get('answer', '')

                content = f"Question: {question}\n\nAnswer: {answer}"

                doc = Document(
                    page_content=content,
                    metadata={
                        "source": source_name,
                        "document_type": source_name,
                        "index": idx
                    }
                )
                documents.append(doc)

    except FileNotFoundError:
        print(f"Warning: File {file_path} not found")
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in {file_path}")

    return documents


def create_combined_vector_store(document_paths: dict) -> tuple:
    """
    Create a combined vector store from multiple legal JSON documents.

    Args:
        document_paths: Dictionary with keys (IPC, CRPC, Constitution) and file paths as values

    Returns:
        Tuple of (vector_store, all_documents)
    """
    # Initialize embeddings using OpenAI
    embeddings = OpenAIEmbeddings(
        api_key=api_key,
        model="text-embedding-3-small"
    )

    all_documents = []

    # Load documents from all three legal codes
    for source_name, file_path in document_paths.items():
        print(f"Loading {source_name} documents...")
        docs = load_json_documents(file_path, source_name)
        all_documents.extend(docs)
        print(f"✓ Loaded {len(docs)} Q&A pairs from {source_name}")

    if not all_documents:
        raise ValueError("No documents loaded from the provided files")

    # Split documents into chunks for better retrieval
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    split_documents = text_splitter.split_documents(all_documents)

    # Create vector store from documents
    vector_store = FAISS.from_documents(
        documents=split_documents,
        embedding=embeddings
    )

    return vector_store, all_documents


def create_legal_rag_chain(vector_store):
    """
    Create a RAG chain for Indian legal information retrieval.

    Args:
        vector_store: FAISS vector store with legal documents

    Returns:
        LCEL chain for legal Q&A
    """
    # Initialize the language model
    llm = ChatOpenAI(
        api_key=api_key,
        model="gpt-3.5-turbo",
        temperature=0.7
    )

    # Create a comprehensive legal prompt template
    template = """You are an expert legal assistant specializing in Indian Law. Your task is to explain legal concepts in simple, easy-to-understand language for people without legal backgrounds.

IMPORTANT GUIDELINES:
1. Translate complex legal language into everyday language
2. Use analogies and real-world examples when explaining legal concepts
3. Clearly state which legal code or section you're referencing (Indian Penal Code, Criminal Procedure Code, or Constitution)
4. Break down legal provisions into simple steps or points
5. Highlight the key rights, duties, and responsibilities involved
6. Provide practical implications of the law

CONTEXT FROM LEGAL DOCUMENTS:
{context}

USER QUERY: {question}

RESPONSE GUIDELINES:
- Start with a simple explanation suitable for a layperson
- Use bullet points for clarity when listing multiple aspects
- Provide real-world examples if relevant
- Highlight important deadlines, procedures, or rights
- If a specific section is mentioned, explain what it means in practical terms
- Keep the response within 300 words for clarity
- Always mention the relevant section number and legal code

RESPONSE:"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    # Create retrieval chain
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}  # Retrieve top 5 most relevant documents
    )

    # Build LCEL chain
    qa_chain = (
        {
            "context": itemgetter("question") | retriever | (lambda docs: "\n\n---\n\n".join([doc.page_content for doc in docs])),
            "question": itemgetter("question")
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return qa_chain


def initialize_streamlit_ui():
    """Initialize Streamlit UI configuration."""
    st.set_page_config(
        page_title="Indian Law Assistant",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    This AI-powered legal assistant helps you understand Indian laws in everyday language.
    Ask questions about:
    - **Indian Constitution** - Fundamental rights, duties, and governmental structure
    - **Indian Penal Code (IPC)** - Criminal offences and punishments
    - **Criminal Procedure Code (CrPC)** - Criminal procedures and processes
    """)


def main():
    """Main Streamlit application."""
    initialize_streamlit_ui()

    # Initialize session state
    if "vector_store" not in st.session_state:
        with st.spinner("Loading legal documents and creating vector store..."):
            try:
                document_paths = {
                    "Indian Constitution": "law documents/constitution_qa.json",
                    "Indian Penal Code (IPC)": "law documents/ipc_qa.json",
                    "Criminal Procedure Code (CrPC)": "law documents/crpc_qa.json"
                }

                vector_store, documents = create_combined_vector_store(
                    document_paths)
                st.session_state.vector_store = vector_store
                st.session_state.qa_chain = create_legal_rag_chain(
                    vector_store)
                st.session_state.total_documents = len(documents)

                st.success(
                    f"✓ Successfully loaded {len(documents)} legal Q&A pairs from 3 legal codes!")

            except Exception as e:
                st.error(f"Error loading documents: {str(e)}")
                st.info(
                    "Please ensure the JSON files are in the 'law documents' folder")
                return

    # Sidebar for additional information
    with st.sidebar:
        st.markdown("### 📚 About This Assistant")
        st.markdown(f"""
        **Total Legal Q&A Pairs:** {st.session_state.total_documents}
        
        **Coverage:**
        - Constitution of India
        - Indian Penal Code (IPC)
        - Criminal Procedure Code (CrPC)
        
        **Features:**
        - Simplified legal explanations
        - Real-world examples
        - Reference to specific sections
        - Easy-to-understand language
        """)

        st.markdown("---")
        st.markdown("### 💡 Example Questions")
        example_questions = [
            "What is the right to equality in the Constitution?",
            "What is theft according to IPC?",
            "What is the procedure for arrest under CrPC?",
            "What are fundamental rights?",
            "What is the punishment for assault?"
        ]
        for i, question in enumerate(example_questions, 1):
            st.markdown(f"{i}. {question}")

    # Main chat interface
    st.markdown("---")
    st.markdown("### 🔍 Ask Your Legal Question")

    # Create two columns for input and button
    col1, col2 = st.columns([4, 1])

    with col1:
        user_query = st.text_input(
            "Enter your question about Indian law:",
            placeholder="E.g., What are my rights under the Constitution?",
            label_visibility="collapsed"
        )

    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)

    # Process the query
    if search_button and user_query:
        with st.spinner("Searching legal database and generating response..."):
            try:
                response = st.session_state.qa_chain.invoke(
                    {"question": user_query})

                # Display response
                st.markdown("---")
                st.markdown("### 📋 Legal Explanation")
                st.markdown(response)

                # Add a divider and additional context
                st.markdown("---")
                st.markdown("### 📍 Retrieved References")

                # Retrieve source documents for transparency
                retriever = st.session_state.vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 3}
                )
                source_docs = retriever.invoke(user_query)

                for idx, doc in enumerate(source_docs, 1):
                    with st.expander(f"Reference {idx} - {doc.metadata.get('document_type', 'Unknown')}"):
                        st.markdown(
                            f"**Source:** {doc.metadata.get('document_type', 'Unknown')}")
                        st.text(
                            doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)

            except Exception as e:
                st.error(f"Error processing query: {str(e)}")

    # Additional information section
    st.markdown("---")
    st.markdown("### ℹ️ Disclaimer")
    st.warning("""
    **Important:** This AI assistant provides general information about Indian law for educational purposes only.
    It should not be considered as legal advice. For specific legal matters, please consult a qualified lawyer.
    The accuracy of responses depends on the completeness of the legal database used.
    """)


if __name__ == "__main__":
    main()
