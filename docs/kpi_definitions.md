<<<<<<< HEAD
# KPI Definitions
## Average Order Value (AOV)
AOV = SUM(UnitPrice * Quantity * (1 - Discount)) / COUNT(DISTINCT OrderID)
## Gross Margin (GM)
GM = SUM((UnitPrice - CostOfGoods) * Quantity * (1 - Discount))
- If CostOfGoods missing, approximate 70% of UnitPrice
=======
# KPI Definitions
## Average Order Value (AOV)
AOV = SUM(UnitPrice * Quantity * (1 - Discount)) / COUNT(DISTINCT OrderID)
## Gross Margin (GM)
GM = SUM((UnitPrice - CostOfGoods) * Quantity * (1 - Discount))
- If CostOfGoods missing, approximate 70% of UnitPrice
>>>>>>> 8e017c34374abf24b249e7e3dbbfa14b453c5c75
