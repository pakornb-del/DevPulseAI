import re

def scrub_pii_data(text: str) -> str:
    """Detects and masks sensitive PII data such as phone numbers and emails."""
    if not isinstance(text, str):
        return text
        
    # Mask Email addresses (e.g. user@domain.com -> u***@domain.com)
    def mask_email(match):
        email = match.group(0)
        parts = email.split('@')
        if len(parts) == 2:
            name, domain = parts
            if len(name) > 1:
                masked_name = name[0] + "***"
            else:
                masked_name = "*"
            return f"{masked_name}@{domain}"
        return email

    # Regular expression for email
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    text = re.sub(email_pattern, mask_email, text)
    
    # Mask Thai Phone Numbers (e.g. 081-234-5678 -> 081-XXX-XX78 or 0812345678 -> 081XXXXX78)
    # Match patterns with dashes or spaces
    phone_pattern_dash = r'\b(0[1-9]\d?)[- ]?(\d{3})[- ]?(\d{4})\b'
    def mask_phone(match):
        prefix = match.group(1)
        mid = match.group(2)
        suffix = match.group(3)
        # Mask the middle numbers and part of suffix
        return f"{prefix}-XXX-XX{suffix[-2:]}"
        
    text = re.sub(phone_pattern_dash, mask_phone, text)
    
    return text

def clean_pii_context(raw_data):
    """Recursively traverses a nested data structure (dict/list) and scrubs PII from string values."""
    if isinstance(raw_data, dict):
        return {k: clean_pii_context(v) for k, v in raw_data.items()}
    elif isinstance(raw_data, list):
        return [clean_pii_context(item) for item in raw_data]
    elif isinstance(raw_data, str):
        return scrub_pii_data(raw_data)
    else:
        return raw_data
