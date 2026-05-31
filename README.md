# ⚖️ Indian Law Assistant

An AI-powered legal assistant that helps you understand Indian laws in simple, everyday language using LangChain and OpenAI.

## 📋 Overview

This Streamlit application provides intelligent Q&A assistance for:
- **Indian Constitution** - Fundamental rights, duties, and governmental structure
- **Indian Penal Code (IPC)** - Criminal offences and punishments
- **Criminal Procedure Code (CrPC)** - Criminal procedures and processes

The application uses LangChain's Retrieval-Augmented Generation (RAG) to provide accurate, contextual legal explanations in layman's terms.

## ✨ Features

- 🔍 **Semantic Search** - Uses OpenAI embeddings to find relevant legal information
- 📚 **Multi-Document Support** - Integrates IPC, CrPC, and Constitution Q&A pairs
- 💬 **Simplified Explanations** - Translates complex legal language into everyday language
- 📖 **Real-World Examples** - Provides practical implications and examples
- 📍 **Source References** - Shows retrieved source documents for transparency
- 🎨 **Streamlit UI** - User-friendly web interface

## 🏗️ Architecture

```
User Query
    ↓
OpenAI Embeddings (text-embedding-3-small)
    ↓
FAISS Vector Store (Semantic Search)
    ↓
Retrieved Documents (Top 5 matches)
    ↓
Prompt Template (Context + Question)
    ↓
LLM (gpt-3.5-turbo)
    ↓
Simplified Legal Explanation
```

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Streamlit |
| **RAG Framework** | LangChain |
| **Embeddings** | OpenAI (text-embedding-3-small) |
| **LLM** | OpenAI GPT-3.5-Turbo |
| **Vector Store** | FAISS |
| **Data Format** | JSON (Q&A pairs) |

## 📦 Project Structure

```
.
├── Indian_law.py                 # Main Streamlit application
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
├── .github/
│   └── workflows/
│       └── run-streamlit.yml     # GitHub Actions workflow
└── law documents/
    ├── constitution_qa.json      # Constitution Q&A pairs
    ├── ipc_qa.json              # Indian Penal Code Q&A pairs
    └── crpc_qa.json             # Criminal Procedure Code Q&A pairs
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API Key
- Git

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file:**
   ```bash
   echo "OPENAI_API_KEY=sk-your-actual-key-here" > .env
   ```

5. **Run the Streamlit app:**
   ```bash
   streamlit run Indian_law.py
   ```

The app will open at `http://localhost:8501`

## 📖 Usage

### Local Usage

1. Start the application:
   ```bash
   streamlit run Indian_law.py
   ```

2. Ask your legal question in the search box

3. Get a simplified explanation with references

### Example Questions

- "What is the right to equality in the Constitution?"
- "What is theft according to IPC?"
- "What is the procedure for arrest under CrPC?"
- "What are my fundamental rights?"
- "What is the punishment for assault?"

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-openai-api-key
```

**Security Note:** Never commit `.env` to version control. It's already in `.gitignore`.

## 📊 Data Sources

The application uses three JSON files containing Q&A pairs:

- **constitution_qa.json** - Constitution-related questions and answers
- **ipc_qa.json** - Indian Penal Code questions and answers
- **crpc_qa.json** - Criminal Procedure Code questions and answers

## 🔄 How It Works

1. **Document Loading** - JSON files are loaded and converted to LangChain Document objects
2. **Text Splitting** - Documents are split into chunks (1000 chars, 200 overlap)
3. **Embedding** - All chunks are embedded using OpenAI's `text-embedding-3-small`
4. **Vector Store** - Embeddings are stored in FAISS for fast semantic search
5. **Query Processing** - User query is embedded and matched against the vector store
6. **Context Retrieval** - Top 5 relevant documents are retrieved
7. **Response Generation** - Context is passed to GPT-3.5-Turbo with a specialized prompt
8. **Simplification** - The LLM generates easy-to-understand legal explanations

## 📝 Custom Prompt Template

The application uses a comprehensive prompt template that instructs the LLM to:
- Use simple, everyday language
- Provide real-world examples
- Break down legal provisions into steps
- Highlight key rights and responsibilities
- Keep responses under 300 words
- Always reference section numbers

## 🤖 LLM Models Used

| Model | Purpose | Cost |
|-------|---------|------|
| `text-embedding-3-small` | Convert text to vectors | $0.02 per 1M tokens |
| `gpt-3.5-turbo` | Generate responses | $0.50/$1.50 per 1M tokens |

## 🐳 Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "Indian_law.py"]
```

Build and run:
```bash
docker build -t indian-law-assistant .
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... indian-law-assistant
```

## 🚀 GitHub Actions Deployment

This repository includes a GitHub Actions workflow that allows manual triggering:

1. Go to **Actions** tab on GitHub
2. Select **Run Indian Law Assistant**
3. Click **Run workflow**
4. Provide your API key via GitHub Secrets

The API key should be set in:
- **Settings** → **Secrets and variables** → **Actions** → **OPENAI_API_KEY**

## 📋 Requirements

```
streamlit==1.28.0
langchain==0.1.0
langchain-openai==0.0.2
langchain-community==0.0.10
faiss-cpu==1.7.4
python-dotenv==1.0.0
```

For GPU support (FAISS):
```bash
pip install faiss-gpu
```

## ⚠️ Disclaimer

**Important:** This AI assistant provides general information about Indian law for educational purposes only.

- ❌ Not a substitute for legal advice
- ❌ Should not be used for court proceedings
- ❌ Consult a qualified lawyer for specific legal matters
- ⚠️ Accuracy depends on the completeness of the database

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Error: "OPENAI_API_KEY not set"
- Ensure you have created a `.env` file with your API key
- Verify the key is valid and active

### Error: "No documents loaded"
- Check that JSON files are in the `law documents/` folder
- Verify JSON file format is correct

### Slow response times
- This is normal on first run (vector store creation takes time)
- Subsequent queries will be faster

### FAISS import error
```bash
pip install faiss-cpu
```

## 📞 Support

For issues or questions:
1. Check existing GitHub Issues
2. Create a new Issue with detailed description
3. Provide error logs and steps to reproduce

## 🙏 Acknowledgments

- LangChain for RAG framework
- OpenAI for embeddings and LLM
- Streamlit for UI framework
- FAISS for vector search

---

**Made with ⚖️ for legal clarity**
