
def inboundPallets():
    inboundPallets = """
SELECT * FROM(
    SELECT  
CASE WHEN CustomerName >= 430 THEN 430 ELSE CustomerName END As ID, FacilityName,
IsNull(month(DeliveryDate), 0) as month ,
PalletsReceived 
FROM WarehouseReceipt
WHERE DeliveryDate BETWEEN '1/01/2022 00:00:01' AND CAST(GETDATE() AS DATE) AND FacilityName !='ZTEST' AND
 CustomerName != 'PC' AND CustomerName !='Z_TEST')  test
 PIVOT (
    SUM(PalletsReceived) FOR month IN ([1] , [2] , [3] , [4] , [5] , [6] , [7] , [8] ,[9] , [10] , [11] , [12])) AS thingy
    """
    return inboundPallets


def outPallets():
    outPallets = """
SELECT * FROM(
    SELECT  
CASE WHEN CustomerName >= 430 THEN 430 ELSE CustomerName END As ID, FacilityName,
IsNull(month(ActualShipDate), 0) as month ,
PalletsShipped 
FROM ShipmentOrder
WHERE ActualShipDate BETWEEN '1/01/2022 00:00:01' AND CAST(GETDATE() AS DATE) AND FacilityName !='ZTEST' AND
 CustomerName != 'PC' AND CustomerName !='Z_TEST')  test
 PIVOT (
    SUM(PalletsShipped) FOR month IN ([1] , [2] , [3] , [4] , [5] , [6] , [7] , [8] ,[9] , [10] , [11] , [12])) AS thingy
    """
    return outPallets
