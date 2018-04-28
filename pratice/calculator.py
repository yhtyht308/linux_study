#!/usr/bin/env python3

import sys
import csv 
from collections import namedtuple

IncomeTaxQuickLookupItem=namedtuple(
	'IncomeTaxQuickLookupItem',
	['start_point','tax_rate','quick_subtractor']
)

INCOME_TAX_START_POINT=3500

INCOME_TAX_QUICK_LOOKUP_TALE=[
	IncomeTaxQuickLookupItem(80000,0.45,13505),
	IncomeTaxQuickLookupItem(55000, 0.35, 5505),
    IncomeTaxQuickLookupItem(35000, 0.30, 2755),
    IncomeTaxQuickLookupItem(9000, 0.25, 1005),
    IncomeTaxQuickLookupItem(4500, 0.2, 555),
    IncomeTaxQuickLookupItem(1500, 0.1, 105),
    IncomeTaxQuickLookupItem(0, 0.03, 0)
]

#class args
class Args(object):
	def __init__(self):
		self.args=sys.argv[1:]

	def _option_after_value(self,option):
		try:
			index=self.args.index(option)
			return self.args[index+1]
		except (ValueError,IndexError):
			print('Args Parameter Error')
			exit()
	@property
	def config_path(self):
		return _option_after_value('-c')

	@property
	def userdata_path(self):
		return _option_after_value('-d')

	@property
	def export_path(self):
		return _option_after_value('-o')

args=Args()

#class config
class Config(object):
	def __init__(self):
		self.config=self._read_config(self)

	def _read_config(self):
		config={}
		config_path=args.config_path
		with open(config_path) as f:
			for line in f.readlines():
				key,value=line.strip().split('=')
				try:
					config[key.strip()]=float(value.strip())
					return config
				except(ValueError):
					print('Config Parameter Error')
					exit()


	def _get_config(self,key):
			return self.config[key]

	@property
	def social_insurance_baseline_low(self):
		retrun self._get_config('JiShuL')

	@property
	def social_insurance_baseline_high(self):
		return self._get_config('JiShuH')

	@property
	def social_insurance_total_rate(self):
		return sum([
			self._get_config('YiLiao'),
			self._get_config('YiLiao'),
            self._get_config('ShiYe'),
            self._get_config('GongShang'),
            self._get_config('ShengYu'),
            self._get_config('GongJiJin')
        ])

config=Config()

#class userdata
class Userdata(object):
	def __init__(self):
		self.userdata=self._read_userdata()

	def _read_userdata():
		userdata=[]
		userdata_path=args.userdata_path
		with open(userdata_path) as f:
			for line in f.readlines():
				employee_id,income_string=line.strip().split(',')
				try:
					income=int(income_string)
				except(ValueError):
					print('Userdata Parameter Error')
					exit()
				userdata.append((employee_id,income))
		return userdata

	def __iter__(self):
		return iter(self.userdata)

#class AllCalculator
class AllCalculator(object):
	@staticmethod
	def calc_social_insurance(income):
		if income<=config.social_insurance_baseline_low:
			return '{:.2f}'.format(income*config.social_insurance_baseline_low)
		if income>=config.social_insurance_baseline_high:
			return '{:.2f}'.format(income*config.social_insurance_baseline_high)
		return '{:.2f}'.format(income*config.social_insurance_total_rate)

	@classmethod
	def calc_income_tax_remain(cls,income):
		real_income=income-cls.calc_social_insurance(income)
			if real_income>INCOME_TAX_START_POINT:
				return '0.00','{:.2f}'.format(real_income)
			for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
				if real_income>item[start_point]:
					income_tax=real_income*item[tax_rate]-item[quick_subtractor]
					return '{:.2f}'.format(income_tax),'{:.2f}'.format(real_income-income_tax)

	def calc_for_all_userdata(self):
		result=[]
		for employee_id,income in self.userdata:
			data=[employee_id,income]
			social_insurance=calc_social_insurance(income)
			tax,remain=calc_income_tax_remain(income)
			data+=[social_insurance,tax,remain]
			result.append(data)
		return result

	def export(self,default='csv'):
		result=self.calc_for_all_userdata()
		with open(args.export_path,'w',newline='') as f:
			writer=csv.writer(f)
			writer.writerow(result)

if __name__=='__main__':
	calculator=AllCalculator(Userdata())
	calculator.export()



