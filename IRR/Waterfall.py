# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 21:43:24 2019

@author: hyatu
"""
import numpy as np

class Waterfall:
    
        def __init__(self, inputs):
            self.PromoteStructureMethod = inputs["PromoteStructureMethod"]
            self.SponsorContribution = inputs["SponsorContribution"]
            self.LPContribution = 1 - self.SponsorContribution
            self.LP_IRR_Hurdles = inputs["LP_IRR_Hurdles"]
            self.SponsorPromote = inputs["SponsorPromote"]
            self.Y0YE = inputs["Y0YE"]
            self.NYears = len(inputs["NetLeveredBeforeTaxCashFlow"])
            self.NetLeveredBeforeTaxCashFlow = np.array(inputs["NetLeveredBeforeTaxCashFlow"])
            self.AssetManagementFees = np.array(inputs["AssetManagementFees"])
            self.AcquisitionDispositionFees = np.array(inputs["AcquisitionDispositionFees"])
            self.AdjustedLeveredBeforeTaxCashFlow = self.NetLeveredBeforeTaxCashFlow - self.AssetManagementFees - self.AcquisitionDispositionFees
            self.LeveredIRR = np.irr(self.AdjustedLeveredBeforeTaxCashFlow)
            self.ContributionsFromLP = -np.minimum(self.AdjustedLeveredBeforeTaxCashFlow*self.LPContribution,0)
            self.ContributionsFromSponsor = -np.minimum(self.AdjustedLeveredBeforeTaxCashFlow*self.SponsorContribution,0)
            
        
        def Calc_ReturnCapitalHurdle(self, hurdle_num, PriorDistributions = [], PriorCashFlowRemaining = [], PriorTotalDistributions = []):
            #hurdle_num=4
            #PriorDistributions = ThisHurdle["Next_PriorDistributions"]
            #PriorCashFlowRemaining = ThisHurdle["CashFlowRemaining"]
            #PriorTotalDistributions = ThisHurdle["Next_PriorTotalDistributions"]
            
            if len(PriorDistributions) ==0:
                PriorDistributions = np.zeros(self.NYears)
                PriorCashFlowRemaining = np.zeros(self.NYears)
                PriorTotalDistributions = np.zeros(self.NYears)
            if hurdle_num == 1:
                SponsorDistribution = self.SponsorContribution
                LPDistribution = 1 - SponsorDistribution
            else:
                SponsorDistribution = 1 - self.LPContribution*(1-self.SponsorPromote[hurdle_num - 2])
                LPDistribution = 1 - SponsorDistribution
            ThisHurdle = {}
            if hurdle_num <= len(self.LP_IRR_Hurdles):
                ReturnThreshold = self.LP_IRR_Hurdles[hurdle_num - 1]   
                BeginningBalance_LPCapitalAccount = np.array([0])
                ReqReturnLPHit2Hurdle = np.array([0])
                if hurdle_num == 1:
                    Distributions2LP = np.array([max(ReqReturnLPHit2Hurdle[0],self.AdjustedLeveredBeforeTaxCashFlow[0])])
                else:
                    temp1 = BeginningBalance_LPCapitalAccount[0] + ReqReturnLPHit2Hurdle[0] - PriorDistributions[0]
                    temp2 = PriorCashFlowRemaining[0] * LPDistribution
                    Distributions2LP = np.array([min(temp1,temp2)])
                EndingBalance_LPCapitalAccount = np.array([BeginningBalance_LPCapitalAccount[0]+self.ContributionsFromLP[0]-Distributions2LP[0]])
                for i in range(1,self.NYears):
                    temp_BeginningBalance_LPCapitalAccount = EndingBalance_LPCapitalAccount[i-1]
                    BeginningBalance_LPCapitalAccount = np.append(BeginningBalance_LPCapitalAccount, [temp_BeginningBalance_LPCapitalAccount])
                    if self.PromoteStructureMethod == "Equity Multiple":
                        temp_ReqReturnLPHit2Hurdle = self.ContributionsFromLP[0]*(ReturnThreshold - 1)
                    else:
                        temp_ReqReturnLPHit2Hurdle = BeginningBalance_LPCapitalAccount[i]*ReturnThreshold
                    ReqReturnLPHit2Hurdle = np.append(ReqReturnLPHit2Hurdle, [temp_ReqReturnLPHit2Hurdle])
                    if hurdle_num == 1:
                        temp_Distributions2LP = min(temp_BeginningBalance_LPCapitalAccount + temp_ReqReturnLPHit2Hurdle, max(0,self.AdjustedLeveredBeforeTaxCashFlow[i])*LPDistribution)
                    else:
                        temp1_Distributions2LP = temp_BeginningBalance_LPCapitalAccount + temp_ReqReturnLPHit2Hurdle - PriorDistributions[i]
                        temp2_Distributions2LP = PriorCashFlowRemaining[i]*LPDistribution
                        temp_Distributions2LP = min(temp1_Distributions2LP,temp2_Distributions2LP)
                    Distributions2LP = np.append(Distributions2LP,[temp_Distributions2LP])
                    temp_EndingBalance_LPCapitalAccount = temp_BeginningBalance_LPCapitalAccount+temp_ReqReturnLPHit2Hurdle+self.ContributionsFromLP[i]-temp_Distributions2LP - PriorDistributions[i]
                    EndingBalance_LPCapitalAccount = np.append(EndingBalance_LPCapitalAccount,[temp_EndingBalance_LPCapitalAccount])
                Distribution2Sponsor = Distributions2LP*(SponsorDistribution/LPDistribution)
                TotalDistributions = Distribution2Sponsor + Distributions2LP
                CashFlowRemaining = np.array( [max(0,x) for x in self.AdjustedLeveredBeforeTaxCashFlow - TotalDistributions - PriorTotalDistributions])
                
                ThisHurdle["HurdleNum"] = hurdle_num    
                ThisHurdle["SponsorDistribution"] = SponsorDistribution
                ThisHurdle["LPDistribution"] = LPDistribution
                ThisHurdle["BeginningBalance_LPCapitalAccount"] = BeginningBalance_LPCapitalAccount 
                ThisHurdle["ReqReturnLPHit2Hurdle"] = ReqReturnLPHit2Hurdle 
                ThisHurdle["Distributions2LP"] = Distributions2LP 
                ThisHurdle["EndingBalance_LPCapitalAccount"] = EndingBalance_LPCapitalAccount 
                ThisHurdle["Distribution2Sponsor"] = Distribution2Sponsor 
                ThisHurdle["TotalDistributions"] = TotalDistributions 
                ThisHurdle["CashFlowRemaining"] = CashFlowRemaining 
                ThisHurdle["Next_PriorDistributions"] = Distributions2LP + PriorDistributions
                ThisHurdle["Next_PriorTotalDistributions"] = TotalDistributions + PriorTotalDistributions
            else:
                ThisHurdle["Distributions2LP"] = PriorCashFlowRemaining* LPDistribution
                ThisHurdle["Distribution2Sponsor"] = PriorCashFlowRemaining - ThisHurdle["Distributions2LP"]
                ThisHurdle["TotalDistributions"] = PriorCashFlowRemaining 
                ThisHurdle["CashFlowRemaining"] = PriorCashFlowRemaining -  ThisHurdle["TotalDistributions"]
            return( ThisHurdle )
            
        def Calc_InvestorLevelReturns(self):
            N_Hurdles = len(self.LP_IRR_Hurdles) + 1
            Total_LP_Distributions = np.zeros(self.NYears)
            Total_Sponsor_Distributions = np.zeros(self.NYears)
            Total_LP_Contributions = self.ContributionsFromLP
            Hurdles_details = []
            for ih in range(1,N_Hurdles + 1 ):
                if ih == 1:
                    temp_hurdle = self.Calc_ReturnCapitalHurdle(ih)
                else:
                    temp_hurdle = self.Calc_ReturnCapitalHurdle(ih, PriorDistributions = PriorDistributions, PriorCashFlowRemaining = PriorCashFlowRemaining, PriorTotalDistributions = PriorTotalDistributions)
                Hurdles_details.append(temp_hurdle)
                if ih < N_Hurdles:
                    PriorDistributions = temp_hurdle["Next_PriorDistributions"]
                    PriorCashFlowRemaining = temp_hurdle["CashFlowRemaining"]
                    PriorTotalDistributions = temp_hurdle["Next_PriorTotalDistributions"]
                Total_LP_Distributions = Total_LP_Distributions + temp_hurdle["Distributions2LP"]
                Total_Sponsor_Distributions = Total_Sponsor_Distributions + temp_hurdle["Distribution2Sponsor"]

            Total_LP_Profit = Total_LP_Distributions - Total_LP_Contributions
            LP_IRR = np.irr(Total_LP_Profit)
            LP_EquityMultiple = sum(Total_LP_Distributions) / sum(Total_LP_Contributions)

            Total_Sponsor_Fees = self.AssetManagementFees + self.AcquisitionDispositionFees
            Total_Sponsor_Contributions = -( np.array([ min(0,x) for x in self.AdjustedLeveredBeforeTaxCashFlow ]) + self.ContributionsFromLP )
            Total_Sponsor_Profit = Total_Sponsor_Distributions + Total_Sponsor_Fees - Total_Sponsor_Contributions
            Sponsor_IRR = np.irr(Total_Sponsor_Profit)
            Sponsor_EquityMultiple = sum(Total_Sponsor_Distributions)/sum(Total_Sponsor_Contributions)
            
            InvestorLevelReturns = {}
            InvestorLevelReturns["LP_IRR"] = LP_IRR
            InvestorLevelReturns["LP_EquityMultiple"] = LP_EquityMultiple
            InvestorLevelReturns["Total_LP_Distributions"] = Total_LP_Distributions
            InvestorLevelReturns["Total_LP_Contributions"] = Total_LP_Contributions
            InvestorLevelReturns["Total_LP_Profit"] = Total_LP_Profit
            
            InvestorLevelReturns["Sponsor_IRR"] = Sponsor_IRR
            InvestorLevelReturns["Sponsor_EquityMultiple"] = Sponsor_EquityMultiple
            InvestorLevelReturns["Total_Sponsor_Distributions"] = Total_Sponsor_Distributions
            InvestorLevelReturns["Total_Sponsor_Fees"] = Total_Sponsor_Fees
            InvestorLevelReturns["Total_Sponsor_Contributions"] = Total_Sponsor_Contributions
            InvestorLevelReturns["Total_Sponsor_Profit"] = Total_Sponsor_Profit
            self.Hurdles_details = Hurdles_details
            self.InvestorLevelReturns = InvestorLevelReturns
            return( InvestorLevelReturns )
            
            

            
            