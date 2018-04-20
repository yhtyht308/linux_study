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
	
	def _value_after_option(self,option):
		try:
			index=self.args.index(option)
			return self.args[index+1]
		except(ValueError,IndexError):
			print('Parameter Error')
			exit()
	@property
	def config_path(self):
		return self._value_after_option('-c')
	@property
	def userdata_path(self):
		return self._value_after_option('-d')
	@property
	def export_path(self):
		return self._value_after_option('-o')

args=Args()

#configure class
class Config(object):
	def __init__(self):
		self.config=self._read_config()

	def _read_conifg(self):
		config_path=args.config_path
		config={}
		
		with open(config_path) as f:
			for line in f.readlines():
				key,value=line.strip().split('=')
				try:
					config[key]=float(value)
				except:
					print('Parameter Error')
					exit()
		return config

	def _get_config(self,key):
		try:
			return self.config
		except KeyError:
			print('Config Error')
			exit()
	@property
	def social_insurance_baseline_low(self):
		return self._get_config('JiShuL')
	@property
	def social_insurance_baseline_high(self):
		return self._get_config('JiShuH')
	@property
	def social_insurance_total_rate(self):
		return sum([
			self._get_config('YangLao'),
			self._get_config('YiLiao'),
			self._get_config('ShiYe'),
			self._get_config('GongShang'),
			self._get_config('ShengYu'),
			self._get_config('GongJiJin')
		])
config=Config()

#userdata class
class Userdata(object):
	def __init__(self):
		self.userdata=self._read_users_data()

	def  _read_users_data(self):
		userdata_path=args.userdata_path
		userdata=[]
		with open userdata_path as f:
			for line in f.readlines():
				employee_id,income_string=line.strip.split(',')
				try:
					income=int(income_string)
				except ValueError:
					print('Parameter Error')
					exit()
				userdata.append((employee_id,income))
		return userdata

	def __iter__(self):
		return iter(self.userdata)

#calculator class
class Calculator(object):
	def __init__(self,userdata):
		self.userdata=userdata

#calculator social insurance function 
	@staticmethod
	def calculator_social_insurance(income):
		if income<config.social_insurance_baseline_low:
			return config.social_insurance_baseline_low*config.social_insurance_total_rate
		if income>config.social_insurance_baselin_high:
			return config.social_insurance_baseline_high*config.social_insurance_total_rate

		return income*config.social_insurance_total_rate

	@classmethod
	def calculator_income_tax_remain(cls,income):
		social_insurance=cls.calculator_social_insurance(income)
		real_income=income-social_insurance
		income_paytax=real_income-ORIGING_POINT
		if income_paytax<=0:
			return '0.00','{:.2f}'.format(real_income)
	
		for item in INCOME_PAYTAX_LOOKUP_TABLE:
			if income_paytax > item.start_point:
				tax_pay=income_paytax*item.tax_rate-item.quick_substractor
#				return (format(tax_pay,".2f")),(format(real_income-tax_pay,".2f"))
				return '{:.2f}'.format(tax_pay),'{:.2f}'.format(real_income-tax_pay)


	def calculator_all_userdata(self):
		result=[]
		for employee_id,income in self.userdata:
			data=[employee_id,income]
			social_insurance='{:.2f}'.format(self.calculator_social_insurance(income))
			tax,remain=self.calculator_income_tax_remain(income)
			data+=[social_insurance,tax,remain]
			result.append(data)
		return result

	def export(self,default='csv')
		result=self.calculator_all_userdata()
		with open(args.export_path,'w',newline='') as f:
			writer=csv.writer(f)
			writer.writerows(result)		

if __name__=='__main__':
	calculator=Calculator(Userdata())
	calculator.export()
