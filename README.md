# Project: Context-Supported AI Response System with RAG

## Overview
This project is a conversational AI application designed to answer user queries using a multilingual large language model (LLM) called **Llama 3.2**. The system leverages a combination of advanced natural language processing (NLP) tools and a vector database to provide contextual, accurate, and efficient responses. The AI can maintain a history of conversations and use this history alongside relevant external documents to generate meaningful answers.

---

## Features
1. **Contextual Query Handling**:
   - Answers questions using a combination of conversation history and a vector-based document retrieval system.
   - If a question is unrelated to the context or history, the system gracefully responds with "pass."

2. **Multilingual LLM Integration**:
   - Utilizes **Llama 3.2**, a state-of-the-art multilingual large language model for text input/output operations.

3. **Conversation Memory**:
   - Maintains a history of the last 5 exchanges between the user and the model to enrich future responses.

4. **Real-Time Web Interface**:
   - Built with **NiceGUI** to provide a clean and user-friendly web application for interaction.

5. **PDF Document Processing**:
   - Parses and splits PDF documents into manageable chunks for efficient retrieval.

6. **Efficient Database Management**:
   - Uses **Chroma Vector Database** to store and retrieve embeddings of textual data.

7. **Logging**:
   - Logs user queries and AI responses for debugging and tracking purposes.

8. **Real-Time Conversation Contextualization**:
   - Integrates contextual memory and external document retrieval in real-time for more accurate responses.

9. **Adaptive Language Model Tuning**:
   - Supports custom fine-tuning for more specialized domains to adapt the model to particular use cases.

10. **Interactive User Feedback**:
    - Users can provide feedback on answers, which helps improve future responses by adjusting memory.

---

## Technologies Used
### **Language Model and NLP Tools**
- **Llama 3.2**:
  - A collection of pretrained and instruction-tuned generative models in 1B and 3B sizes.
  - Optimized for multilingual dialogue, agentic retrieval, and summarization tasks.
  - Outperforms many open-source and closed chat models on industry benchmarks.
- **LangChain**:
  - For building the conversational pipeline, including prompt templates and retrieval-based queries.
- **Ollama Embeddings**:
  - Converts text into numerical representations for similarity searches.

### **Database and Document Management**
- **Chroma Vector Database**:
  - Stores embeddings of text documents for fast semantic search.
- **PyPDFDirectoryLoader**:
  - Extracts text content from PDF files.
- **Recursive Character Text Splitter**:
  - Splits large text into manageable chunks for better search and retrieval.
- **External File Format Support**:
  - Plans for future support for additional file types such as DOCX, TXT, and HTML.

### **Web Interface**
- **NiceGUI**:
  - A Python-based framework for creating modern web interfaces.
  - Implements real-time user interaction with AI.
- **Real-Time Conversation Handling**:
  - The web interface is optimized to handle live interactions, offering seamless conversation flow.

### **Other Utilities**
- **Argparse**:
  - Handles command-line arguments for flexibility in usage.
- **Logging**:
  - Tracks user inputs and model outputs in a structured log file.
- **Datetime and Asyncio**:
  - Used for logging timestamps and managing real-time asynchronous tasks.
- **User Feedback Mechanism**:
  - A feedback loop that allows users to rate answers, improving response generation.

---

## How It Works
1. **PDF Processing**:
   - Upload PDF documents to the `data` directory.
   - The system processes and splits documents into chunks with metadata, storing them in the Chroma database.

2. **Querying**:
   - Users input a query through the web interface or command-line.
   - The query is converted into embeddings, and the most relevant document chunks are retrieved.

3. **Conversational Memory**:
   - The AI uses the last 5 exchanges to add depth and context to its answers.

4. **Response Generation**:
   - Combines retrieved documents and conversation history to craft a response using the Llama 3.2 model.

5. **Logging**:
   - All interactions are logged for later analysis.

6. **Interactive Feedback**:
   - Users can rate responses or provide feedback, which can influence future model behavior and improve the system’s adaptability.

---

## Model Details: Llama 3.2
The Llama 3.2 collection of multilingual large language models (LLMs) is a collection of pretrained and instruction-tuned generative models in 1B and 3B sizes (text in/text out). The Llama 3.2 instruction-tuned text-only models are optimized for multilingual dialogue use cases, including agentic retrieval and summarization tasks. They outperform many of the available open-source and closed chat models on common industry benchmarks.

---

## Getting Started
### Prerequisites
- Python 3.8 or later
- Required Python packages (install via `pip install -r requirements.txt`):
  - langchain
  - nicegui
  - chromadb
  - PyPDF2

### Running the Application
1. **Populate the Database**:
   - Place your PDF documents in the `data` directory.
   - Run `populate_database.py` to process and store document embeddings.

2. **Start the Web Interface**:
   - Run `ui_utils.py` to launch the NiceGUI-based web app.
   - Access the app at `http://localhost:8080`.

3. **Command-Line Query**:
   - Run `main.py` with a query argument:  
     `python main.py "Your query here"`

4. **User Feedback**:
   - Provide ratings or comments on responses directly from the web interface.

---

## Example Use Cases
1. **Contextual Question Answering**:
   - The AI retrieves relevant content from PDFs to answer questions accurately.
2. **Multilingual Conversations**:
   - Supports queries and responses in multiple languages.
3. **Agentic Retrieval**:
   - Summarizes large documents and provides concise answers.
4. **Interactive Feedback Loop**:
   - Users can help fine-tune future responses by providing feedback.

---

## Future Improvements
- Add support for additional file types (e.g., DOCX, TXT).
- Enhance multilingual capabilities with more tuned models.
- Implement user-specific memory across sessions.
- Refine user feedback mechanism to dynamically improve the system.

---

## Contact
For questions, suggestions, or contributions, feel free to reach out at ekerinfo@gmail.com.
