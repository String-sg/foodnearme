from streamlit.testing.v1 import AppTest


def test_postal_code_pass():
    at = AppTest.from_file("main.py").run()
    at.text_input("postal_code").input("260004").run()
    assert not at.exception


def test_postal_code_fail():
    at = AppTest.from_file("main.py").run()
    at.text_input("postal_code").input("whatever").run()
    assert at.warning[0].value == "Postal code must be 6 digits."
