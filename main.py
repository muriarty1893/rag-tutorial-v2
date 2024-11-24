import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function
from log_utils import log_interaction

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context, if the question is not about the below context, answer with "pass.":

{context}

---

Answer the question based on the above context, as if you are the person in the above text give information about (if question includes "aaa" at the start of the sentence, then answer quickly and short as possible):  {question}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    response_text = query_rag(query_text)
    
    log_interaction(query_text, response_text)

def query_rag(query_text: str):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = OllamaLLM(model="llama3.2:latest")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"\n---\nResponse: {response_text}\nSources: {sources}\n"
    print(formatted_response)
    return response_text

if __name__ == "__main__":
    main()
