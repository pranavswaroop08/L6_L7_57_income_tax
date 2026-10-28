# L6_L7_57 – Income Tax Calculator

**Lab 6: Code and Branch Coverage Analysis**  
**Student Name:** Pranav Swaroop  
**SRN:** PES2UG24CS365  
**Course:** Software Engineering Laboratory (UE24CS351A)  

---

## Overview

This repository contains the solution and deliverables for **Lab 6: Code and Branch Coverage Analysis**. The target application under test is `income_tax.py`, which computes net taxable income under two regimes (New vs. Old), calculates progressive tax liabilities according to three age brackets (Super Senior, Senior Citizen, and General), and evaluates refund/settlement statuses.

---

## Deliverables Summary

| File | Description | Coverage Target | Achieved |
|------|-------------|-----------------|----------|
| `income_tax.py` | Target module under test | – | – |
| `test_income_tax.py` | Complete test suite (starter + full cases) | >90% Coverage | **100%** Line / **100%** Branch |
| `CodeCoverageTest_income_tax.py` | Targeted test suite for Code Coverage | >90% Line Coverage | **100%** Line Coverage |
| `BranchCoverageTest_income_tax.py` | Targeted test suite for Branch Coverage | >90% Branch Coverage | **100%** Branch Coverage |
| `initial_coverage_report.png` | Baseline initial test coverage terminal screenshot | Baseline Reference | 38% Line / 33% Branch |
| `code_coverage_report.png` | Code coverage terminal output screenshot | Minimum 90% | **100%** |
| `branch_coverage_report.png` | Branch coverage terminal output screenshot | Minimum 90% | **100%** |
| `PES2UG24CS365_Lab_6.pdf` | Comprehensive formal lab report | Evaluation Rubric | Complete |

---

## Coverage Metrics Comparison

| Metric | Initial Baseline (`test_income_tax.py`) | Code Coverage Suite (`CodeCoverageTest_income_tax.py`) | Branch Coverage Suite (`BranchCoverageTest_income_tax.py`) |
|--------|----------------------------------------|-------------------------------------------------------|-----------------------------------------------------------|
| **Statements** | 39 | 39 | 39 |
| **Missed Statements** | 24 | **0** | **0** |
| **Line Coverage** | 38% | **100%** | **100%** |
| **Branches** | 28 | 28 | 28 |
| **Partial / Missed Branches** | 7 | 0 | **0** |
| **Branch Coverage** | 33% | 100% | **100%** |
| **Tests Passed** | 2 passed | 16 passed | 29 passed |

---

## Running the Tests & Coverage

### 1. Install Dependencies
```bash
pip install coverage pytest
```

### 2. Run Code Coverage (Line Coverage)
```bash
coverage run -m pytest CodeCoverageTest_income_tax.py
coverage report -m
```

### 3. Run Branch Coverage
```bash
coverage run --branch -m pytest BranchCoverageTest_income_tax.py
coverage report -m
```

### 4. Run Full Test Suite
```bash
coverage run --branch -m pytest test_income_tax.py
coverage report -m
```
