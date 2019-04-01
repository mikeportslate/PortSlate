# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 21:46:43 2019

@author: hyatu
"""
import datetime
import os
import portSlate_PrivateEquityFundWaterfall as pefw

#set inputs
inputs = {
        "PromoteStructureMethod": "IRR",
        "SponsorContribution": 0.1,
        "LP_IRR_Hurdles": [0.08, 0.12, 0.15],
        "SponsorPromote": [0.2, 0.3, 0.4],
        "Y0YE": datetime.datetime.strptime("2019-03-31","%Y-%m-%d").date(),
        "NetLeveredBeforeTaxCashFlow" : [-12025083,1210090,1258087,966584,1016520,1067454,1119407,1172400,1226452,1281585,1337820,1395181,56701018 ],
        "AssetManagementFees" : [114000,114000,114000,114000,114000,114000,114000,114000,114000,114000,114000,114000,114000],
        "AcquisitionDispositionFees" : [ 525000,0,0,0,0,0,0,0,0,0,0,0,828750 ]
        }

# os.chdir('C:\\Users\hyatu\OneDrive\Work\Portslate\PrivateEquityFundWaterfall')
# print(os.getcwd())

security=pefw.portSlate_PrivateEquityFundWaterfall(inputs)
InvestorLevelReturns = security.Calc_InvestorLevelReturns()

print("LP IRR: " + str( round( 100 * InvestorLevelReturns["LP_IRR"], 2 ) ) + "%" )
print("LP Equity Multiple: " + str( round( InvestorLevelReturns["LP_EquityMultiple"], 2 ) ) + "x" )

print("Sponsor IRR: " + str( round( 100 * InvestorLevelReturns["Sponsor_IRR"], 2 ) ) + "%" )
print("Sponsor Equity Multiple: " + str( round( InvestorLevelReturns["Sponsor_EquityMultiple"], 2 ) ) + "x" )

print("Total LP Distributions:\n" + str(InvestorLevelReturns["Total_LP_Distributions"]) )
print("Total LP Contributions:\n" + str(InvestorLevelReturns["Total_LP_Contributions"]) )
print("Total LP Profit:\n" + str(InvestorLevelReturns["Total_LP_Profit"]) )

print("Total Sponsor Distributions:\n" + str(InvestorLevelReturns["Total_Sponsor_Distributions"]) )
print("Total Sponsor Fees:\n" + str(InvestorLevelReturns["Total_Sponsor_Fees"]) )
print("Total Sponsor Contributions:\n" + str(InvestorLevelReturns["Total_Sponsor_Contributions"]) )
print("Total Sponsor Profit:\n" + str(InvestorLevelReturns["Total_Sponsor_Profit"]) )