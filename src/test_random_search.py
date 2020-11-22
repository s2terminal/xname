from src.random_search import search_ary

def test_search_ary():
    original_name = "sara"
    xname = search_ary(original_name)[0]
    assert len(original_name) == len(xname)
