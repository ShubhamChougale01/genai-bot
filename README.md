# GenAI Bot

A Python-based AI chatbot that answers questions from a PDF using Retrieval-Augmented Generation (RAG), performs arithmetic operations, and fetches general information via web search.

## Features
1. **PDF Q&A**: Answers questions from `genai_intro.pdf` using RAG with FAISS(vectore db) and HuggingFace embeddings(all-MiniLM-L6-v2).
2. **Calculator**: Evaluates arithmetic expressions (e.g., "45 × 19").
3. **Web Search**: Retrieves external information using the DuckDuckGo search API.

## Prerequisites
- Python 3.12
- A valid GROQ API key (sign up at [https://console.groq.com/keys](https://console.groq.com/keys) for access).
- The `genai_intro.pdf` file placed in the `Doc/` directory.
- The `faiss_index` s placed in the `Doc/` directory.

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ShubhamChougale01/genai-bot.git
   cd genai-bot

2. **Install Dependencies**:
   Create a virtual environment and install required packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   The `requirements.txt` includes:
   ```
streamlit
python-dotenv
langchain
langchain_groq
langchain_community
langchain_core
faiss-cpu
sentence-transformers
langchain-huggingface==0.0.3
pypdf
duckduckgo-search
requests
tqdm
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root with your GROQ API key:
   ```plaintext
   GROQ_API_KEY=your_groq_api_key
   ```

4. **Prepare the PDF**:
   Ensure `genai_intro.pdf` is in the `Doc/` directory. The path is hardcoded as `/Users/shubham/genai_bot/Doc/genai_intro.pdf` in `Document_QA.py`. Update this path if needed or move the file accordingly.

5. **Run the Application**:
   Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage
- Access the chatbot at `http://localhost:8501` in your browser.
- Type questions in the chat input, such as:
  - "What is Generative AI?"
  - "List one challenge of GenAI."
  - "What is 45 × 19?"
  - "Who is the Prime Minister of India?"
- The bot uses a LangChain agent to route queries to the appropriate tool:
  - **PDF Q&A**: For questions about Generative AI concepts or challenges.
  - **Calculator**: For arithmetic operations.
  - **Web Search**: For general knowledge queries for web search.

## Project Structure
- `app.py`: Streamlit UI for the chatbot interface.
- `main.py`: Initializes the LangChain agent, tools, and memory for query handling.
- `tools/`: Contains tool implementations:
  - `Document_QA.py`: Loads and queries the PDF using RAG.
  - `calculator.py`: Handles arithmetic operations.
  - `web_search.py`: Performs web searches via DuckDuckGo.
- `Doc/`: Stores `genai_intro.pdf` and the FAISS index (`faiss_index`).
- `.env`: Environment variables (e.g., GROQ API key).
- `requirements.txt`: Python dependencies.
- `.gitignore`: Ignores virtual environments and temporary files.

## Running Test Queries
To test the bot programmatically, run:
```bash
python main.py
```
This executes the test queries defined in `main.py`:
- "What is Generative AI?"
- "List one challenge of GenAI."
- "What is 45 × 19?" (Expected: Result: 855)
- "Who is the Prime Minister of India?" (Expected: Narendra Modi, as of August 2025)

## Notes
- **Web Search**: Relies on DuckDuckGo; ensure internet connectivity. If initialization fails, the tool returns an error message.
- **Verbose Output**: The agent’s `verbose=True` setting logs tool selection and reasoning to the console, useful for debugging.
- **LLM Used:** `gemma2-9b-it` from Groq Cloud API.
