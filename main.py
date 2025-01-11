import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function
from log_utils import log_interaction


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

conversation_history = []

def is_cv_related(question: str) -> bool:
    control_model = OllamaLLM(model="gemma2:2b")
    prompt = f"Is this question related to a CV or job application? Answer 'Yes' or 'No': {question}"
    response = control_model.invoke(prompt).strip().lower()
    return "yes" in response

def query_rag(query_text: str):
    global conversation_history

    if not is_cv_related(query_text):
        print("\n---\nResponse: This question is not related to CVs or job applications.\n")
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
    MAX_HISTORY = 2
    conversation_history = conversation_history[-MAX_HISTORY:]

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"\n---\nResponse: {response_text}\nSources: {sources}\n"
    print(formatted_response)
    
    return response_text

def get_exp_sum():
    global conversation_history

    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    query_text = "Provide a summary of the experience section in the provided document by 2-3 sentences."

    results = db.similarity_search_with_score(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    history_text = "\n".join([f"User: {entry['user']}\nLLM: {entry['llm']}" for entry in conversation_history])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(history=history_text, context=context_text, question=query_text)

    model = OllamaLLM(model="llama3.2:latest")
    response_text = model.invoke(prompt)

    conversation_history.append({"user": query_text, "llm": response_text})
    MAX_HISTORY = 2
    conversation_history = conversation_history[-MAX_HISTORY:]

    print(f"\n---\nExperience Summary: {response_text}\n")
    return response_text

def get_proj_sum():
    global conversation_history

    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    query_text = "Provide a summary of the projects section in the provided document by 2-3 sentences."

    results = db.similarity_search_with_score(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    history_text = "\n".join([f"User: {entry['user']}\nLLM: {entry['llm']}" for entry in conversation_history])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(history=history_text, context=context_text, question=query_text)

    model = OllamaLLM(model="llama3.2:latest")
    response_text = model.invoke(prompt)

    conversation_history.append({"user": query_text, "llm": response_text})
    MAX_HISTORY = 2
    conversation_history = conversation_history[-MAX_HISTORY:]

    print(f"\n---\nProject Summary: {response_text}\n")
    return response_text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    response_text = query_rag(query_text)
    log_interaction(query_text, response_text)

if __name__ == "__main__":
    main()
