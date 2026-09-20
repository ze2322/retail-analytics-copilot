# KPI Definitions
## Average Order Value (AOV)
AOV = SUM(UnitPrice * Quantity * (1 - Discount)) / COUNT(DISTINCT OrderID)
## Gross Margin (GM)
GM = SUM((UnitPrice - CostOfGoods) * Quantity * (1 - Discount))
- If CostOfGoods missing, approximate 70% of UnitPrice
