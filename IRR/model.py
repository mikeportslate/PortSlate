import pandas as pd
import numpy as np
import os


SPONS_PROMOTE = "sponser promote structure"
LP_SHARE = "limited partner equity share"
SPONS_SHARE = "sponser equity share"
SPONS_DISTR_PERC = "sponsor distribution percentage"
LP_DISTR_PERC = "limited partner distribution percentage"
REQ_RETURN_1 = "required reuturn for hurdle 1"

CASH_FLOW = "cash flows array"
M_FEES = "management fees array"
AQ_FEES = "aquisition fees array"
SIZE = "size or number of years in the model"

ADJ_LEV = "adjusted levered cash flows"
LP_CONTR = "limited partner contributions"
SPONSR_CONTR = "sponser contributions"

LP_REQ_RETURN = "required return by LP to hit hurdle 1"
START_BAL = "starting balance"
END_BAL_LP = "ending balance of the LP capital account"
LP_DIS = "distributions to limitedp partners"




class Model: 
	'''
	The actual model that runs all the calculations
	'''
	def __init__(self, in_dict):
		self.in_dict = in_dict
		self.data_dict = {}
		
		self.data_dict[ADJ_LEV] = self.in_dict[CASH_FLOW] - self.in_dict[M_FEES] - self.in_dict[AQ_FEES]
		self.data_dict[LP_CONTR] = -np.minimum(0, self.data_dict[ADJ_LEV] * self.in_dict[LP_SHARE])
		self.data_dict[SPONSR_CONTR] = -np.minimum(0, self.data_dict[ADJ_LEV] * self.in_dict[SPONS_SHARE])

		self.data_dict[START_BAL] = np.zeros(in_dict[SIZE])
		self.data_dict[LP_REQ_RETURN] = np.zeros(in_dict[SIZE])
		self.data_dict[LP_DIS] = np.zeros(in_dict[SIZE])
		self.data_dict[END_BAL_LP] = np.zeros(in_dict[SIZE])

		self.calculate_first_hurdle()


	def calculate_first_hurdle(self):
		data_dict = self.data_dict
		in_dict = self.in_dict

		data_dict[START_BAL][0] = 0
		data_dict[LP_REQ_RETURN][0] = 0
		data_dict[LP_DIS][0] = max(data_dict[ADJ_LEV][0], data_dict[LP_REQ_RETURN][0])
		data_dict[END_BAL_LP][0] = data_dict[START_BAL][0] + data_dict[LP_CONTR][0] - data_dict[LP_DIS][0]

		for i in range(1, self.in_dict[SIZE]):
			data_dict[START_BAL][i] = data_dict[END_BAL_LP][i-1]
			data_dict[LP_REQ_RETURN][i] = in_dict[REQ_RETURN_1] * data_dict[START_BAL][i]

			a = data_dict[START_BAL][i] + data_dict[LP_REQ_RETURN][i]
			b = max(data_dict[ADJ_LEV][i],0)*in_dict[LP_DISTR_PERC][0]
			data_dict[LP_DIS][i] = min(a, b)

			data_dict[END_BAL_LP][i] = data_dict[START_BAL][i] + data_dict[LP_CONTR][i] + data_dict[LP_REQ_RETURN][i] - data_dict[LP_DIS][i] 

		self.data_dict = data_dict #I know dictionaries are references but just in case
	




def read_test_data(filename):

	try:
		df = pd.read_csv(filename)
	except:
		print("Your file path is invalid")
		return None

	return df;


def initiate_model():
	input_dict = {}
	input_dict[SPONS_PROMOTE] = np.array([.1, .2, .3, .4])
	input_dict[LP_SHARE] = .9
	input_dict[SPONS_SHARE] = .1

	input_dict[SPONS_DISTR_PERC] = np.array([.1, .28, .37, .46])
	input_dict[LP_DISTR_PERC] = 1 - input_dict[SPONS_DISTR_PERC]
	input_dict[REQ_RETURN_1] = .08

	df = read_test_data("data.csv")

	input_dict[CASH_FLOW] = np.array(df.loc[0,"0":])
	input_dict[M_FEES] = np.array(df.loc[1,"0":])
	input_dict[AQ_FEES] = np.array(df.loc[2,"0":])
	input_dict[SIZE] = input_dict[CASH_FLOW].size

	model = Model(input_dict)

	return model

def print_model(model):

	for index in model.in_dict:
		print(model.in_dict[index])

	for index in model.data_dict:
		print(model.data_dict[index])


def main():
	model = initiate_model()
	#print_model(model)
	print(model.data_dict[END_BAL_LP])
	
main()	

