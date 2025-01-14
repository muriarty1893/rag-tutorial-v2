from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Below is a conversation history between a user and an assistant. Use the history and the provided context to answer the question.:

Conversation History:
{history}

---

Context:
{context}

---

Answer the question based on the above context and history, as if you are the person in the above text: {question}
"""

def is_cv_related(question):
    control_model = OllamaLLM(model="gemma2:2b")
    prompt = f"Is this question related to a CV or job application? Answer 'Yes' or 'No': {question}"
    response = control_model.invoke(prompt).strip().lower()
    return "yes" in response

def query_rag(query_text: str, conversation_history=[]):
    if not is_cv_related(query_text):
        return "This question is not related to CVs or job applications."

    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    results = db.similarity_search_with_score(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    history_text = "\n".join([f"User: {entry['user']}\nLLM: {entry['llm']}" for entry in conversation_history])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(history=history_text, context=context_text, question=query_text)

    model = OllamaLLM(model="llama3.2:latest")
    response_text = model.invoke(prompt)

    conversation_history.append({"user": query_text, "llm": response_text})
    conversation_history = conversation_history[-2:]

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    return response_text

def get_summary(query_text: str):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_score(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(history="", context=context_text, question=query_text)

    model = OllamaLLM(model="llama3.2:latest")
    response_text = model.invoke(prompt)

    return response_text


def get_exp_sum():
    return get_summary("Provide a summary of the experience section in the provided document by 2-3 sentences.")

def get_proj_sum():
    return get_summary("Provide a summary of the projects section in the provided document by 2-3 sentences.")
