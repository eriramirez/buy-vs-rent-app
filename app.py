import streamlit as st
from copy import copy


# Utility functions

def get_loan(buy_price, down_payment, **kwargs):
    return buy_price * (1 - down_payment)

def get_monthly_effective_rate(annual_interest_rate, yearly_compound_periods, **kwargs):
    return ((1 + (annual_interest_rate / 12 * yearly_compound_periods))**(1 / yearly_compound_periods)) - 1

def get_monthly_payment(loan, monthly_effective_rate, loan_life_months, **kwargs):
    i = monthly_effective_rate
    n = loan_life_months
    return loan * i *(1 + i)**n / ((1 + i)**n - 1)

def get_disbursement(buy_price, down_payment, buy_tax, buy_closing_fees, **kwargs):
    return (buy_tax + down_payment) * buy_price + buy_closing_fees

def get_opportunity_cost(disbursment, monthly_effective_rate):
    return disbursment * monthly_effective_rate

def get_marginal_payment(monthly_payment, opportunity_cost, current_rent, monthly_condo_fee, monthly_tax, maintainance, **kwargs):
    monthly_outflow = monthly_condo_fee + monthly_tax + maintainance + monthly_payment + opportunity_cost
    return monthly_outflow - current_rent

def get_sell_inflow(sell_price, sell_closing_fees, sell_realtor_fee, **kwargs):
    return sell_price - sell_closing_fees - sell_realtor_fee * sell_price

def get_balance_due(monthly_payment, monthly_effective_rate, month_of_sale, loan_life_months, **kwargs):
    i = monthly_effective_rate
    pmt = monthly_payment
    months = loan_life_months - month_of_sale
    return pmt * (((1 + i)**months - 1) / (i *(1 + i)**months))

def get_future_value_marginal_payment(marginal_payment, monthly_effective_rate, month_of_sale, **kwargs):
    i = monthly_effective_rate
    return (marginal_payment * ((1 + i)**month_of_sale - 1)) / i

def get_pv_net_income(sell_inflow, balance_due, effective_monthly_rate, fv_marginal_pmt, disbursement, month_of_sale, **kwargs):
    net_income = sell_inflow - balance_due - fv_marginal_pmt - disbursement
    i = effective_monthly_rate
    return net_income / (1+i)**month_of_sale

def fcurrency(v):
    return f"{v:,.2f}"

def main(case):
    loan = get_loan(**case)
    st.metric("Loan", fcurrency(loan))
    i = get_monthly_effective_rate(**case)
    st.metric("Monthly Effective Rate", f"{i*100:.4f}%")
    payment = get_monthly_payment(loan, i, **case)
    st.metric("Monthly payment", fcurrency(payment))
    d = get_disbursement(**case)
    st.metric("Disbursement", fcurrency(d))
    opportunity_cost = get_opportunity_cost(d, i)
    st.metric("Opportunity Cost", fcurrency(opportunity_cost))
    marginal_payment = get_marginal_payment(payment, opportunity_cost, **case)
    sell_inflow = get_sell_inflow(**case)
    balance_due = get_balance_due(payment, i, **case)
    st.metric("Balance due", fcurrency(balance_due))
    fv_marginal_pmt = get_future_value_marginal_payment(marginal_payment, i, **case)
    st.metric("Future value marginal payment", fcurrency(fv_marginal_pmt))
    net_income = get_pv_net_income(sell_inflow, balance_due, i, fv_marginal_pmt, d, **case)
    st.metric("Net Income of the investment", fcurrency(net_income))
    return net_income


# User interface

"""
# Buy vs Rent
This simulator will provide the expected profit of buying a property compared to continue renting
"""

base_case = {
    # buy
    "buy_price": 600_000,
    "down_payment": 0.2,
    "buy_closing_fees": 2_000, # in USD
    "buy_tax": 0.03, # rate
    "current_rent": 3_000,
    # maintainance
    "monthly_condo_fee": 1_055,
    "monthly_tax": 300,
    "maintainance": 50,  
    # loan
    "annual_interest_rate": .04,
    "yearly_compound_periods": 6,
    "loan_life_months": 300,
    # sell
    "sell_price": 600_000,
    "month_of_sale": 24,
    "sell_closing_fees": 2_000,
    "sell_realtor_fee": 0.05
}

# get inputs
case = dict()
for k, v in base_case.items():
    k_label = k.replace("_", " ")
    case[k] = float(st.text_input(k_label, v))


net_income = main(case)
st.write("# Should I buy?")
if net_income > 0:
    st.write("**Yes**. According to this simulation, buying is profitable.")
else:
    st.write("**No**. According to this simulation, buying is unprofitable.")


# variable_inputs = (
#     dict(sell_price=600_000, month_of_sale=24),
#     dict(sell_price=600_000, month_of_sale=60),
#     dict(sell_price=600_000, month_of_sale=120),
# )
# cases = [case_gen(base_case, **kwargs) for kwargs in variable_inputs]




















