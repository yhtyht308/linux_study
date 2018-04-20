#!/usr/bin/env python3
#-*-coding:utf-8 -*-

import sys
import csv

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

#deal with parameters class
class Args(object):
	def __init__(self):
		self.args=sys.argv[1:] 

#configure class
class Config(object):
	def __init__(self):
		self.config=self._read_config()

	def _read_conifg(self):
		config={}

#userdata class
class Userdata(object):
	def __init__(self):
		self.userdata=self._read_users_data()

	def  _read_users_data(self):
		userdata=[]

#calculator class
class Calculator(object):
	def __init__(self,userdata):
		self.userdata=userdata


#calculator social insurance function 
	def calculator_social_insurance(income):
		social_insurance= income*sum(SOCIAL_INSURANCE_RATE.values())
		return social_insurance

def calculator_tax_pay(income):
	social_insurance=calculator_social_insurance(income)
	income_paytax=income-ORIGING_POINT-social_insurance
	if income_paytax<=0:
		return 0
	
	for item in INCOME_PAYTAX_LOOKUP_TABLE:
		if income_paytax > item.start_point:
			tax_pay=income_paytax*item.tax_rate-item.quick_substractor
#			return(format(tax_pay,".2f"))
			return tax_pay

#calculator take-home pay function
def calculator_take_home_pay(income):
	social_insurance=calculator_social_insurance(income)
	tax_pay=calculator_tax_pay(income)
	take_home_pay=income-social_insurance-tax_pay
	return (format(take_home_pay,".2f"))

	def calculator_all_userdata(self):
		result=[]

	def export(self,default='csv')
		
def main():
	if len(sys.argv)<2:
		print("Parameter Error")
		exit()
#deal with parameters
#for arg in sys.argv[1:]
#arg.split(':')
#char change to int and try_except 
	for arg in sys.argv[1:]:
		employ_id,income_string=arg.split(':')
		try:
			income=int(income_string)
		except:
			print('Parameter Error')
			exit()
		remain=calculator_take_home_pay(income)
		print('{}:{}'.format(employ_id,remain))

if __name__=='__main__':
	main()

