"""
For investments over $1M it can be typically assumed that they will return 5% forever.
Using the [2022 - 2023 JMU Cost of Attendance](https://www.jmu.edu/financialaid/learn/cost-of-attendance-undergrad.shtml),
calculate how much a rich alumnus would have to give to pay for one full year (all costs) for an in-state student
and an out-of-state student. Store your final answer in the variables: "in_state_gift" and "out_state_gift".

Note: this problem does not require the "compounding interest" formula from the previous problem.

"""

#Total cost of attendance for one in/out of state student (USD)
in_state_cost = 30792
out_state_cost = 47882

#Interest rate
rate = 5 / 100

#Final answers
in_state_gift = in_state_cost / rate

out_state_gift = out_state_cost / rate

#Printing final answers
print('alumn would need to donate', in_state_gift, 'USD to pay for one in-state student.')
print('alumn would need to donate', out_state_gift, 'USD to pay for one out-of-state student.')