from main import query_rag

def test_cv_name():
    assert query_rag(
        "What is the name of the person in the CV? (Answer with the full name and nothing else)"
    ) == "Muhammed Mustafa Savar"

def test_detail():
    assert query_rag(
        " Is Tailwind.css one of the skills of the person in the CV? (Answer with 'Yes' or 'No')"
    ) == "Yes"

if __name__ == "__main__":
    test_cv_name()
    test_detail()
