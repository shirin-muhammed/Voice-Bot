import corrections


def test_learned_word_is_replaced_whole_word_only():
    assert corrections.apply("Shirin said hi", {"Shirin": "Shirin M."}) == "Shirin M. said hi"
    assert corrections.apply("shirinxy", {"shirin": "X"}) == "shirinxy"


def test_learn_records_substitution_and_vocabulary():
    data = corrections.learn("send it to Sherin today", "send it to Shirin today", {"corrections": {}, "vocabulary": []})
    assert data["corrections"] == {"Sherin": "Shirin"}
    assert "Shirin" in data["vocabulary"]


def test_initial_prompt_uses_vocabulary():
    assert corrections.initial_prompt({"vocabulary": ["Shirin", "Kochi"]}) == "Shirin, Kochi"
