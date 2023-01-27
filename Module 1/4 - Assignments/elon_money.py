"""
This problem requires you to calculate compounding interest and final value of a  US treasury deposit based upon
current interest rates (that will be provided). Your analysis should return the final value of the investment
after a 1-year and 20-year period. The final values should be stored in the variables "ten_year_final"
and "twenty_year_final", respectively. Perform all your calculations in this file. Do not perform the calculations by hand
and simply write in the final result.

Prompt: On October 27th, 2022, Elon Musk purchased Twitter for $44B in total, with reportedly $33B of his own money. Since
that time, it appears this investment has not worked out. If Elon has instead bought $44B of US Treasury Bonds, how much
would his investment be worth in 10-year and 20-year bonds? Assume the 10-year bonds pay 3.96%,
the 20-year bonds pay 4.32%, with each compounding annually.
"""

### all your code below ###

#Initial investment of 44 Billion USD
elon_investment = 44000000000

#Interest rates (%) for each type of bond
ten_year_rate = 3.96
twenty_year_rate = 4.32

#Number of years for each type of bond
n = 10
n2 = 20


# final answer for 10-year
ten_year_final = f'{elon_investment * ((1 + (ten_year_rate / 100)) ** n):.2f}'

# final answer for 20-year
twenty_year_final = f'{elon_investment * ((1 + (twenty_year_rate / 100)) ** n2):.2f}'

#Printing out 
print(ten_year_final, ',', twenty_year_final)