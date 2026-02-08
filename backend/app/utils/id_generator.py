import uuid


def generate_id(prefix: str) -> str:
    """Generate a unique ID with the given prefix.

    Uses UUID4 hex suffix truncated to match expected format lengths:
      - CUST-XXXXXX, ALERT-XXXXXX, CASE-XXXXXX, DOC-XXXXXX  → 6 chars
      - TXN-XXXXXXX                                           → 7 chars
      - ACC-XXXXXXXXX                                          → 9 chars
      - ORG-XXXX, USR-XXXX                                     → 4 chars
    """
    suffix_lengths = {
        "CUST": 6,
        "ALERT": 6,
        "CASE": 6,
        "DOC": 6,
        "TXN": 7,
        "ACC": 9,
        "ORG": 4,
        "USR": 4,
    }
    length = suffix_lengths.get(prefix, 6)
    suffix = uuid.uuid4().hex[:length].upper()
    return f"{prefix}-{suffix}"
