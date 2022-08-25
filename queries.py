
def palletsRec():
    palletsRecQuery = """SELECT * FROM
    ( SELECT CASE WHEN CustomerName >= 430 THEN 430 ELSE CustomerName END As ID,
    year(DeliveryDate) as year, IsNull(month(DeliveryDate), 0) as month,
    PalletsReceived FROM WarehouseReceipt WHERE DeliveryDate BETWEEN '1/01/2021 00:00:01' AND '07/31/2022 23:59:59' AND 
    CustomerName != 'PC' AND CustomerName != 'Z_TEST')  test
    PIVOT ( SUM(PalletsReceived) FOR month IN ([1] , [2] , [3] , [4] , [5] , [6] , [7] , [8] ,[9] , [10] , [11] , [12])) AS thingy ORDER BY ID, year desc"""
    return palletsRecQuery

def storageByUnit():
    storage = """
SELECT 
CASE WHEN CustomerName >= 430 THEN 430 ELSE CustomerName END As ID,
FORMAT(EffectiveDate, 'yyyyMM') AS YM,
TransactionType, Sum(QTY) As QTY
FROM InventoryTransaction
WHERE CustomerName = '425' AND FacilityName = 'Fullerton' AND TransactionType <4 
GROUP BY CustomerName ,  TransactionType, FORMAT(EffectiveDate, 'yyyyMM')
ORDER BY FORMAT(EffectiveDate, 'yyyyMM')
    """
    return storage
def inboundCharges():
    inbound = """
SELECT  DocumentInvoice.ReceiptNumber, 
WarehouseReceipt.DeliveryDate, WarehouseReceipt.CustomerOrderNumber,WarehouseReceipt.CustomerPONumber, 
WarehouseReceipt.CarrierName, WarehouseReceipt.TransportMethod, WarehouseReceipt.PalletsReceived, WarehouseReceipt.QtyReceived, WarehouseReceipt.LadingQuantity
"&InboundLinkList&"
FROM DocumentInvoice LEFT JOIN  DocumentInvoiceDetail ON DocumentInvoice.DocumentInvoiceNumber = DocumentInvoiceDetail.DocumentInvoiceNumber 
LEFT JOIN WarehouseReceipt ON DocumentInvoice.ReceiptNumber = WarehouseReceipt.ReceiptNumber AND DocumentInvoice.FacilityName = WarehouseReceipt.FacilityName

WHERE DocumentInvoice.CustomerName = "425" AND DocumentInvoice.InvoiceDate BETWEEN '6/1/2022' AND '6/30/2022' AND DocumentInvoice.FacilityName!='Ztest' AND DocumentInvoice.ReceiptNumber != 0
GROUP BY DocumentInvoice.CustomerName, DocumentInvoice.FacilityName, DocumentInvoice.ReceiptNumber, DocumentInvoice.InvoiceDate,
WarehouseReceipt.DeliveryDate, WarehouseReceipt.CustomerOrderNumber,WarehouseReceipt.CustomerPONumber,  WarehouseReceipt.CarrierName, WarehouseReceipt.TransportMethod, WarehouseReceipt.QtyReceived, WarehouseReceipt.LadingQuantity, WarehouseReceipt.PalletsReceived

ORDER BY DocumentInvoice.ReceiptNumber 
    """
    return inbound

def inAcc():
    inAcc = """
SELECT Accessorial.AccessorialName, Accessorial.AccessorialAlias, Accessorial.Description , AccessorialCriteria.TableName, AccessorialCriteria.FieldName, AccessorialCriteria.FieldValue,
AccessorialCriteria.ComparisonType, AccessorialCriteria.DataType

FROM Accessorial Inner Join AccessorialCriteria ON Accessorial.AccessorialName = AccessorialCriteria.AccessorialName

WHERE Accessorial.GLCode = 'Inbound Handling' 
    """
    return inAcc