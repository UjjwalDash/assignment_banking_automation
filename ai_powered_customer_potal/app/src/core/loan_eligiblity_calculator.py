class LoanEligibilityCalculator:
    WEIGHTS = {
        "credit_score": 0.40,
        "debt_to_income": 0.20,
        "income_stability": 0.15,
        "loan_factors": 0.10,
        "employment_risk": 0.10,
        "risk_factors": 0.05
    }

    def __init__(self, age, employment_type, residence_type,
                 monthly_income, other_income, total_emi, savings,
                 bank_balance, credit_score, existing_loans,
                 past_defaults, credit_utilization, loan_amount,
                 loan_type, down_payment, collateral,
                 legal_issues, guarantor):
        self.age = age
        self.employment_type = employment_type
        self.residence_type = residence_type
        self.monthly_income = monthly_income
        self.other_income = other_income
        self.total_emi = total_emi
        self.savings = savings
        self.bank_balance = bank_balance
        self.credit_score = credit_score
        self.existing_loans = existing_loans
        self.past_defaults = past_defaults
        self.credit_utilization = credit_utilization
        self.loan_amount = loan_amount
        self.loan_type = loan_type
        self.down_payment = down_payment
        self.collateral = collateral
        self.legal_issues = legal_issues
        self.guarantor = guarantor

    def calculate_score(self):
        # Normalize credit score to 100 scale
        credit_score_normalized = (self.credit_score / 900) * 100

        # Calculate Debt-to-Income Ratio (DTI) (Lower is better)
        dti = (self.total_emi / (self.monthly_income + self.other_income)) * 100
        dti_score = max(0, 100 - dti)  # Higher DTI lowers the score

        # Income Stability Score
        savings_score = min(100, (self.savings / self.monthly_income) * 20)
        bank_balance_score = min(100, (self.bank_balance / self.monthly_income) * 10)
        income_stability_score = (savings_score + bank_balance_score) / 2

        # Loan-Specific Factors
        down_payment_score = min(100, (self.down_payment / self.loan_amount) * 50)
        collateral_score = 100 if self.collateral else 50
        loan_factors_score = (down_payment_score + collateral_score) / 2

        # Employment and Residence Stability
        employment_risk_score = 100 if self.employment_type == "Salaried" else 70
        residence_score = 100 if self.residence_type == "Owned" else 70
        employment_stability_score = (employment_risk_score + residence_score) / 2

        # Additional Risk Factors
        past_defaults_score = 50 if self.past_defaults else 100
        credit_utilization_score = max(0, 100 - self.credit_utilization)
        legal_issues_score = 50 if self.legal_issues else 100
        guarantor_risk_score = 70 if self.guarantor else 100
        risk_factors_score = (past_defaults_score + credit_utilization_score + legal_issues_score + guarantor_risk_score) / 4

        # Final Score Calculation
        final_score = (
            (credit_score_normalized * self.WEIGHTS["credit_score"]) +
            (dti_score * self.WEIGHTS["debt_to_income"]) +
            (income_stability_score * self.WEIGHTS["income_stability"]) +
            (loan_factors_score * self.WEIGHTS["loan_factors"]) +
            (employment_stability_score * self.WEIGHTS["employment_risk"]) +
            (risk_factors_score * self.WEIGHTS["risk_factors"]) 
        )

        return round(final_score, 2)

# Example usage
# data = {
#     "age": 30,
#     "employment_type": "Salaried",
#     "residence_type": "Owned",
#     "monthly_income": 60000,
#     "other_income": 10000,
#     "total_emi": 10000,
#     "savings": 200000,
#     "bank_balance": 50000,
#     "credit_score": 750,
#     "existing_loans": 2,
#     "past_defaults": False,
#     "credit_utilization": 30,
#     "loan_amount": 1000000,
#     "loan_type": "Home Loan",
#     "down_payment": 200000,
#     "collateral": True,
#     "legal_issues": False,
#     "guarantor": False
# }

# calculator = LoanEligibilityCalculator(**data)
# score = calculator.calculate_score()
# print(f"Loan Eligibility Score: {score}/100")
