#!/usr/bin/env python3
from collections import namedtuple
import sys
ORIGING_POINT=3500

IncomePaytaxLookupItem=namedtuple(
	'IncomePaytaxLookupItem',
	['start_point','tax_rate','quick_substractor']
)

INCOME_PAYTAX_LOOKUP_TABLE=[
	IncomePaytaxLookupItem(80000,0.45,13505),
	IncomePaytaxLookupItem(55000,0.35,5505),
	IncomePaytaxLookupItem(35000,0.30,2755),
	IncomePaytaxLookupItem(9000,0.25,1005),
	IncomePaytaxLookupItem(4500,0.20,555),
	IncomePaytaxLookupItem(1500,0.10,105),
	IncomePaytaxLookupItem(0,0.03,0)
]

def calculator_tax_pay(income):
	income_paytax=income-ORIGING_POINT
	if income_paytax<=0:
		return 0
	
	for item in INCOME_PAYTAX_LOOKUP_TABLE:
		if income_paytax > item.start_point:
			tax_pay=income_paytax*item.tax_rate-item.quick_substractor
			return(format(tax_pay,".2f"))

def main():
	if len(sys.argv)!=2:
		print("Parameter Error")
		exit()
	try:
		income=int(sys.argv[1])
	except:
		print('Parameter Error')
		print("Please input the int number")
		exit()
	paytax=calculator_tax_pay(income)
	print(paytax)

if __name__=='__main__':
	main()

