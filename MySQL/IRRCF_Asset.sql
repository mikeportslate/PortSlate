select AssetID, TransactionID, PurchaseDate as 'Period', "Gross Purchase Price", P_USD_TotalCostLevered
from t_finP_Transaction
where transactionID=3

union all

select 3, TransactionID, Period, 'Equity Contribution', Equity
from t_finP_EquityCF
where transactionID=3

union all

select AssetID, 3, Period, Field,Amount
from t_finP_AssetCF
where AssetID=3
and Field in ('NETOPERATINGINCOME', 'NTMNOI')

union all

select 3, LoanID, Period, 'DebtService', DebtService
from t_finP_LoanCF
where loanID =3

union all

select 3, LoanID, Period, 'DebtFunding', DebtFunding
from t_finP_LoanCF
where loanID =3

union all

select 3, LoanID, Period, 'DebtPayoff', DebtPayoff
from t_finP_LoanCF
where loanID =3


