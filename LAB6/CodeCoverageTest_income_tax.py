import pytest
from income_tax import taxable_income, tax_due, refund_status

"""
CodeCoverageTest_income_tax.py
Test suite designed to achieve 100% Line (Statement) Coverage for income_tax.py.
Covers every executable line across taxable_income, tax_due, and refund_status.
"""

# ==========================================
# Tests for taxable_income
# ==========================================

def test_taxable_income_negative_gross():
    """Hits line 3: raise ValueError('invalid income')"""
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-10000, "new", 0)


def test_taxable_income_new_regime_positive():
    """Hits line 5 (deduction = 75000) and line 15 (return taxable)"""
    assert taxable_income(500000, "new", 0) == 425000


def test_taxable_income_new_regime_zero_taxable():
    """Hits line 14: return 0 when taxable < 0"""
    assert taxable_income(50000, "new", 0) == 0


def test_taxable_income_old_regime_investments_capped():
    """Hits lines 6, 7, 8, 9: investments > 150000 capped at 150000"""
    assert taxable_income(600000, "old", 200000) == 400000


def test_taxable_income_old_regime_investments_uncapped():
    """Hits line 9 with uncapped investments"""
    assert taxable_income(300000, "old", 50000) == 200000


def test_taxable_income_unknown_regime():
    """Hits line 11: raise ValueError('unknown regime')"""
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "corporate", 0)


# ==========================================
# Tests for tax_due
# ==========================================

def test_tax_due_negative_taxable():
    """Hits line 20: raise ValueError('invalid amount')"""
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-500, 30)


def test_tax_due_super_senior_exempt():
    """Hits lines 21, 22, 27, 28: age >= 80, taxable <= 500000"""
    assert tax_due(400000, 85) == 0


def test_tax_due_senior_exempt():
    """Hits lines 23, 24, 27, 28: age >= 60, taxable <= 300000"""
    assert tax_due(250000, 65) == 0


def test_tax_due_general_first_slab():
    """Hits lines 25, 26, 29, 30, 31: slab <= 250000"""
    # exempt = 250000, taxable = 350000 -> slab = 100000 -> tax = 5000
    assert tax_due(350000, 30) == 5000


def test_tax_due_general_second_slab():
    """Hits line 32: slab > 250000"""
    # exempt = 250000, taxable = 600000 -> slab = 350000 -> tax = 12500 + 20000 = 32500
    assert tax_due(600000, 30) == 32500


# ==========================================
# Tests for refund_status
# ==========================================

def test_refund_status_refund_on_time():
    """Hits line 39: difference > 0 and filed_on_time == True"""
    assert refund_status(50000, 30000, True) == "refund"


def test_refund_status_refund_delayed():
    """Hits line 40: difference > 0 and filed_on_time == False"""
    assert refund_status(50000, 30000, False) == "refund delayed"


def test_refund_status_pay_balance_on_time():
    """Hits line 43: difference < 0 and filed_on_time == True"""
    assert refund_status(30000, 50000, True) == "pay balance"


def test_refund_status_pay_balance_with_penalty():
    """Hits line 44: difference < 0 and filed_on_time == False"""
    assert refund_status(30000, 50000, False) == "pay balance with penalty"


def test_refund_status_settled():
    """Hits line 45: difference == 0"""
    assert refund_status(40000, 40000, True) == "settled"
