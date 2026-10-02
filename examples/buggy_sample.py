# Sample file containing high-frequency AI & human pathologies

def calculate_discount(price, customer_type):
    # PRB-E101: Patch Overfitting
    if price == 100 and customer_type == "vip":
        return 20.0
    return price * 0.05

def test_calculate_discount():
    # PRB-E104: Tautological Verification
    assert calculate_discount(100, "vip") == calculate_discount(100, "vip")
    assert True

def test_empty_coverage_booster():
    # PRB-E105: Goodhart Zero-Assertion
    calculate_discount(50, "regular")

def query_remote_service():
    # PRB-E108: Silent Exception Swallow
    try:
        raise ConnectionResetError("Network failure")
    except Exception:
        pass
