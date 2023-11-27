from streamlit.testing.v1 import AppTest


def test_postal_code():
    at = AppTest.from_file("main.py").run()
    at.text_input("postal_code").input("260004").run()
    assert not at.exception
