import pytest
from income_tax import taxable_income, tax_due, refund_status

"""
test_income_tax.py
Complete test suite providing >90% (100%) Code and Branch Coverage
for the income tax calculation module.
"""

# ============================================================================
# Starter Example Test Cases
# ============================================================================

def test_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000

def test_below_exemption():
    assert tax_due(200000, 30) == 0


# ============================================================================
# Additional Comprehensive Test Cases for 100% Code & Branch Coverage
# ============================================================================

# --- taxable_income tests ---

def test_taxable_income_negative_gross():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-5000, "new", 0)

def test_taxable_income_new_regime_taxable_negative():
    assert taxable_income(50000, "new", 0) == 0

def test_taxable_income_new_regime_taxable_zero_boundary():
    assert taxable_income(75000, "new", 0) == 0

def test_taxable_income_old_regime_investments_capped():
    assert taxable_income(800000, "old", 250000) == 600000

def test_taxable_income_old_regime_investments_boundary():
    assert taxable_income(400000, "old", 150000) == 200000

def test_taxable_income_old_regime_investments_uncapped():
    assert taxable_income(500000, "old", 80000) == 370000

def test_taxable_income_old_regime_zero_investments():
    assert taxable_income(200000, "old", 0) == 150000

def test_taxable_income_old_regime_taxable_negative():
    assert taxable_income(100000, "old", 100000) == 0

def test_taxable_income_unknown_regime():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(600000, "corporate", 50000)


# --- tax_due tests ---

def test_tax_due_negative_taxable():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-500, 30)

def test_tax_due_super_senior_exact_age_80_exempt():
    assert tax_due(400000, 80) == 0

def test_tax_due_super_senior_boundary_exempt():
    assert tax_due(500000, 85) == 0

def test_tax_due_super_senior_slab_one():
    assert tax_due(650000, 82) == 7500

def test_tax_due_super_senior_slab_two():
    assert tax_due(850000, 80) == 32500

def test_tax_due_senior_exact_age_60_exempt():
    assert tax_due(200000, 60) == 0

def test_tax_due_senior_boundary_age_79_exempt():
    assert tax_due(300000, 79) == 0

def test_tax_due_senior_slab_one():
    assert tax_due(420000, 65) == 6000

def test_tax_due_senior_slab_two():
    assert tax_due(650000, 70) == 32500

def test_tax_due_general_boundary_age_59_exempt():
    assert tax_due(250000, 59) == 0

def test_tax_due_general_slab_one_boundary():
    assert tax_due(500000, 30) == 12500

def test_tax_due_general_slab_two():
    assert tax_due(600000, 35) == 32500


# --- refund_status tests ---

def test_refund_status_refund_on_time():
    assert refund_status(60000, 40000, True) == "refund"

def test_refund_status_refund_delayed():
    assert refund_status(60000, 40000, False) == "refund delayed"

def test_refund_status_pay_balance_on_time():
    assert refund_status(40000, 60000, True) == "pay balance"

def test_refund_status_pay_balance_penalty():
    assert refund_status(40000, 60000, False) == "pay balance with penalty"

def test_refund_status_settled_on_time():
    assert refund_status(50000, 50000, True) == "settled"

def test_refund_status_settled_delayed():
    assert refund_status(50000, 50000, False) == "settled"
