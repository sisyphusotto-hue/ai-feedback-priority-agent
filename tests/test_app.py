from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_app_analyzes_feedback_after_button_click():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.run()

    app.text_area[0].input("页面报错无法提交\n希望增加深色模式")
    app.button[0].click().run()

    assert app.metric[0].value == "2"
    assert "优先级建议" in [header.value for header in app.subheader]
