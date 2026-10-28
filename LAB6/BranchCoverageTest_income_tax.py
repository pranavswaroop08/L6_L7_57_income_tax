import pytest
from income_tax import taxable_income, tax_due, refund_status

"""
BranchCoverageTest_income_tax.py
Comprehensive Branch Coverage Test Suite for income_tax.py.
Targets 100% Branch Coverage by validating every decision path,
Boolean condition (True and False), and boundary/edge case:
- gross < 0 (True/False)
- regime == 'new' vs 'old' vs invalid (all branches)
- investments > 150000 (True, False, and exact boundary == 150000)
- taxable < 0 (True, False, and exact boundary == 0)
- taxable < 0 in tax_due (True/False)
- age categories: age >= 80, 60 <= age < 80, age < 60 (with boundaries 80, 79, 60, 59)
- taxable <= exempt (True: strictly less, exact equality; False)
- slab <= 250000 (True: strictly less, exact boundary == 250000; False: strictly greater)
- tax calculations across all 3 age categories for both slabs
- refund_status: difference > 0, difference < 0, difference == 0, with filed_on_time True/False
"""

# ============================================================================
# Branch Coverage Tests for taxable_income(gross, regime, investments)
# ============================================================================

def test_taxable_income_negative_gross():
    """Branch: gross < 0 -> True (raises ValueError)"""
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_taxable_income_new_regime_standard():
    """Branch: regime == 'new' -> True, taxable > 0 (normal path)"""
    # 500,000 - 75,000 = 425,000
    assert taxable_income(500000, "new", 0) == 425000


def test_taxable_income_new_regime_taxable_below_zero():
    """Branch: regime == 'new' -> True, taxable < 0 -> True (returns 0)"""
    # 50,000 - 75,000 = -25,000 (< 0) -> returns 0
    assert taxable_income(50000, "new", 0) == 0


def test_taxable_income_new_regime_taxable_exactly_zero():
    """Branch: regime == 'new' -> True, taxable == 0 boundary (returns 0)"""
    # 75,000 - 75,000 = 0 (not < 0) -> returns 0
    assert taxable_income(75000, "new", 0) == 0


def test_taxable_income_old_regime_investments_above_limit():
    """Branch: regime == 'old', investments > 150000 -> True (capped at 150000)"""
    # deduction = 50,000 + 150,000 = 200,000; taxable = 800,000 - 200,000 = 600,000
    assert taxable_income(800000, "old", 250000) == 600000


def test_taxable_income_old_regime_investments_exact_limit():
    """Branch: regime == 'old', investments == 150000 boundary -> False"""
    # deduction = 50,000 + 150,000 = 200,000; taxable = 400,000 - 200,000 = 200,000
    assert taxable_income(400000, "old", 150000) == 200000


def test_taxable_income_old_regime_investments_below_limit():
    """Branch: regime == 'old', investments < 150000 -> False"""
    # deduction = 50,000 + 80,000 = 130,000; taxable = 500,000 - 130,000 = 370,000
    assert taxable_income(500000, "old", 80000) == 370000


def test_taxable_income_old_regime_zero_investments():
    """Branch: regime == 'old', zero investments edge case"""
    # deduction = 50,000 + 0 = 50,000; taxable = 200,000 - 50,000 = 150,000
    assert taxable_income(200000, "old", 0) == 150000


def test_taxable_income_old_regime_taxable_below_zero():
    """Branch: regime == 'old', taxable < 0 -> True (returns 0)"""
    # deduction = 50,000 + 100,000 = 150,000; gross = 100,000 -> taxable = -50,000 -> returns 0
    assert taxable_income(100000, "old", 100000) == 0


def test_taxable_income_unknown_regime():
    """Branch: regime not 'new' and not 'old' -> else (raises ValueError)"""
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(600000, "custom", 50000)


# ============================================================================
# Branch Coverage Tests for tax_due(taxable, age)
# ============================================================================

def test_tax_due_negative_taxable():
    """Branch: taxable < 0 -> True (raises ValueError)"""
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-1, 30)


# --- Age Category: Super Senior (age >= 80, exemption = 500,000) ---

def test_tax_due_super_senior_exact_age_80_exempt():
    """Branch: age == 80 boundary, taxable <= exempt (strictly less)"""
    assert tax_due(400000, 80) == 0


def test_tax_due_super_senior_taxable_equals_exempt():
    """Branch: age > 80, taxable == exempt boundary (500,000 == 500,000)"""
    assert tax_due(500000, 85) == 0


def test_tax_due_super_senior_slab_one():
    """Branch: age >= 80, taxable > exempt, slab <= 250000"""
    # exempt = 500000, taxable = 650000 -> slab = 150000 <= 250000 -> 150000 * 5 // 100 = 7500
    assert tax_due(650000, 82) == 7500


def test_tax_due_super_senior_slab_two():
    """Branch: age >= 80, taxable > exempt, slab > 250000"""
    # exempt = 500000, taxable = 850000 -> slab = 350000 > 250000
    # 12500 + (350000 - 250000) * 20 // 100 = 12500 + 20000 = 32500
    assert tax_due(850000, 80) == 32500


# --- Age Category: Senior Citizen (60 <= age < 80, exemption = 300,000) ---

def test_tax_due_senior_exact_age_60_exempt():
    """Branch: age == 60 boundary, taxable < exempt"""
    assert tax_due(200000, 60) == 0


def test_tax_due_senior_upper_boundary_age_79_exempt():
    """Branch: age == 79 boundary, taxable == exempt (300,000 == 300,000)"""
    assert tax_due(300000, 79) == 0


def test_tax_due_senior_slab_one():
    """Branch: 60 <= age < 80, slab <= 250000"""
    # exempt = 300000, taxable = 420000 -> slab = 120000 -> 120000 * 5 // 100 = 6000
    assert tax_due(420000, 65) == 6000


def test_tax_due_senior_slab_two():
    """Branch: 60 <= age < 80, slab > 250000"""
    # exempt = 300000, taxable = 650000 -> slab = 350000
    # 12500 + 100000 * 20 // 100 = 32500
    assert tax_due(650000, 70) == 32500


# --- Age Category: General Citizen (age < 60, exemption = 250,000) ---

def test_tax_due_general_boundary_age_59_exempt():
    """Branch: age == 59 boundary, taxable <= exempt"""
    assert tax_due(250000, 59) == 0


def test_tax_due_general_taxable_below_exempt():
    """Branch: age < 60, taxable < exempt"""
    assert tax_due(100000, 25) == 0


def test_tax_due_general_slab_one_exact_boundary():
    """Branch: age < 60, slab == 250000 exact boundary"""
    # exempt = 250000, taxable = 500000 -> slab = 250000 -> 250000 * 5 // 100 = 12500
    assert tax_due(500000, 30) == 12500


def test_tax_due_general_slab_two():
    """Branch: age < 60, slab > 250000"""
    # exempt = 250000, taxable = 600000 -> slab = 350000 -> 12500 + 20000 = 32500
    assert tax_due(600000, 35) == 32500


# ============================================================================
# Branch Coverage Tests for refund_status(tax_paid, tax_due_amount, filed_on_time)
# ============================================================================

def test_refund_status_refund_filed_on_time():
    """Branch: difference > 0, filed_on_time == True -> 'refund'"""
    assert refund_status(60000, 40000, True) == "refund"


def test_refund_status_refund_filed_late():
    """Branch: difference > 0, filed_on_time == False -> 'refund delayed'"""
    assert refund_status(60000, 40000, False) == "refund delayed"


def test_refund_status_pay_balance_filed_on_time():
    """Branch: difference < 0, filed_on_time == True -> 'pay balance'"""
    assert refund_status(40000, 60000, True) == "pay balance"


def test_refund_status_pay_balance_filed_late():
    """Branch: difference < 0, filed_on_time == False -> 'pay balance with penalty'"""
    assert refund_status(40000, 60000, False) == "pay balance with penalty"


def test_refund_status_settled_on_time():
    """Branch: difference == 0, filed_on_time == True -> 'settled'"""
    assert refund_status(50000, 50000, True) == "settled"


def test_refund_status_settled_late():
    """Branch: difference == 0, filed_on_time == False -> 'settled'"""
    assert refund_status(50000, 50000, False) == "settled"
