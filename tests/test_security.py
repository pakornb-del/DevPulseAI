import pytest
from app.security import scrub_pii_data, clean_pii_context

def test_scrub_pii_emails():
    # Test typical emails
    text = "Please contact support@example.com or lead.dev@team.org for info."
    masked = scrub_pii_data(text)
    assert "s***@example.com" in masked
    assert "l***@team.org" in masked
    assert "support@example.com" not in masked

def test_scrub_pii_phones():
    # Test Thai phone formats
    text1 = "My number is 081-234-5678."
    text2 = "Call me at 0891234567."
    assert "081-XXX-XX78" in scrub_pii_data(text1)
    # Masking with or without dashes is parsed: 0891234567 -> prefix '089', mid '123', suffix '4567' -> masked: 089-XXX-XX67
    assert "089-XXX-XX67" in scrub_pii_data(text2)

def test_clean_pii_nested_structures():
    # Test dictionary scrubbing
    data = {
        "email": "pete@example.com",
        "details": {
            "phone": "086-765-4321",
            "remarks": "Pete can be reached at pete@example.com or 086-765-4321."
        },
        "score": 4.5
    }
    clean_data = clean_pii_context(data)
    assert clean_data["email"] == "p***@example.com"
    assert clean_data["details"]["phone"] == "086-XXX-XX21"
    assert "p***@example.com" in clean_data["details"]["remarks"]
    assert "086-XXX-XX21" in clean_data["details"]["remarks"]
    assert clean_data["score"] == 4.5
