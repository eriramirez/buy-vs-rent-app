import streamlit as st


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
    # buy inputs
    "buy_price": {"default":600_000, "help":"value of the property at t=0"}, 
    "down_payment": {"default":0.2, "help": "percentage of the buy price that will be paid in advance"},
    "buy_closing_fees": {"default":2_000, "help": "amount in USD of the buy-closing-fees"},
    "buy_tax": {"default":0.03, "help":"percentage of the buy-price that will be paid as tax"},
    "current_rent": {"default":3_000, "help":"amount of monthly rent in USD that you currently pay"},
    
    # maintainance inputs
    "monthly_condo_fee": {"default":1_055, "help":"monthly amount that should be paid in USD if you own the property"},
    "monthly_tax": {"default":300, "help":"monthly amount that should be paid in USD if you own the property"},
    "maintainance": {"default":50, "help":"montlhy amount of maintainance expenses in USD if you own the property"}, 
    
    # loan inputs
    "annual_interest_rate": {"default":.04, "help":"percentage anualized interest rate for the loan"},
    "yearly_compound_periods": {"default":6, "help":"if semiannual, then 6; if monthly, then 1"},
    "loan_life_months": {"default":300, "help":"number of months given for the loan"},
    
    # sell inputs
    "sell_price": {"default":600_000, "help":"selling value of the property at the time of the sale"},
    "month_of_sale": {"default":24, "help":"number of month when the sell takes place"},
    "sell_closing_fees": {"default":2_000, "help":"amount in USD of the selling closing fees"},
    "sell_realtor_fee": {"default":0.05, "help":"percentage of the sell price that will be paid to realtor"}
}

# get inputs
case = dict()
for k, v in base_case.items():
    k_label = k.replace("_", " ")
    case[k] = float(st.text_input(k_label, v["default"], help=v["help"]))


net_income = main(case)
st.write("# Should I buy?")
if net_income > 0:
    st.write("**Yes**. According to this simulation, buying is profitable.")
else:
    st.write("**No**. According to this simulation, buying is unprofitable.")





















