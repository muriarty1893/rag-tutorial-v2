from main import query_rag
from langchain_community.llms.ollama import Ollama

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def test_cv_name():
    assert query_and_validate(
        question="What is the name of the person in the CV? (Answer with the full name and nothing else)",
        expected_response="Murat Eker",  # Buraya CV'deki kişinin adı yazılmalı
    )


def test_cv_education():
    assert query_and_validate(
        question="Which university did the person graduate from? (Answer with the university name only)",
        expected_response="Adana Alparslan Türkeş Science and Technology University",  # CV'ye göre doğru yanıtı girin
    )


def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="llama3.2:latest")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )

if __name__ == "__main__":
    test_cv_name()
    test_cv_education()
