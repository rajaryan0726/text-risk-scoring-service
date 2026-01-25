from app.engine import analyze_text

def test_determinism():
    text = "This is a scam message"
    assert analyze_text(text) == analyze_text(text)

def test_empty_input():
    result = analyze_text("")
    assert result["errors"]["error_code"] == "EMPTY_INPUT"

def test_high_risk():
    result = analyze_text("kill and scam")
    assert result["risk_category"] == "HIGH"






def test_no_substring_match():
    result = analyze_text("studies")
    assert result["risk_category"] == "LOW"


def test_category_saturation_cap():
    text = "kill kill kill kill kill"
    result = analyze_text(text)
    assert result["risk_score"] <= 0.6


def test_same_input_determinism():
    assert analyze_text("scam") == analyze_text("scam")
