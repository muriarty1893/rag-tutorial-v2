from main import query_rag

def test_cv_name():
    assert query_rag(
        "What is the name of the person in the CV? (Answer with the full name and nothing else)"
    ) == "Murat Eker"

def test_not_cv_related():
    assert query_rag("What is the capital of France?") == "This question is not related to CVs or job applications."

if __name__ == "__main__":
    test_cv_name()
    test_not_cv_related()
